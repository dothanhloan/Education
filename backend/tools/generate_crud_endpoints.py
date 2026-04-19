# coding: utf-8
import re
from pathlib import Path


def camel_case(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


schema_path = Path(r"d:\HRM_ICS\backend\schema_only.sql")
endpoints_dir = Path(r"d:\HRM_ICS\backend\app\api\v1\endpoints")
router_path = Path(r"d:\HRM_ICS\backend\app\api\v1\router.py")

schema = schema_path.read_text(encoding="utf-8", errors="replace")
pattern = re.compile(r"CREATE TABLE `(?P<name>[^`]+)`", re.S)

names = sorted({name for name in pattern.findall(schema) if name != "nhanvien"})

endpoints_dir.mkdir(parents=True, exist_ok=True)

imports = []
router_lines = ["from fastapi import APIRouter", "", "api_router = APIRouter()", ""]

for name in names:
    class_name = camel_case(name)
    file_name = f"{name}.py"
    module_name = name

    content = [
        "from app.api.v1.endpoints.crud_factory import create_crud_router",
        f"from app.models.generated import {class_name}",
        "",
        f"router = create_crud_router({class_name}, prefix='/{name}', tags=['{name}'])",
        "",
    ]

    (endpoints_dir / file_name).write_text("\n".join(content), encoding="utf-8")

    imports.append(f"from app.api.v1.endpoints import {module_name}")
    router_lines.append(f"api_router.include_router({module_name}.router)")

router_path.write_text("\n".join(imports + [""] + router_lines) + "\n", encoding="utf-8")
