# Archlib - Executable Architecture Library

A reusable Python library implementing the **Executable Architecture** methodology. Projects import archlib to create executable `architecture.py` files that validate their codebase structure matches declared architectural intent.

## What is Executable Architecture?

Instead of writing static documentation that rots over time, you write executable Python code that **validates itself**. Your `architecture.py` file acts as both documentation and validator - reading it explains the architecture, running it validates the architecture.

## The Triad of Reality

Archlib enforces a three-layer model:

1. **Goals** - Business objectives with acceptance tests (The Why & What)
2. **Solutions** - Architectural strategies with constraints (The How)
3. **Implementations** - Physical code artifacts with symbol declarations (The Reality)

## Quick Start

### 1. Install

**Using pip:**
```bash
pip install archlib
```

**Using uv:**
```bash
uv pip install archlib
```

**Optional: Install with tree-sitter support for better JavaScript/TypeScript parsing:**
```bash
pip install archlib[treesitter]
# or
uv pip install "archlib[treesitter]"
```

**Development install (from source):**
```bash
git clone <repo-url>
cd archlib
uv pip install -e .
```

### 2. Create architecture.py

```python
from archlib import Architecture, Goal, Solution, Implementation

# Define Goals
goal_compression = Goal(
    id_tag="G-1",
    name="Token-Efficient Compression",
    acceptance_test="tests/uat/test_token_budgets.py"
)

# Define Solutions
sol_scoring = Solution(
    id_tag="S-1",
    name="Hybrid Importance Scoring",
    satisfies=[goal_compression],
    constraints={"complexity": "O(n)", "benchmark": "tests/bench/scoring.py"}
)

# Define Implementations
impl_core = Implementation(
    id_tag="I-1",
    name="Core Scoring Logic",
    implements=sol_scoring,
    code_files=["src/core.py"],
    test_files=["tests/test_core.py"],
    must_define={"src/core.py": ["ScoredNode", "calculate_importance"]}
)

# Create Architecture
if __name__ == "__main__":
    arch = Architecture(
        goals=[goal_compression],
        solutions=[sol_scoring],
        implementations=[impl_core]
    )
    arch.cli()
```

### 3. Use CLI Commands

```bash
# Validate architecture
python architecture.py validate

# Generate mission briefing for Implementation
python architecture.py spec --id I-1

# Run tests for a node
python architecture.py test --id I-1
```

## Features

### ✅ Traceability Validation
Every Implementation must trace through Solution → Goal, ensuring code serves business value.

### ✅ Dependency Validation
Solution dependency chains are validated, circular dependencies are detected.

### ✅ Code Inventory
- Declared symbols (classes, functions, globals) must exist in files
- All Python/JavaScript files must be declared
- Supports Python (AST) and JavaScript/TypeScript (tree-sitter with regex fallback)

### ✅ Test Inventory
Test files must exist and contain expected test functions.

### ✅ CLI Tooling
- `validate` - Run all checks
- `spec --id` - Generate focused mission briefing for AI agents
- `test --id` - Run targeted tests

## API Reference

### Goal
```python
Goal(id_tag: str, name: str, acceptance_test: str)
```
- `id_tag`: Unique identifier (e.g., "G-1")
- `name`: Human-readable name
- `acceptance_test`: Path to UAT file

### Solution
```python
Solution(
    id_tag: str,
    name: str,
    satisfies: List[Goal],
    requires: List[Solution] = None,
    constraints: Dict[str, Any] = None
)
```
- `satisfies`: Goals this solution satisfies
- `requires`: Other solutions this depends on
- `constraints`: Flexible constraint dictionary

### Implementation
```python
Implementation(
    id_tag: str,
    name: str,
    implements: Solution,
    code_files: List[str],
    test_files: List[str] = None,
    must_define: Dict[str, List[str]] = None
)
```
- `implements`: Solution this implements
- `code_files`: Source files
- `test_files`: Test files
- `must_define`: `{filepath: [symbols]}` mapping

### Architecture
```python
Architecture(goals: List[Goal], solutions: List[Solution], implementations: List[Implementation])
```

**Methods:**
- `validate()` - Run validation
- `generate_spec(impl_id)` - Generate mission briefing
- `run_tests(node_id)` - Run tests for node
- `cli()` - Command-line interface

## Examples

See `examples/template.py` for a complete example.

## Migration from v1

If you're using v1 methodology (Intent → Requirement → Design → Task → Test), migrate by:

1. **Map Intent + Requirement → Goal** (merge business goals and constraints)
2. **Map Design → Solution** (preserve architectural strategy)
3. **Map Task → Implementation** (preserve code declarations)

See `EXECUTABLE_ARCHITECTURE.v2.md` for details.

## Requirements

- Python 3.7+
- Optional: `tree-sitter` for better JavaScript/TypeScript parsing (falls back to regex if unavailable)

## License

See LICENSE file.

