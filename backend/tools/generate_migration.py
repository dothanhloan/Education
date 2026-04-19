# coding: utf-8
import re
from pathlib import Path

schema_path = Path(r"d:\HRM_ICS\backend\alembic\sql\schema_only_no_nhanvien.sql")
sql = schema_path.read_text(encoding="utf-8", errors="replace")

pattern = re.compile(r"CREATE TABLE `(?P<name>[^`]+)`", re.S)
table_names = pattern.findall(sql)

migration_path = Path(r"d:\HRM_ICS\backend\alembic\versions\0001_create_tables_except_nhanvien.py")

content = [
    "\"\"\"Create tables except nhanvien\n\nRevision ID: 0001_create_tables_except_nhanvien\nRevises: \nCreate Date: 2026-04-05\n\"\"\"",
    "from pathlib import Path",
    "from alembic import op",
    "",
    "revision = '0001_create_tables_except_nhanvien'",
    "down_revision = None",
    "branch_labels = None",
    "depends_on = None",
    "",
    "",
    "def upgrade() -> None:",
    "    sql_path = Path(__file__).resolve().parents[1] / 'sql' / 'schema_only_no_nhanvien.sql'",
    "    op.execute(sql_path.read_text(encoding='utf-8'))",
    "",
    "",
    "def downgrade() -> None:",
]

for name in reversed(table_names):
    content.append(f"    op.execute(\"DROP TABLE IF EXISTS `{name}`;\")")

migration_path.write_text("\n".join(content) + "\n", encoding="utf-8")
