#!/usr/bin/env python3
"""Basic test to verify archlib functionality."""

import os
import tempfile
from archlib import Architecture, Goal, Solution, Implementation

def test_basic_validation():
    """Test basic node creation and validation."""
    
    # Create temporary test files
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        
        # Create test directory structure
        os.makedirs("src", exist_ok=True)
        os.makedirs("tests", exist_ok=True)
        os.makedirs("tests/uat", exist_ok=True)
        
        # Create a simple Python file
        with open("src/example.py", "w") as f:
            f.write("""
class ExampleClass:
    pass

def example_function():
    pass

GLOBAL_VAR = 42
""")
        
        # Create a test file
        with open("tests/test_example.py", "w") as f:
            f.write("""
def test_example():
    assert True
""")
        
        # Create UAT file
        with open("tests/uat/test_example.py", "w") as f:
            f.write("""
def test_acceptance():
    assert True
""")
        
        # Define architecture
        goal = Goal("G-1", "Example Feature", "tests/uat/test_example.py")
        sol = Solution("S-1", "Example Solution", satisfies=[goal])
        impl = Implementation(
            "I-1",
            "Example Implementation",
            implements=sol,
            code_files=["src/example.py"],
            test_files=["tests/test_example.py"],
            must_define={"src/example.py": ["ExampleClass", "example_function", "GLOBAL_VAR"]}
        )
        
        arch = Architecture(goals=[goal], solutions=[sol], implementations=[impl])
        
        # Validate (should pass)
        print("Testing validation...")
        try:
            result = arch.validate()
            print("✅ Validation passed!")
            return True
        except SystemExit:
            print("❌ Validation failed!")
            return False

if __name__ == "__main__":
    success = test_basic_validation()
    exit(0 if success else 1)


