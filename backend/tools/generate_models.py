# coding: utf-8
import re
from pathlib import Path


def camel_case(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def split_type_and_rest(definition: str):
    depth = 0
    in_quote = False
    for idx, ch in enumerate(definition):
        if ch == "'":
            in_quote = not in_quote
        elif not in_quote:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif ch.isspace() and depth == 0:
                return definition[:idx].strip(), definition[idx:].strip()
    return definition.strip(), ""


dump_path = Path(r"c:\Users\loanl\Downloads\backup_qlns_old.sql")
sql = dump_path.read_text(encoding="utf-8", errors="replace")

pattern = re.compile(r"CREATE TABLE `(?P<name>[^`]+)` \((?P<body>.*?)\) ENGINE=.*?;", re.S)

create_tables = []
create_tables_no_nv = []
model_lines = []

model_lines.append("# coding: utf-8")
model_lines.append("import sqlalchemy as sa")
model_lines.append("from sqlalchemy.dialects import mysql")
model_lines.append("from app.db.base import Base")
model_lines.append("")


def parse_default(rest: str):
    match = re.search(r"DEFAULT\s+((?:'[^']*')|(?:[^\s,]+))", rest)
    if not match:
        return None
    value = match.group(1)
    if value.upper() == "NULL":
        return None
    if value.upper() in {"CURRENT_TIMESTAMP", "CURRENT_TIMESTAMP()"}:
        return "CURRENT_TIMESTAMP"
    return value


def parse_enum_values(type_str: str):
    return re.findall(r"'([^']*)'", type_str)


def map_type(type_str: str) -> str:
    type_lower = type_str.lower()
    if type_lower.startswith("tinyint(1)"):
        return "sa.Boolean"
    if type_lower.startswith("tinyint"):
        return "sa.SmallInteger"
    if type_lower.startswith("bigint"):
        return "sa.BigInteger"
    if type_lower.startswith("int"):
        return "sa.Integer"
    if type_lower.startswith("varchar"):
        length = re.search(r"varchar\((\d+)\)", type_lower)
        size = length.group(1) if length else "255"
        return f"sa.String({size})"
    if type_lower.startswith("char"):
        length = re.search(r"char\((\d+)\)", type_lower)
        size = length.group(1) if length else "1"
        return f"sa.String({size})"
    if type_lower.startswith("text") or type_lower.startswith("longtext"):
        return "sa.Text"
    if type_lower.startswith("date"):
        return "sa.Date"
    if type_lower.startswith("datetime"):
        fsp = re.search(r"datetime\((\d+)\)", type_lower)
        if fsp:
            return f"mysql.DATETIME(fsp={fsp.group(1)})"
        return "sa.DateTime"
    if type_lower.startswith("timestamp"):
        return "mysql.TIMESTAMP()"
    if type_lower.startswith("time"):
        return "sa.Time"
    if type_lower.startswith("decimal"):
        precision = re.search(r"decimal\((\d+),(\d+)\)", type_lower)
        if precision:
            return f"sa.Numeric({precision.group(1)}, {precision.group(2)})"
        return "sa.Numeric"
    if type_lower.startswith("double") or type_lower.startswith("float"):
        return "sa.Float"
    if type_lower.startswith("json"):
        return "mysql.JSON"
    if type_lower.startswith("enum"):
        values = parse_enum_values(type_str)
        items = ", ".join([repr(v) for v in values])
        return f"mysql.ENUM({items})"
    return "sa.Text"


for match in pattern.finditer(sql):
    table_name = match.group("name")
    body = match.group("body")

    create_tables.append(match.group(0))
    if table_name != "nhanvien":
        create_tables_no_nv.append(match.group(0))

    if table_name == "nhanvien":
        continue

    class_name = camel_case(table_name)
    model_lines.append(f"class {class_name}(Base):")
    model_lines.append(f"    __tablename__ = \"{table_name}\"")

    pk_columns = set()
    unique_constraints = []
    foreign_key_constraints = []
    indexes = []

    lines = [line.strip().rstrip(",") for line in body.splitlines() if line.strip()]

    for line in lines:
        if line.startswith("PRIMARY KEY"):
            cols = re.findall(r"`([^`]+)`", line)
            pk_columns.update(cols)
        elif line.startswith("UNIQUE KEY"):
            name_match = re.match(r"UNIQUE KEY `([^`]+)`", line)
            cols_match = re.search(r"\((.*?)\)", line)
            if name_match and cols_match:
                cols = [c.strip().strip("`") for c in cols_match.group(1).split(",")]
                unique_constraints.append((name_match.group(1), cols))
        elif line.startswith("KEY"):
            name_match = re.match(r"KEY `([^`]+)`", line)
            cols_match = re.search(r"\((.*?)\)", line)
            if name_match and cols_match:
                cols = [c.strip().strip("`") for c in cols_match.group(1).split(",")]
                indexes.append((name_match.group(1), cols))
        elif line.startswith("CONSTRAINT") and "FOREIGN KEY" in line:
            name_match = re.match(r"CONSTRAINT `([^`]+)`", line)
            cols_match = re.search(r"FOREIGN KEY \(([^\)]+)\)", line)
            ref = re.search(r"REFERENCES `([^`]+)` \(([^\)]+)\)", line)
            on_delete = re.search(r"ON DELETE ([A-Z ]+?)(?: ON UPDATE|$)", line)
            on_update = re.search(r"ON UPDATE ([A-Z ]+)", line)

            if name_match and cols_match and ref:
                col_list = [c.strip().strip("`") for c in cols_match.group(1).split(",")]
                ref_table = ref.group(1)
                ref_cols = [c.strip().strip("`") for c in ref.group(2).split(",")]
                foreign_key_constraints.append(
                    (
                        name_match.group(1),
                        col_list,
                        ref_table,
                        ref_cols,
                        on_delete.group(1).strip() if on_delete else None,
                        on_update.group(1).strip() if on_update else None,
                    )
                )

    for line in lines:
        if not line.startswith("`"):
            continue
        col_match = re.match(r"`(?P<name>[^`]+)`\s+(?P<definition>.+)", line)
        if not col_match:
            continue
        col_name = col_match.group("name")
        definition = col_match.group("definition")
        col_type, rest = split_type_and_rest(definition)

        nullable = "NOT NULL" not in rest
        autoincrement = "AUTO_INCREMENT" in rest
        default_value = parse_default(rest)

        args = [repr(col_name), map_type(col_type)]
        if col_name in pk_columns:
            args.append("primary_key=True")
        if not nullable:
            args.append("nullable=False")
        if autoincrement:
            args.append("autoincrement=True")
        if default_value is not None:
            if default_value == "CURRENT_TIMESTAMP":
                args.append("server_default=sa.text(\"CURRENT_TIMESTAMP\")")
            elif default_value.startswith("'"):
                args.append(f"server_default=sa.text({repr(default_value)})")
            else:
                args.append(f"server_default=sa.text(\"{default_value}\")")

        attr_name = col_name if col_name.isidentifier() else f"col_{col_name}"
        model_lines.append(f"    {attr_name} = sa.Column({', '.join(args)})")

    table_args = []
    for name, cols in unique_constraints:
        cols_list = ", ".join([repr(c) for c in cols])
        table_args.append(f"sa.UniqueConstraint({cols_list}, name=\"{name}\")")
    for name, cols, ref_table, ref_cols, on_delete, on_update in foreign_key_constraints:
        cols_list = ", ".join([repr(c) for c in cols])
        ref_list = ", ".join([repr(f"{ref_table}.{c}") for c in ref_cols])
        extra = []
        if on_delete:
            extra.append(f"ondelete=\"{on_delete}\"")
        if on_update:
            extra.append(f"onupdate=\"{on_update}\"")
        extra_sql = ", " + ", ".join(extra) if extra else ""
        table_args.append(
            f"sa.ForeignKeyConstraint([{cols_list}], [{ref_list}], name=\"{name}\"{extra_sql})"
        )
    for name, cols in indexes:
        cols_list = ", ".join([repr(c) for c in cols])
        table_args.append(f"sa.Index(\"{name}\", {cols_list})")

    if table_args:
        model_lines.append("    __table_args__ = (")
        for item in table_args:
            model_lines.append(f"        {item},")
        model_lines.append("    )")

    model_lines.append("")

schema_all = (
    "CREATE DATABASE IF NOT EXISTS hrm_ics\n"
    "  CHARACTER SET utf8mb4\n"
    "  COLLATE utf8mb4_unicode_ci;\n\n"
    "USE hrm_ics;\n\n"
    + "\n\n".join(create_tables)
    + "\n"
)

schema_no_nv = (
    "CREATE DATABASE IF NOT EXISTS hrm_ics\n"
    "  CHARACTER SET utf8mb4\n"
    "  COLLATE utf8mb4_unicode_ci;\n\n"
    "USE hrm_ics;\n\n"
    + "\n\n".join(create_tables_no_nv)
    + "\n"
)

out_models = Path(r"d:\HRM_ICS\backend\app\models\generated.py")
out_schema_all = Path(r"d:\HRM_ICS\backend\schema_only.sql")
out_schema = Path(r"d:\HRM_ICS\backend\alembic\sql\schema_only_no_nhanvien.sql")

out_models.write_text("\n".join(model_lines) + "\n", encoding="utf-8")
out_schema_all.write_text(schema_all, encoding="utf-8")
out_schema.write_text(schema_no_nv, encoding="utf-8")
