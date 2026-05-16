"""Architecture boundary tests using AST to check imports."""

import ast
import os
from pathlib import Path


def get_imports(filepath: Path) -> set[str]:
    """Parse a Python file and return a set of all imported module names."""
    with open(filepath, encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=str(filepath))
        except SyntaxError:
            return set()

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
            # Also add the specific imported names as potential submodules
            for alias in node.names:
                imports.add(f"{node.module}.{alias.name}")
    return imports


def get_all_python_files(base_dir: Path) -> list[Path]:
    """Return a list of all .py files in the given directory and subdirectories."""
    py_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                py_files.append(Path(root) / file)
    return py_files


def check_boundary(source_prefix: str, forbidden_prefix: str) -> None:
    """Check that modules matching source_prefix don't import forbidden_prefix."""
    src_dir = Path(__file__).parent.parent.parent / "src"

    for filepath in get_all_python_files(src_dir):
        rel_path = filepath.relative_to(src_dir)
        module_parts = list(rel_path.parts)
        if not module_parts:
            continue

        if module_parts[-1] == "__init__.py":
            module_parts.pop()
        else:
            module_parts[-1] = module_parts[-1][:-3]  # remove .py

        if not module_parts:
            continue

        module_name = ".".join(module_parts)

        # Check if the current module belongs to the source prefix
        if not (
            module_name == source_prefix
            or module_name.startswith(f"{source_prefix}.")
        ):
            continue

        imports = get_imports(filepath)
        for imp in imports:
            if imp == forbidden_prefix or imp.startswith(f"{forbidden_prefix}."):
                msg = (
                    f"Architecture violation: '{module_name}' imports '{imp}'. "
                    f"'{source_prefix}' must not import from '{forbidden_prefix}'."
                )
                raise AssertionError(msg)


def test_compute_does_not_import_api() -> None:
    """1. compute modules must not import workbench.api"""
    check_boundary("workbench.compute", "workbench.api")


def test_compute_does_not_import_agents() -> None:
    """2. compute modules must not import workbench.agents"""
    check_boundary("workbench.compute", "workbench.agents")


def test_agents_do_not_import_compute() -> None:
    """3. agents modules must not import workbench.compute"""
    check_boundary("workbench.agents", "workbench.compute")


def test_api_does_not_import_compute() -> None:
    """4. api modules must not import workbench.compute directly"""
    check_boundary("workbench.api", "workbench.compute")
