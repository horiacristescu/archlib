#!/usr/bin/env python3
"""Tests for JavaScript/TypeScript AST parsing functionality."""

import os
import tempfile
from archlib.parsing.javascript import (
    extract_javascript_symbols,
    _parse_javascript_with_regex,
    extract_test_functions_javascript,
)


def test_regex_fallback_parsing():
    """Test regex-based parsing fallback when tree-sitter is unavailable."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
        f.write("""
class MyClass {
    constructor() {}
    methodName() {}
    async asyncMethod() {}
}

function standaloneFunction() {}

const arrowFunction = () => {};

async function asyncFunction() {}

module.exports = {
    exportedFunction: function() {}
};

const GLOBAL_CONST = 42;
""")
        temp_path = f.name

    try:
        symbols = _parse_javascript_with_regex(temp_path)
        
        # Verify classes extracted
        assert "MyClass" in symbols["classes"], "Class should be extracted"
        
        # Verify functions extracted
        assert "standaloneFunction" in symbols["functions"], "Function should be extracted"
        assert "arrowFunction" in symbols["functions"], "Arrow function should be extracted"
        assert "asyncFunction" in symbols["functions"], "Async function should be extracted"
        
        # Verify globals extracted
        assert "GLOBAL_CONST" in symbols["globals"], "Global should be extracted"
        
        print("✅ Regex fallback parsing works correctly")
        return True
    finally:
        os.unlink(temp_path)


def test_extract_javascript_symbols_graceful_degradation():
    """Test that extract_javascript_symbols gracefully degrades when tree-sitter unavailable."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
        f.write("""
class TestClass {
    testMethod() {}
}

function testFunction() {}
""")
        temp_path = f.name

    try:
        # Should work even without tree-sitter (falls back to regex)
        symbols = extract_javascript_symbols(temp_path)
        
        assert "TestClass" in symbols["classes"], "Class should be extracted"
        assert "testFunction" in symbols["functions"], "Function should be extracted"
        
        print("✅ Graceful degradation works (tree-sitter optional)")
        return True
    finally:
        os.unlink(temp_path)


def test_extract_test_functions_javascript():
    """Test extraction of test function names from JavaScript test files."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".test.js", delete=False) as f:
        f.write("""
test('should do something', () => {});
it('should handle edge cases', () => {});
test("should parse correctly", () => {});
""")
        temp_path = f.name

    try:
        test_functions = extract_test_functions_javascript(temp_path)
        
        assert "should do something" in test_functions, "Test name should be extracted"
        assert "should handle edge cases" in test_functions, "Test name should be extracted"
        assert "should parse correctly" in test_functions, "Test name should be extracted"
        
        print("✅ Test function extraction works")
        return True
    finally:
        os.unlink(temp_path)


if __name__ == "__main__":
    print("Testing JavaScript parser...")
    success = True
    success &= test_regex_fallback_parsing()
    success &= test_extract_javascript_symbols_graceful_degradation()
    success &= test_extract_test_functions_javascript()
    
    if success:
        print("\n✅ All JavaScript parser tests passed!")
        exit(0)
    else:
        print("\n❌ Some tests failed!")
        exit(1)




