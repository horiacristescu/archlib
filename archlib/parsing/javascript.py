"""JavaScript/TypeScript AST parsing for symbol extraction."""

import os
import re
from typing import Any, Dict, Optional, Set


def _init_treesitter_parser(language: str) -> Optional[Any]:
    """Initialize tree-sitter parser for language. Returns None if unavailable."""
    try:
        from tree_sitter import Language, Parser

        # Map language names to tree-sitter language modules
        language_map = {
            "javascript": ("tree-sitter-javascript", "javascript"),
            "typescript": ("tree-sitter-typescript", "typescript"),
            "tsx": ("tree-sitter-typescript", "tsx"),
        }

        if language.lower() not in language_map:
            return None

        module_name, lang_name = language_map[language.lower()]
        # Try to load the language (this requires the grammar to be built)
        # For now, return None and fall back to regex
        # In production, you'd need to build the grammars first
        return None  # Placeholder - tree-sitter setup requires grammar compilation

    except ImportError:
        return None


def _parse_with_treesitter(
    file_path: str, language: str
) -> Optional[Dict[str, Set[str]]]:
    """Parse JS/TS file with tree-sitter. Returns None if tree-sitter unavailable."""
    parser = _init_treesitter_parser(language)
    if parser is None:
        return None

    # Tree-sitter implementation would go here
    # For now, return None to trigger regex fallback
    return None


def _parse_javascript_with_regex(file_path: str) -> Dict[str, Set[str]]:
    """Fallback regex-based parsing for JavaScript/TypeScript files."""
    symbols = {"classes": set(), "functions": set(), "globals": set()}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract ES6 classes
        class_pattern = r"class\s+(\w+)"
        classes = set(re.findall(class_pattern, content))
        symbols["classes"].update(classes)

        # Extract functions (multiple patterns)
        functions = set()

        # ES6 class methods
        for class_name in classes:
            class_pattern_full = rf"class\s+{class_name}\s*\{{"
            for match in re.finditer(class_pattern_full, content):
                class_start = match.end()
                next_class = content.find("class ", class_start)
                class_chunk = (
                    content[class_start:next_class]
                    if next_class != -1
                    else content[class_start:]
                )

                # Method patterns
                method_patterns = [
                    r"(\w+)\s*\([^)]*\)\s*{",  # methodName() {
                    r"(\w+)\s*=\s*\([^)]*\)\s*=>",  # methodName = () =>
                    r"(\w+)\s*=\s*async\s*\([^)]*\)\s*=>",  # async arrow
                ]
                for pattern in method_patterns:
                    matches = re.findall(pattern, class_chunk)
                    functions.update(matches)

        # Standalone functions
        function_patterns = [
            r"function\s+(\w+)\s*\(",
            r"const\s+(\w+)\s*=\s*(?:function|\(|async\s+function)",
            r"let\s+(\w+)\s*=\s*(?:function|\(|async\s+function)",
            r"var\s+(\w+)\s*=\s*(?:function|\(|async\s+function)",
            r"async\s+function\s+(\w+)\s*\(",
        ]
        for pattern in function_patterns:
            matches = re.findall(pattern, content)
            functions.update(matches)

        symbols["functions"].update(functions)

        # Extract module exports (globals)
        globals_set = set()

        # window.X = or const/let/var X = (not function)
        global_patterns = [
            r"window\.(\w+)\s*=",
            r"const\s+(\w+)\s*=\s*(?!function|\(|async)",
            r"let\s+(\w+)\s*=\s*(?!function|\(|async)",
            r"var\s+(\w+)\s*=\s*(?!function|\(|async)",
        ]
        for pattern in global_patterns:
            matches = re.findall(pattern, content)
            globals_set.update(matches)

        # module.exports
        module_exports_pattern = r"module\.exports\s*=\s*\{([^}]+)\}"
        module_match = re.search(module_exports_pattern, content, re.DOTALL)
        if module_match:
            exports_content = module_match.group(1)
            export_pattern = r"(\w+)\s*:"
            exported = re.findall(export_pattern, exports_content)
            functions.update(exported)  # Exports are usually functions

        symbols["globals"].update(globals_set)

    except Exception as e:
        raise ValueError(f"Failed to parse {file_path}: {e}")

    return symbols


def extract_javascript_symbols(file_path: str) -> Dict[str, Set[str]]:
    """Extract classes, functions, and exports from JavaScript/TypeScript file."""
    # Determine language from extension
    ext = os.path.splitext(file_path)[1].lower()
    language_map = {
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "tsx",
    }
    language = language_map.get(ext, "javascript")

    # Try tree-sitter first
    result = _parse_with_treesitter(file_path, language)
    if result is not None:
        return result

    # Fall back to regex
    return _parse_javascript_with_regex(file_path)


def extract_test_functions_javascript(file_path: str) -> Set[str]:
    """Extract test function names from JavaScript test file (test/it calls)."""
    test_functions = set()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract test/it function calls with string literals
        test_pattern = r"(?:test|it)\s*\(\s*['\"]([^'\"]+)['\"]"
        matches = re.findall(test_pattern, content)
        test_functions.update(matches)

    except Exception as e:
        pass

    return test_functions




