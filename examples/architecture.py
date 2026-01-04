"""
Example architecture.py for archlib project itself.

This demonstrates how to use archlib to define the architecture of archlib.
This is a meta-example - archlib uses archlib to validate itself.
"""

from archlib import Architecture, Goal, Implementation, Solution

# ============================================================================
# GOALS (The Why & What)
# ============================================================================

goal_executable_architecture = Goal(
    id_tag="G-1",
    name="Executable Architecture Validation",
    acceptance_test="../test_basic.py",
    description="""The core value proposition: architecture.py must validate itself (quine property),
ensuring declared structure matches actual codebase. This prevents architectural drift where code
evolves without updating architecture declarations. The validation engine performs
bidirectional reconciliation: top-down (declared symbols must exist) and bottom-up
(existing files must be declared), maintaining complete architectural ledger.""",
)

goal_multi_language_support = Goal(
    id_tag="G-2",
    name="Multi-Language AST Parsing",
    acceptance_test="../test_basic.py",
    description="""Projects use multiple languages (Python, JavaScript, TypeScript). Archlib must
extract symbols from all supported languages to validate code inventory. Python
uses built-in ast module, JavaScript/TypeScript uses tree-sitter with regex
fallback. This enables polyglot projects to use archlib without language-specific
limitations, making the architecture validator language-agnostic.""",
)

goal_cli_tooling = Goal(
    id_tag="G-3",
    name="CLI Tooling for Architecture Management",
    acceptance_test="../test_cli.py",
    description="""Architecture.py must function as project control plane, not just a validator.
CLI commands enable validation, mission briefing generation, and targeted test
execution. This transforms architecture.py from passive documentation into
active tooling that orchestrates development workflows and enables AI agent
coordination through focused context generation.""",
)

goal_context_slicing = Goal(
    id_tag="G-4",
    name="Context Slicing for AI Agents",
    acceptance_test="../test_cli.py",
    description="""When implementing a task, agents need focused context, not entire codebase.
The spec generator slices the architecture graph to extract only relevant Goals,
Constraints, and file targets for a specific Implementation. This reduces token
usage from thousands of lines to 50-200 lines, enabling efficient multi-agent
coordination where different agents work on different Implementations with
minimal context overlap.""",
)

# ============================================================================
# SOLUTIONS (The How)
# ============================================================================

sol_core_validation = Solution(
    id_tag="S-1",
    name="Core Validation Engine",
    satisfies=[goal_executable_architecture],
    constraints={
        "complexity": "O(n) where n = number of nodes",
        "validation_time": "<1s for typical projects",
        "error_reporting": "Structured with context",
        "benchmark": "../test_basic.py",
    },
    description="""Implements four validation checks: traceability (Implementation → Solution → Goal),
dependencies (no cycles, all references valid), code inventory (AST parsing),
and test inventory (test files exist). Uses flexible Dict[str, Any] constraints
enabling project-specific constraint definitions without modifying archlib core.
Runs in O(n) time where n is number of nodes. Error reporting includes node IDs,
file paths, and context to enable rapid debugging. This is the foundation that
all other solutions build upon.""",
)

sol_python_ast = Solution(
    id_tag="S-2",
    name="Python AST Parser",
    satisfies=[goal_multi_language_support],
    requires=[],
    constraints={
        "parser": "Built-in ast module",
        "symbols_extracted": "classes, functions, globals",
        "performance": "<10ms per file",
        "benchmark": "../test_basic.py",
    },
    description="""Uses Python's built-in ast module to walk syntax trees and extract classes,
functions (including async), and top-level globals. Distinguishes module-level
assignments from function-local assignments. Handles edge cases: nested classes,
decorators, type annotations. Performance target: <10ms per file for typical
codebases. This parser is the reference implementation for symbol extraction.""",
)

sol_javascript_ast = Solution(
    id_tag="S-3",
    name="JavaScript/TypeScript AST Parser",
    satisfies=[goal_multi_language_support],
    requires=[],
    constraints={
        "primary_parser": "tree-sitter (optional)",
        "fallback_parser": "regex-based extraction",
        "languages": "JavaScript, TypeScript, JSX, TSX",
        "llm_review": "claude",
    },
    description="""Primary parser uses tree-sitter for proper AST construction (handles ES6+, JSX,
TypeScript, decorators, async/await). Falls back to regex-based extraction when
tree-sitter unavailable, ensuring graceful degradation. Regex patterns handle
ES6 classes, function declarations, arrow functions, and module exports (CommonJS
and ES6). This dual-mode approach balances robustness with accessibility.""",
)

sol_cli_interface = Solution(
    id_tag="S-4",
    name="Command-Line Interface",
    satisfies=[goal_cli_tooling],
    requires=[sol_core_validation],
    constraints={
        "commands": "validate, spec, test",
        "framework": "argparse",
        "exit_codes": "0=success, 1=failure",
        "test": "../test_cli.py",
    },
    description="""Provides three commands: validate (runs all checks), spec --id (generates mission
briefing), test --id (runs targeted tests). Uses argparse with subparsers for
extensible command routing. Exit codes: 0=success, 1=failure, enabling CI/CD
integration. Requires core validation engine to perform actual validation work.
This transforms architecture.py from passive file into active project control plane.""",
)

sol_spec_generator = Solution(
    id_tag="S-5",
    name="Mission Briefing Generator",
    satisfies=[goal_context_slicing],
    requires=[sol_core_validation],
    constraints={
        "output_format": "Markdown",
        "context_size": "50-200 lines",
        "includes": "Goals, Constraints, Required Output",
        "test": "../test_cli.py",
        "llm_review": "claude",
    },
    description="""Slices architecture graph to extract focused context for specific Implementation.
Outputs Markdown with Goals (why), Constraints (boundaries), and Required Output
(files and symbols). Context size: 50-200 lines instead of thousands, enabling
efficient AI agent coordination. Requires core validation to understand graph
structure. This enables "context slicing" where agents receive minimal focused
briefing rather than entire codebase context.""",
)

