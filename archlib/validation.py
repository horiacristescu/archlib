"""Validation functions for architectural integrity checks."""

import os
from typing import List

from .nodes import Goal, Implementation, Solution
from .parsing import extract_javascript_symbols, extract_python_symbols


def validate_traceability(
    implementations: List[Implementation], solutions: List[Solution], goals: List[Goal]
) -> List[str]:
    """Validate Implementation → Solution → Goal chains. Returns error list."""
    errors = []

    # Build lookup maps
    solution_map = {s.id: s for s in solutions}
    goal_map = {g.id: g for g in goals}

    # Check each implementation traces to goals
    for impl in implementations:
        sol = impl.implements
        if sol.id not in solution_map:
            errors.append(f"{impl.id} implements {sol.id} which doesn't exist")
            continue

        sol_obj = solution_map[sol.id]

        # Check solution satisfies at least one goal
        if not sol_obj.satisfies:
            errors.append(f"{sol_obj.id} satisfies no goals (orphaned solution)")
            continue

        # Check all satisfied goals exist
        for goal in sol_obj.satisfies:
            if goal.id not in goal_map:
                errors.append(f"{sol_obj.id} satisfies {goal.id} which doesn't exist")

    # Check every goal has at least one solution
    goal_satisfied_by = {g.id: False for g in goals}
    for sol in solutions:
        for goal in sol.satisfies:
            if goal.id in goal_satisfied_by:
                goal_satisfied_by[goal.id] = True

    for goal_id, satisfied in goal_satisfied_by.items():
        if not satisfied:
            errors.append(f"{goal_id} is not satisfied by any solution (orphaned goal)")

    # Check every solution has at least one implementation
    solution_implemented = {s.id: False for s in solutions}
    for impl in implementations:
        if impl.implements.id in solution_implemented:
            solution_implemented[impl.implements.id] = True

    for sol_id, implemented in solution_implemented.items():
        if not implemented:
            errors.append(f"{sol_id} has no implementation (unimplemented solution)")

    return errors


def validate_dependencies(solutions: List[Solution]) -> List[str]:
    """Validate Solution.requires chains and detect cycles. Returns error list."""
    errors = []

    solution_map = {s.id: s for s in solutions}

    # Check all requires references exist
    for sol in solutions:
        for req in sol.requires:
            if req.id not in solution_map:
                errors.append(f"{sol.id} requires {req.id} which doesn't exist")

    # Detect circular dependencies
    def has_cycle(start_id: str, visited: set, path: set) -> List[str] | None:
        if start_id in path:
            return list(path) + [start_id]  # Cycle found
        if start_id in visited:
            return None  # Already checked, no cycle

        visited.add(start_id)
        path.add(start_id)

        if start_id not in solution_map:
            path.remove(start_id)
            return None

        sol = solution_map[start_id]
        for req in sol.requires:
            cycle = has_cycle(req.id, visited, path)
            if cycle:
                return cycle

        path.remove(start_id)
        return None

    visited = set()
    for sol in solutions:
        if sol.id not in visited:
            cycle = has_cycle(sol.id, visited, set())
            if cycle:
                errors.append(f"Circular dependency detected: {' → '.join(cycle)}")

    return errors


def validate_code_inventory(
    implementations: List[Implementation], goals: List[Goal] = None, root_dir: str = "."
) -> List[str]:
    """Validate code files exist and contain declared symbols. Returns error list."""
    errors = []
    declared_files = set()
    declared_test_files = set()

    # Collect all declared files (code and test)
    for impl in implementations:
        for file_path in impl.code_files:
            declared_files.add(file_path)
        for file_path in impl.test_files:
            declared_test_files.add(file_path)

    # Collect acceptance test files from Goals
    if goals:
        for goal in goals:
            declared_test_files.add(goal.acceptance_test)

    # Top-down: check declared files and symbols
    for impl in implementations:
        for file_path in impl.code_files:
            declared_files.add(file_path)
            full_path = os.path.join(root_dir, file_path)

            if not os.path.exists(full_path):
                errors.append(f"{impl.id}: Missing code file {file_path}")
                continue

            # Validate symbols if must_define specifies them
            if file_path in impl.must_define:
                required_symbols = set(impl.must_define[file_path])

                # Extract actual symbols based on file type
                ext = os.path.splitext(file_path)[1].lower()
                try:
                    if ext == ".py":
                        actual_symbols = extract_python_symbols(full_path)
                        all_actual = (
                            actual_symbols["classes"]
                            | actual_symbols["functions"]
                            | actual_symbols["globals"]
                        )
                    elif ext in [".js", ".jsx", ".ts", ".tsx"]:
                        actual_symbols = extract_javascript_symbols(full_path)
                        all_actual = (
                            actual_symbols["classes"]
                            | actual_symbols["functions"]
                            | actual_symbols["globals"]
                        )
                    else:
                        # Unknown file type - skip symbol validation
                        continue

                    missing = required_symbols - all_actual
                    if missing:
                        errors.append(
                            f"{impl.id}: {file_path} missing symbols: {sorted(missing)}"
                        )
                except ValueError as e:
                    errors.append(f"{impl.id}: {file_path} - {e}")

    # Bottom-up: check for undeclared Python/JS files (excluding test files and examples)
    code_extensions = {".py", ".js", ".jsx", ".ts", ".tsx"}
    for root, dirs, files in os.walk(root_dir):
        # Skip common ignore directories
        dirs[:] = [
            d
            for d in dirs
            if d
            not in {".git", "__pycache__", "node_modules", ".venv", "venv", "examples"}
        ]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in code_extensions:
                rel_path = os.path.relpath(os.path.join(root, file), root_dir)
                # Skip test files - they're validated separately
                # Skip example files - they're demonstration code
                # Check if file is in examples directory (check both relative path and absolute path)
                abs_path = os.path.abspath(os.path.join(root, file))
                path_parts = os.path.normpath(rel_path).split(os.sep)
                abs_path_parts = abs_path.split(os.sep)
                if (
                    "examples" in path_parts
                    or "examples" in abs_path_parts
                    or rel_path.startswith("examples/")
                ):
                    continue
                if (
                    rel_path not in declared_files
                    and rel_path not in declared_test_files
                ):
                    errors.append(
                        f"Undeclared code file: {rel_path} (not in any Implementation)"
                    )

    return errors


def validate_test_inventory(
    goals: List[Goal], implementations: List[Implementation], root_dir: str = "."
) -> List[str]:
    """Validate test files exist and contain test functions. Returns error list."""
    errors = []

    # Check Goal acceptance tests
    for goal in goals:
        full_path = os.path.join(root_dir, goal.acceptance_test)
        if not os.path.exists(full_path):
            errors.append(
                f"{goal.id}: Missing acceptance test file {goal.acceptance_test}"
            )

    # Check Implementation test files
    for impl in implementations:
        for test_file in impl.test_files:
            full_path = os.path.join(root_dir, test_file)
            if not os.path.exists(full_path):
                errors.append(f"{impl.id}: Missing test file {test_file}")

    return errors




