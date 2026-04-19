from pathlib import Path
import re

schema = Path(r"d:\\HRM_ICS\\backend\\schema_only.sql").read_text(encoding="utf-8", errors="replace")
pattern = re.compile(r"CREATE TABLE `(?P<name>[^`]+)` \\((?P<body>.*?)\\) ENGINE=.*?;", re.S)

multi_pk = []
no_pk = []

for match in pattern.finditer(schema):
    name = match.group("name")
    body = match.group("body")
    pk_match = re.search(r"PRIMARY KEY \\(([^\\)]+)\\)", body)
    if not pk_match:
        no_pk.append(name)
        continue
    cols = [c.strip().strip("`") for c in pk_match.group(1).split(",")]
    if len(cols) != 1:
        multi_pk.append((name, cols))

print("no_pk", no_pk)
print("multi_pk", multi_pk)