# ============================================================================
# IMPLEMENTATIONS (The Reality)
# ============================================================================

impl_core_validation = Implementation(
    id_tag="I-1",
    name="Core Validation Implementation",
    implements=sol_core_validation,
    code_files=["../archlib/validation.py", "../archlib/architecture.py"],
    test_files=["../test_basic.py"],
    must_define={
        "../archlib/validation.py": [
            "validate_traceability",
            "validate_dependencies",
            "validate_code_inventory",
            "validate_test_inventory",
        ],
        "../archlib/architecture.py": ["Architecture"],
    },
    description="""Implements the four validation functions: validate_traceability checks Implementation
→ Solution → Goal chains, validate_dependencies detects cycles and broken references,
validate_code_inventory performs bidirectional AST parsing, validate_test_inventory
confirms test files exist. Architecture class orchestrates these checks and provides
CLI interface. Module structure (validation.py, architecture.py, parsing/) separates
concerns enabling independent evolution and clear architectural boundaries, matching
the mental model where Implementations map to specific modules rather than monolithic files.""",
)

impl_python_ast = Implementation(
    id_tag="I-2",
    name="Python AST Parser Implementation",
    implements=sol_python_ast,
    code_files=["../archlib/parsing/python.py"],
    test_files=["../test_basic.py"],
    must_define={
        "../archlib/parsing/python.py": [
            "extract_python_symbols",
            "extract_test_functions_python",
        ]
    },
    description="""extract_python_symbols() walks AST using built-in ast module, extracting ClassDef
nodes for classes, FunctionDef/AsyncFunctionDef for functions, and top-level
Assign/AnnAssign for globals. extract_test_functions_python() finds pytest-style
test functions (test_* prefix). Handles nested structures, decorators, type hints.
This is the reference parser implementation that other language parsers emulate.""",
)

impl_javascript_ast = Implementation(
    id_tag="I-3",
    name="JavaScript AST Parser Implementation",
    implements=sol_javascript_ast,
    code_files=["../archlib/parsing/javascript.py"],
    test_files=[],
    must_define={
        "../archlib/parsing/javascript.py": [
            "extract_javascript_symbols",
            "_parse_with_treesitter",
            "_parse_javascript_with_regex",
            "extract_test_functions_javascript",
        ]
    },
    description="""extract_javascript_symbols() tries tree-sitter first via _parse_with_treesitter(),
falls back to regex via _parse_javascript_with_regex() if tree-sitter unavailable.
Handles ES6 classes, function declarations, arrow functions, async functions,
module exports (CommonJS and ES6). extract_test_functions_javascript() finds
test/it function calls with string literals. Graceful degradation ensures archlib
works without tree-sitter while preferring proper AST parsing when available.""",
)

impl_cli_interface = Implementation(
    id_tag="I-4",
    name="CLI Interface Implementation",
    implements=sol_cli_interface,
    code_files=["../archlib/architecture.py"],
    test_files=["../test_cli.py"],
    must_define={"../archlib/architecture.py": ["Architecture"]},
    description="""Architecture.cli() sets up argparse with subparsers for validate, spec, and test
commands. Architecture.validate() runs all checks and exits with error code.
Architecture.generate_spec() creates mission briefing markdown. Architecture.run_tests()
dispatches to pytest. The CLI transforms architecture.py from passive file into
active project control plane that orchestrates development workflows.""",
)

impl_spec_generator = Implementation(
    id_tag="I-5",
    name="Spec Generator Implementation",
    implements=sol_spec_generator,
    code_files=["../archlib/architecture.py"],
    test_files=["../test_cli.py"],
    must_define={"../archlib/architecture.py": ["Architecture"]},
    description="""Architecture.generate_spec() takes Implementation ID, extracts its Solution and
satisfied Goals, formats as Markdown mission briefing. Output includes Goals
(why), Constraints (boundaries), and Required Output (files and symbols).
This enables "context slicing" where AI agents receive 50-200 line focused
briefing instead of thousands of lines of codebase context.""",
)

impl_node_classes = Implementation(
    id_tag="I-6",
    name="Node Classes Implementation",
    implements=sol_core_validation,
    code_files=["../archlib/nodes.py"],
    test_files=["../test_basic.py"],
    must_define={"../archlib/nodes.py": ["Node", "Goal", "Solution", "Implementation"]},
    description="""Defines the four core node classes: Node (base), Goal (business objectives),
Solution (architectural strategies), Implementation (code artifacts). These
classes form the metamodel that projects instantiate to define their architecture.
Node classes are simple data containers with id, name, and relationship fields
(satisfies, requires, implements). The Architecture class validates collections
of these nodes to ensure architectural integrity.""",
)

# ============================================================================
# ARCHITECTURE
# ============================================================================

if __name__ == "__main__":
    arch = Architecture(
        goals=[
            goal_executable_architecture,
            goal_multi_language_support,
            goal_cli_tooling,
            goal_context_slicing,
        ],
        solutions=[
            sol_core_validation,
            sol_python_ast,
            sol_javascript_ast,
            sol_cli_interface,
            sol_spec_generator,
        ],
        implementations=[
            impl_core_validation,
            impl_python_ast,
            impl_javascript_ast,
            impl_cli_interface,
            impl_spec_generator,
            impl_node_classes,
        ],
    )
    arch.cli()
