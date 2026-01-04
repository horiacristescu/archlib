#!/usr/bin/env python3
"""Test CLI commands."""

import os
import tempfile
import subprocess
from archlib import Architecture, Goal, Solution, Implementation

def test_spec_command():
    """Test spec command generation."""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        
        # Create minimal structure
        os.makedirs("src", exist_ok=True)
        os.makedirs("tests/uat", exist_ok=True)
        
        with open("src/example.py", "w") as f:
            f.write("class ExampleClass: pass\ndef example_function(): pass\n")
        
        with open("tests/uat/test_example.py", "w") as f:
            f.write("def test_acceptance(): pass\n")
        
        # Define architecture
        goal = Goal("G-1", "Example Feature", "tests/uat/test_example.py")
        sol = Solution(
            "S-1",
            "Example Solution",
            satisfies=[goal],
            constraints={"complexity": "O(n)", "benchmark": "tests/bench.py"}
        )
        impl = Implementation(
            "I-1",
            "Example Implementation",
            implements=sol,
            code_files=["src/example.py"],
            test_files=[],
            must_define={"src/example.py": ["ExampleClass", "example_function"]}
        )
        
        arch = Architecture(goals=[goal], solutions=[sol], implementations=[impl])
        
        # Test spec generation
        spec = arch.generate_spec("I-1")
        print("Generated spec:")
        print(spec)
        print("\n" + "="*60)
        
        # Check spec contains expected content
        assert "Mission Briefing" in spec
        assert "Example Implementation" in spec
        assert "Example Feature" in spec
        assert "complexity" in spec
        assert "src/example.py" in spec
        assert "ExampleClass" in spec
        
        print("✅ Spec generation test passed!")
        return True

if __name__ == "__main__":
    success = test_spec_command()
    exit(0 if success else 1)

