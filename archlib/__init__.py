"""
Archlib - Executable Architecture Library

A reusable Python library implementing the Executable Architecture methodology.
Projects import archlib to create executable architecture.py files that validate
their codebase structure matches declared architectural intent.

Usage:
    from archlib import Architecture, Goal, Solution, Implementation
    
    goal = Goal("G-1", "Feature X", "tests/uat/test_x.py")
    sol = Solution("S-1", "Strategy Y", satisfies=[goal])
    impl = Implementation("I-1", "Code Z", implements=sol, 
                          code_files=["src/z.py"], test_files=["tests/test_z.py"])
    
    arch = Architecture(goals=[goal], solutions=[sol], implementations=[impl])
    arch.cli()  # Run: python architecture.py validate|spec|test
"""

from .architecture import Architecture
from .nodes import Goal, Implementation, Node, Solution

__all__ = ["Node", "Goal", "Solution", "Implementation", "Architecture"]
