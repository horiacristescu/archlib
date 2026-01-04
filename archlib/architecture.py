"""Architecture class - the compiler and CLI orchestrator."""

import argparse
import subprocess
import sys
from typing import List

from .nodes import Goal, Implementation, Solution
from .validation import (
    validate_code_inventory,
    validate_dependencies,
    validate_test_inventory,
    validate_traceability,
)


class Architecture:
    """The Compiler and CLI Tool. Orchestrates validation and commands."""

    def __init__(
        self,
        goals: List[Goal],
        solutions: List[Solution],
        implementations: List[Implementation],
    ):
        self.goals = goals
        self.solutions = solutions
        self.implementations = implementations

    def validate(self) -> bool:
        """Run full architectural validation. Returns True if valid, exits on failure."""
        print("🏛️  Running Architecture Compiler...")
        print("\n" + "=" * 60)

        errors = []
        warnings = []

        # Run all validation checks
        errors.extend(
            validate_traceability(self.implementations, self.solutions, self.goals)
        )
        errors.extend(validate_dependencies(self.solutions))
        errors.extend(validate_code_inventory(self.implementations, self.goals))
        errors.extend(validate_test_inventory(self.goals, self.implementations))

        # Report results
        if errors:
            print("\n❌ ARCHITECTURE FAILED:")
            for error in errors:
                print(f"   {error}")
            print("=" * 60)
            sys.exit(1)

        if warnings:
            print("\n⚠️  WARNINGS:")
            for warning in warnings:
                print(f"   {warning}")

        print("\n✅ ARCHITECTURE VALIDATED")
        print("   All dependencies satisfied")
        print("   All code files declared")
        print("   All test files declared")
        print("=" * 60)
        return True

    def generate_spec(self, impl_id: str) -> str:
        """Generate mission briefing markdown for an Implementation ID."""
        impl = next((i for i in self.implementations if i.id == impl_id), None)
        if not impl:
            return f"❌ Implementation {impl_id} not found"

        sol = impl.implements

        output = []
        output.append(f"# ⚔️ Mission Briefing: {impl.name}")
        output.append(f"> **Context**: Implementing solution '{sol.name}'")
        if impl.description:
            output.append("")
            output.append(f"{impl.description}")
        output.append("")
        output.append("## 1. Goals (The Why)")
        for goal in sol.satisfies:
            output.append(f"- **{goal.name}** (Verify via `{goal.acceptance_test}`)")
            if goal.description:
                output.append(f"  {goal.description}")
        output.append("")
        output.append("## 2. Solution Context")
        if sol.description:
            output.append(f"{sol.description}")
            output.append("")
        output.append("## 3. Constraints (The Boundaries)")
        if sol.constraints:
            for k, v in sol.constraints.items():
                output.append(f"- **{k}**: `{v}`")
        else:
            output.append("- No constraints specified")
        output.append("")
        output.append("## 4. Required Output")
        output.append("Modify/Create these files:")
        for f in impl.code_files:
            output.append(f"- `{f}`")
        if impl.must_define:
            output.append("")
            output.append("Ensure these symbols exist:")
            for f, syms in impl.must_define.items():
                output.append(f"- `{f}`: {', '.join(syms)}")

        return "\n".join(output)

    def run_tests(self, node_id: str) -> None:
        """Run tests for a Goal or Implementation node."""
        # Try Implementation first
        target = next((i for i in self.implementations if i.id == node_id), None)
        if target:
            files = target.test_files
        else:
            # Try Goal
            target = next((g for g in self.goals if g.id == node_id), None)
            if target:
                files = [target.acceptance_test]
            else:
                print(f"❌ Node {node_id} not found.")
                return

        if not files:
            print(f"❌ Node {node_id} has no test files.")
            return

        print(f"🧪 Running tests for {node_id}...")
        cmd = ["pytest"] + files
        subprocess.run(cmd)

    def cli(self) -> None:
        """Entry point for command-line interface."""
        parser = argparse.ArgumentParser(
            description="Executable Architecture Compiler and CLI"
        )
        subparsers = parser.add_subparsers(dest="action", help="Command to run")

        # Validate command
        subparsers.add_parser("validate", help="Validate architecture")

        # Spec command
        spec_parser = subparsers.add_parser("spec", help="Generate mission briefing")
        spec_parser.add_argument("--id", required=True, help="Implementation ID")

        # Test command
        test_parser = subparsers.add_parser("test", help="Run tests for a node")
        test_parser.add_argument(
            "--id", required=True, help="Node ID (Goal or Implementation)"
        )

        args = parser.parse_args()

        if args.action == "validate":
            self.validate()
        elif args.action == "spec":
            print(self.generate_spec(args.id))
        elif args.action == "test":
            self.run_tests(args.id)
        else:
            # Default to validate if no action specified
            self.validate()


