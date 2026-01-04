"""
Example architecture.py template for projects using archlib.

Copy this file to your project root as architecture.py and customize it
with your Goals, Solutions, and Implementations.

Install archlib first:
    pip install archlib
    # or
    uv pip install archlib
"""

from archlib import Architecture, Goal, Implementation, Solution

# ============================================================================
# GOALS (The Why & What)
# ============================================================================

goal_example = Goal(
    id_tag="G-1", name="Example Feature", acceptance_test="tests/uat/test_example.py"
)

# ============================================================================
# SOLUTIONS (The How)
# ============================================================================

sol_example = Solution(
    id_tag="S-1",
    name="Example Solution",
    satisfies=[goal_example],
    requires=[],  # List other Solutions this depends on
    constraints={
        "complexity": "O(n)",
        "memory_limit": "100MB",
        "benchmark": "tests/bench/example_bench.py",
    },
)

# ============================================================================
# IMPLEMENTATIONS (The Reality)
# ============================================================================

impl_example = Implementation(
    id_tag="I-1",
    name="Example Implementation",
    implements=sol_example,
    code_files=["src/example.py"],
    test_files=["tests/test_example.py"],
    must_define={"src/example.py": ["ExampleClass", "example_function"]},
)

# ============================================================================
# ARCHITECTURE
# ============================================================================

if __name__ == "__main__":
    arch = Architecture(
        goals=[goal_example], solutions=[sol_example], implementations=[impl_example]
    )
    arch.cli()  # Handles: validate, spec --id, test --id
