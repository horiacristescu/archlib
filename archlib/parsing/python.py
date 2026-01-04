"""Python AST parsing for symbol extraction."""

import ast
from typing import Dict, Set


def extract_python_symbols(file_path: str) -> Dict[str, Set[str]]:
    """Extract classes, functions, and globals from Python file."""
    symbols = {"classes": set(), "functions": set(), "globals": set()}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=file_path)
        module_body = set(tree.body)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                symbols["classes"].add(node.name)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                symbols["functions"].add(node.name)
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                # Check if this is a top-level assignment
                is_top_level = node in module_body
                if not is_top_level:
                    # Check if parent is in module body (but not a function/class)
                    for parent in module_body:
                        if node in ast.walk(parent):
                            if not isinstance(
                                parent,
                                (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef),
                            ):
                                is_top_level = True
                                break

                if is_top_level:
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                symbols["globals"].add(target.id)
                    elif isinstance(node, ast.AnnAssign) and isinstance(
                        node.target, ast.Name
                    ):
                        symbols["globals"].add(node.target.id)

    except SyntaxError as e:
        raise ValueError(f"Syntax error in {file_path}: {e}")
    except Exception as e:
        raise ValueError(f"Failed to parse {file_path}: {e}")

    return symbols


def extract_test_functions_python(file_path: str) -> Set[str]:
    """Extract test function names from Python test file (pytest convention)."""
    test_functions = set()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith("test_"):
                    test_functions.add(node.name)
                # Also check for pytest-style test names
                # Could add more patterns here

    except Exception as e:
        # If parsing fails, return empty set (will be reported as error)
        pass

    return test_functions

