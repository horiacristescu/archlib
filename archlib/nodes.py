"""Core node classes for architectural modeling."""

from typing import Any, Dict, List


class Node:
    """Base class for all architectural nodes."""

    def __init__(self, id_tag: str, name: str):
        self.id = id_tag
        self.name = name

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r})"


class Goal(Node):
    """The Why & What. Defines a business objective with acceptance test."""

    def __init__(
        self, id_tag: str, name: str, acceptance_test: str, description: str = ""
    ):
        super().__init__(id_tag, name)
        self.acceptance_test = acceptance_test
        self.description = description


class Solution(Node):
    """The How. Defines architectural strategy with constraints and dependencies."""

    def __init__(
        self,
        id_tag: str,
        name: str,
        satisfies: List["Goal"],
        requires: List["Solution"] = None,
        constraints: Dict[str, Any] = None,
        description: str = "",
    ):
        super().__init__(id_tag, name)
        self.satisfies = satisfies or []
        self.requires = requires or []
        self.constraints = constraints or {}
        self.description = description


class Implementation(Node):
    """The Reality. Declares physical code artifacts with symbol requirements."""

    def __init__(
        self,
        id_tag: str,
        name: str,
        implements: Solution,
        code_files: List[str],
        test_files: List[str] = None,
        must_define: Dict[str, List[str]] = None,
        description: str = "",
    ):
        super().__init__(id_tag, name)
        self.implements = implements
        self.code_files = code_files or []
        self.test_files = test_files or []
        self.must_define = must_define or {}
        self.description = description




