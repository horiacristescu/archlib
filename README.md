# Archlib - Executable Architecture Library

A reusable Python library implementing the **Executable Architecture** methodology. Projects import archlib to create executable `architecture.py` files that validate their codebase structure matches declared architectural intent.

## What is Executable Architecture?

Instead of writing static documentation that rots over time, you write executable Python code that **validates itself**. Your `architecture.py` file acts as both documentation and validator - reading it explains the architecture, running it validates the architecture.

## The Triad of Reality

Archlib enforces a three-layer model:

1. **Goals** - Business objectives with acceptance tests (The Why & What)
2. **Solutions** - Architectural strategies with constraints (The How)
3. **Implementations** - Physical code artifacts with symbol declarations (The Reality)

## Installation

### From GitHub (Recommended)

**Using uv:**
```bash
uv pip install git+https://github.com/horiacristescu/archlib.git
```

**Using pip:**
```bash
pip install git+https://github.com/horiacristescu/archlib.git
```

**With optional tree-sitter support (better JavaScript/TypeScript parsing):**
```bash
uv pip install "git+https://github.com/horiacristescu/archlib.git#egg=archlib[treesitter]"
# or
pip install "git+https://github.com/horiacristescu/archlib.git#egg=archlib[treesitter]"
```

**Development install (editable mode):**
```bash
git clone https://github.com/horiacristescu/archlib.git
cd archlib
uv pip install -e .
```

### Verify Installation

```bash
python -c "from archlib import Architecture, Goal, Solution, Implementation; print('✅ Archlib installed successfully')"
```

## Quick Start

### 1. Read the Bootstrap Guide

**The best way to learn archlib is to read `examples/architecture.py`** - it's archlib defining itself using archlib. This file demonstrates:

- Complete Goal → Solution → Implementation structure
- Rich descriptions explaining each concept
- Real-world patterns and best practices
- How to use `description` fields for documentation
- Multi-file implementations
- Solution dependencies
- Constraint definitions

Copy this file to your project root and adapt it to your needs.

### 2. Create Your `architecture.py`

Start with the template or copy from `examples/architecture.py`:

```python
from archlib import Architecture, Goal, Solution, Implementation

# Define Goals
goal_example = Goal(
    id_tag="G-1",
    name="Example Feature",
    acceptance_test="tests/uat/test_example.py",
    description="What this goal achieves and why it matters"
)

# Define Solutions
sol_example = Solution(
    id_tag="S-1",
    name="Example Solution",
    satisfies=[goal_example],
    requires=[],  # Other Solutions this depends on
    constraints={"complexity": "O(n)", "benchmark": "tests/bench/example.py"},
    description="How this solution achieves the goal"
)

# Define Implementations
impl_example = Implementation(
    id_tag="I-1",
    name="Example Implementation",
    implements=sol_example,
    code_files=["src/example.py"],
    test_files=["tests/test_example.py"],
    must_define={"src/example.py": ["ExampleClass", "example_function"]},
    description="What code files and symbols this implementation provides"
)

# Assemble Architecture
if __name__ == "__main__":
    arch = Architecture(
        goals=[goal_example],
        solutions=[sol_example],
        implementations=[impl_example]
    )
    arch.cli()
```

### 3. Use CLI Commands

```bash
# Validate architecture (checks traceability, dependencies, code inventory, tests)
python architecture.py validate

# Generate mission briefing for an Implementation (context slicing for AI agents)
python architecture.py spec --id I-1

# Run tests for a specific node
python architecture.py test --id I-1
```

## The Development Cycle

1. **Define First**: Write your `architecture.py` with Goals, Solutions, and Implementations
2. **Write Tests**: Create acceptance tests (for Goals) and unit tests (for Implementations)
3. **Implement**: Write code that matches your declarations
4. **Validate**: Run `python architecture.py validate` frequently
5. **Iterate**: Update architecture as requirements evolve

**Key Insight**: Your `architecture.py` is a living document. As you add features, update it. The validator ensures code and architecture stay in sync.

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
Goal(id_tag: str, name: str, acceptance_test: str, description: str = None)
```
- `id_tag`: Unique identifier (e.g., "G-1")
- `name`: Human-readable name
- `acceptance_test`: Path to UAT file
- `description`: Optional documentation (included in spec generation)

### Solution
```python
Solution(
    id_tag: str,
    name: str,
    satisfies: List[Goal],
    requires: List[Solution] = None,
    constraints: Dict[str, Any] = None,
    description: str = None
)
```
- `satisfies`: Goals this solution satisfies
- `requires`: Other solutions this depends on
- `constraints`: Flexible constraint dictionary (e.g., `{"complexity": "O(n)", "benchmark": "path/to/bench.py"}`)
- `description`: Optional documentation

### Implementation
```python
Implementation(
    id_tag: str,
    name: str,
    implements: Solution,
    code_files: List[str],
    test_files: List[str] = None,
    must_define: Dict[str, List[str]] = None,
    description: str = None
)
```
- `implements`: Solution this implements
- `code_files`: Source files this implementation creates
- `test_files`: Unit/integration test files
- `must_define`: `{filepath: [symbols]}` mapping of required symbols
- `description`: Optional documentation

### Architecture
```python
Architecture(goals: List[Goal], solutions: List[Solution], implementations: List[Implementation])
```

**Methods:**
- `validate()` - Run all validation checks
- `generate_spec(impl_id)` - Generate mission briefing markdown
- `run_tests(node_id)` - Run tests for a specific node
- `cli()` - Command-line interface

## Examples

- **`examples/architecture.py`** - **Start here!** Archlib defining itself - complete example with rich descriptions
- **`examples/template.py`** - Minimal template for new projects

## Common Patterns

### Multi-File Implementation
```python
impl_data_layer = Implementation(
    id_tag="I-2",
    name="Data Access Layer",
    implements=sol_database,
    code_files=["src/db/connection.py", "src/db/models.py"],
    test_files=["tests/test_db.py"],
    must_define={
        "src/db/connection.py": ["DatabaseConnection"],
        "src/db/models.py": ["UserModel", "PostModel"]
    }
)
```

### Solution Dependencies
```python
sol_api = Solution(
    id_tag="S-2",
    name="REST API",
    satisfies=[goal_api_access],
    requires=[sol_jwt_auth],  # API depends on authentication
    constraints={"framework": "FastAPI"}
)
```

### JavaScript/TypeScript Support
Archlib automatically parses JavaScript and TypeScript files:

```python
impl_frontend = Implementation(
    id_tag="I-3",
    name="React Frontend",
    implements=sol_ui,
    code_files=["src/components/App.tsx"],
    test_files=["src/components/App.test.tsx"],
    must_define={"src/components/App.tsx": ["App"]}
)
```

## Troubleshooting

**"Missing symbols" error**: Ensure all declared symbols exist in the files. Check for typos or refactored names.

**"Undeclared code file" error**: Every Python/JS file must be declared in an Implementation. Add it to `code_files` or `test_files`.

**"Circular dependency" error**: Solutions have a circular dependency chain. Review your `requires` relationships.

**"Missing test file" error**: Declared test files don't exist. Create them or remove from `test_files`.

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
