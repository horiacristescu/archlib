# Executable Architecture

This methodology shifts the role of the software architect from a documentarian to a legislator. Instead of writing static text files that rot over time, you will now write an executable Python specification—`architecture.py`—that defines the physics, laws, and labor of your project. This file acts as the **single source of truth**, replacing all other documentation (including MIND_MAP.md), enforcing logical consistency between your business goals (`Intent`), your constraints (`Requirements`), your technical solutions (`Design`), your actual code (`Tasks`), and your resource budgets. If the architecture is invalid (e.g., a Task exists without a Requirement, a Design misses a dependency, or code files don't match the ledger), the script will fail to compile, preventing architectural debt before it starts.

## The Complete Accounting System

Architecture.py provides complete bidirectional accountability:

- **Code Inventory**: Every Python file, class, function, and global variable must be declared in a Task node. The validator parses the filesystem AST to confirm declared symbols exist at specified locations and that no undeclared code exists.

- **Test Inventory**: Every test file and test function must be declared. The validator confirms test files exist at specified paths with declared test functions present.

- **Dependency Resolution**: The `requires` field forces explicit dependency declarations. The validator traces the dependency graph to detect missing dependencies, circular dependencies, and conflicts.

- **Resource Accounting**: Designs declare estimated resource budgets (CPU, memory, storage, network, security overhead). After implementation, measured constraints propagate up the hierarchy, forcing reconciliation when reality exceeds estimates.

- **Traceability Enforcement**: Every Task must trace through Design → Requirement → Intent. Orphaned work gets rejected. Unimplemented Requirements get flagged.

- **Conflict Detection**: Incompatible designs are caught at architecture time through explicit `conflicts_with` declarations and constraint incompatibility checks.

## The Constitutional Metamodel

You begin every project by establishing the "Constitution." This is the boilerplate Python code that defines the types of nodes in your system and the rules of their interaction. Copy this into the top of your `architecture.py` file.

```python
from dataclasses import dataclass
from typing import List, Type, Optional, Dict
import ast
import os

@dataclass
class ResourceConstraints:
    """Standardized resource categories for budget tracking."""
    # Compute
    cpu_cores: float = 0
    cpu_percent: float = 0
    latency_p99_ms: float = 0
    
    # Memory
    memory_mb: float = 0
    memory_peak_mb: float = 0
    
    # Storage
    storage_gb: float = 0
    iops: int = 0
    
    # Network
    bandwidth_mbps: float = 0
    connections_max: int = 0
    request_rate: int = 0
    
    # Access
    auth_overhead_ms: float = 0
    max_concurrent_users: int = 0
    
    # Security
    encryption_overhead_ms: float = 0
    key_rotation_interval_hours: int = 0

class Node:
    def __init__(self, id_tag: str, name: str):
        self.id = id_tag
        self.name = name

class Intent(Node):
    """The 'Why'. Immutable business goals.
    
    Use docstrings to explain business context, user needs, and strategic direction.
    These are your axioms - everything else derives from these.
    """
    pass

class Requirement(Node):
    """The 'What'. Derived from Intent.
    
    Use docstrings to explain how this requirement serves the parent Intent,
    what constraints it imposes, and why alternative approaches were rejected.
    """
    def __init__(self, id_tag: str, name: str, derived_from: List[Type[Intent]]):
        super().__init__(id_tag, name)
        self.derived_from = derived_from

class Design(Node):
    """The 'How'. Satisfies Requirements, Requires other Designs.
    
    Use docstrings to document:
    - Architecture decisions and tradeoffs
    - Why this approach over alternatives
    - Performance characteristics and constraints
    - Integration points and dependencies
    """
    def __init__(self, id_tag: str, name: str, 
                 satisfies: List[Type[Requirement]], 
                 requires: List[Type['Design']] = None,
                 conflicts_with: List[Type['Design']] = None,
                 estimated: ResourceConstraints = None,
                 measured: ResourceConstraints = None):
        super().__init__(id_tag, name)
        self.satisfies = satisfies
        self.requires = requires or []
        self.conflicts_with = conflicts_with or []
        self.estimated = estimated or ResourceConstraints()
        self.measured = measured or ResourceConstraints()

class Task(Node):
    """The 'Do'. Implements a Design.
    
    Declares the exact filesystem location and symbols that must exist.
    The validator will parse the AST to confirm all declared symbols are present.
    """
    def __init__(self, id_tag: str, name: str, 
                 implements: Type[Design],
                 file_path: str,
                 classes: List[str] = None,
                 functions: List[str] = None,
                 globals: List[str] = None):
        super().__init__(id_tag, name)
        self.implements = implements
        self.file_path = file_path
        self.classes = classes or []
        self.functions = functions or []
        self.globals = globals or []

class Test(Node):
    """The 'Judge'. Verifies compliance.
    
    Declares test file location and test functions that must exist.
    """
    pass

# The 4 Levels of the Judiciary
class UserAcceptanceTest(Test):
    """Verifies Intent is achieved from user perspective."""
    def __init__(self, id_tag: str, name: str, 
                 verifies: Type[Intent],
                 test_file: str,
                 test_functions: List[str]):
        super().__init__(id_tag, name)
        self.verifies = verifies
        self.test_file = test_file
        self.test_functions = test_functions

class SystemTest(Test):
    """Verifies Requirement is satisfied end-to-end."""
    def __init__(self, id_tag: str, name: str, 
                 verifies: Type[Requirement],
                 test_file: str,
                 test_functions: List[str]):
        super().__init__(id_tag, name)
        self.verifies = verifies
        self.test_file = test_file
        self.test_functions = test_functions

class IntegrationTest(Test):
    """Verifies Design dependencies integrate correctly."""
    def __init__(self, id_tag: str, name: str, 
                 verifies: Type[Design],
                 test_file: str,
                 test_functions: List[str]):
        super().__init__(id_tag, name)
        self.verifies = verifies
        self.test_file = test_file
        self.test_functions = test_functions

class UnitTest(Test):
    """Verifies Design component logic in isolation."""
    def __init__(self, id_tag: str, name: str, 
                 verifies: Type[Design],
                 test_file: str,
                 test_functions: List[str]):
        super().__init__(id_tag, name)
        self.verifies = verifies
        self.test_file = test_file
        self.test_functions = test_functions
```

## Phase 1: Legislating Intent and Requirements

Your first job is not to look at code, but to look at value. Define `Intent` classes that represent the non-negotiable goals of the project. Then, derive `Requirement` classes from these Intents. This enforces the rule that no requirement can be arbitrary - if you cannot find an Intent to justify a Requirement, you have discovered scope creep and must delete it.

Use docstrings extensively to capture your architectural thinking. This is where MIND_MAP.md's conceptual content now lives.

```python
# Level 1: Intent
class IntentSecureData(Intent):
    """[I-1] User data must never be exposed to third parties.
    
    Privacy is a core competitive advantage in our market. Users
    trust us with sensitive information, and any breach would be
    catastrophic both legally and reputationally. This intent drives
    our encryption, access control, and audit logging requirements.
    """

class IntentResponsiveUX(Intent):
    """[I-2] Users expect instant feedback in collaborative features.
    
    Our user research shows that perceived latency over 100ms breaks
    the collaborative flow. This drives our real-time architecture
    decisions and rules out traditional request/response patterns for
    interactive features.
    """

# Level 2: Requirement
class ReqEncryptionAtRest(Requirement):
    """[R-1] All database volumes must be encrypted.
    
    Satisfies IntentSecureData by ensuring that even if physical media
    is compromised, data remains protected. We use AES-256 encryption
    with keys managed through AWS KMS.
    """
    def __init__(self): 
        super().__init__("[R-1]", "DB Encryption", 
                        derived_from=[IntentSecureData])

class ReqRealTimeChat(Requirement):
    """[R-3] Messages must appear within 100ms of send.
    
    Satisfies IntentResponsiveUX. HTTP polling cannot meet this target.
    WebSocket maintains persistent connection for instant delivery.
    Scaling implications are handled by DesignRedisCluster.
    """
    def __init__(self):
        super().__init__("[R-3]", "Real-time messaging",
                        derived_from=[IntentResponsiveUX])
```

## Phase 2: Architectural Negotiation

Now you define the `Design` layer. This is where you use the Python class structure to model the dependency graph explicitly. Use the `requires` list to declare dependencies, `conflicts_with` to flag incompatible designs, and `estimated` to declare resource budgets.

```python
# Level 3: Design
class DesignRedis(Design):
    """[D-1] Redis Cache for Pub/Sub and session storage.
    
    Provides in-memory pub/sub for WebSocket message distribution
    across instances. Also handles session persistence for sticky
    load balancing.
    
    Estimated constraints assume t3.medium instance. Actual production
    load may require tuning.
    """
    def __init__(self): 
        super().__init__(
            "[D-1]", "Redis Cache", 
            satisfies=[],  # Infrastructure - required by others
            estimated=ResourceConstraints(
                cpu_cores=1,
                memory_mb=512,
                connections_max=1000,
                latency_p99_ms=5
            )
        )

class DesignStatelessAPI(Design):
    """[D-4] RESTful stateless endpoints for horizontal scaling.
    
    All state stored in database or Redis. No server-side session state.
    Enables unlimited horizontal scaling through standard load balancing.
    """
    def __init__(self):
        super().__init__(
            "[D-4]", "Stateless REST API",
            satisfies=[],
            estimated=ResourceConstraints(
                cpu_cores=2,
                memory_mb=1024
            )
        )

class DesignWebSocket(Design):
    """[D-2] Socket.io server with sticky session load balancing.
    
    Maintains persistent connections per user. Requires Redis for
    cross-instance message routing. Uses sticky sessions to keep
    user connections on same instance.
    
    CONFLICTS with DesignStatelessAPI because WebSocket connections
    are inherently stateful. If both real-time and stateless patterns
    are needed, they must run on separate service endpoints.
    
    Performance: 850 concurrent connections per instance, 12ms p99 latency.
    """
    def __init__(self): 
        super().__init__(
            "[D-2]", "WebSocket Server", 
            satisfies=[ReqRealTimeChat],
            requires=[DesignRedis],
            conflicts_with=[DesignStatelessAPI],
            estimated=ResourceConstraints(
                cpu_cores=2,
                memory_mb=2048,
                connections_max=1000,
                latency_p99_ms=15
            )
        )
```

## Phase 3: The Judiciary (4-Level Testing)

Before you assign Tasks, establish the Court. Define a `Test` node for every level of the hierarchy. Declare the exact test file paths and test function names that must exist.

```python
# Level 4: The Judiciary
class TestChatUAT(UserAcceptanceTest):
    """[UAT-1] Verify user can send/receive messages in real-time."""
    def __init__(self): 
        super().__init__(
            "[UAT-1]", "Chat Flow UAT", 
            verifies=IntentResponsiveUX,
            test_file="tests/acceptance/test_chat_flow.py",
            test_functions=["test_user_sends_message", "test_user_receives_message"]
        )

class TestRedisIntegration(IntegrationTest):
    """[IT-1] Verify WebSocket server connects to Redis and routes messages."""
    def __init__(self): 
        super().__init__(
            "[IT-1]", "Redis Integration", 
            verifies=DesignWebSocket,
            test_file="tests/integration/test_websocket_redis.py",
            test_functions=["test_redis_connection", "test_message_routing"]
        )

class TestRedisUnit(UnitTest):
    """[UT-1] Verify Redis client handles connection failures gracefully."""
    def __init__(self):
        super().__init__(
            "[UT-1]", "Redis Client Unit Tests",
            verifies=DesignRedis,
            test_file="tests/unit/test_redis_client.py",
            test_functions=["test_reconnect_on_failure", "test_connection_pooling"]
        )
```

## Phase 4: Task Implementation Ledger

Tasks declare the exact code that must exist. The validator will parse each file's AST to confirm declared symbols are present.

```python
# Level 5: Tasks
class TaskRedisImplementation(Task):
    """[T-1] Implement Redis client with connection pooling."""
    def __init__(self):
        super().__init__(
            "[T-1]", "Redis Client Implementation",
            implements=DesignRedis,
            file_path="src/cache/redis_client.py",
            classes=["RedisClient", "ConnectionPool"],
            functions=["connect", "disconnect", "get", "set", "publish", "subscribe"],
            globals=["DEFAULT_POOL_SIZE", "MAX_RETRIES"]
        )

class TaskWebSocketServer(Task):
    """[T-2] Implement WebSocket server with Socket.io."""
    def __init__(self):
        super().__init__(
            "[T-2]", "WebSocket Server",
            implements=DesignWebSocket,
            file_path="src/websocket/server.py",
            classes=["WebSocketServer", "MessageHandler"],
            functions=["start_server", "handle_connection", "broadcast_message"]
        )
```

## Phase 5: Post-Implementation Measurement

After implementation, agents run benchmarks and update measured constraints:

```python
# After TaskRedisImplementation completes and benchmarks run:
DesignRedis.measured = ResourceConstraints(
    cpu_cores=1.8,           # Actually needs more CPU than estimated
    memory_mb=1800,          # Uses 3.5x estimated memory
    memory_peak_mb=2100,
    connections_max=850,      # Slightly below estimate
    latency_p99_ms=12,       # Within acceptable range
    encryption_overhead_ms=3
)
```

## Phase 6: The Compiler (Validation Script)

The validation script performs complete bidirectional reconciliation:

```python
def validate_architecture(intents, requirements, designs, tasks, tests):
    """
    Complete architectural validation:
    
    1. TRACEABILITY
       - Every Task traces through Design → Requirement → Intent
       - Every Requirement has at least one Design
       - Every Design has at least one Task
    
    2. DEPENDENCIES
       - All Design.requires dependencies are instantiated
       - No circular dependencies exist
       - No conflicting designs are both instantiated
    
    3. CODE INVENTORY
       - Every Task.file_path exists in filesystem
       - Every declared class/function/global exists in the file's AST
       - No Python files exist that lack corresponding Tasks
    
    4. TEST INVENTORY
       - Every Test.test_file exists in filesystem
       - Every declared test function exists in the test file
       - Every Design has Unit and Integration tests
       - Every Requirement has System tests
       - Every Intent has UAT tests
    
    5. RESOURCE CONSTRAINTS
       - Aggregate measured constraints from child Designs
       - Check if totals exceed parent budgets
       - Propagate violations up to Requirement level
       - Report which Intents become infeasible
    
    6. CONFLICT DETECTION
       - Check Design.conflicts_with declarations
       - Check constraint key incompatibilities
       - Trace conflict chains to show Intent divergence
    """
    
    print("🏛️  Running Architectural Compiler...")
    print("\n" + "="*60)
    
    errors = []
    warnings = []
    
    # 1. Validate Traceability
    errors.extend(validate_traceability(tasks, designs, requirements, intents))
    
    # 2. Validate Dependencies
    errors.extend(validate_dependencies(designs))
    errors.extend(validate_conflicts(designs))
    
    # 3. Validate Code Inventory
    errors.extend(validate_code_inventory(tasks))
    
    # 4. Validate Test Inventory
    errors.extend(validate_test_inventory(tests, designs, requirements, intents))
    
    # 5. Validate Resource Constraints
    warnings.extend(validate_resource_budgets(designs, requirements))
    
    # 6. Generate Reports
    if errors:
        print("\n❌ COMPILATION FAILED")
        for error in errors:
            print(f"   {error}")
        return False
    
    if warnings:
        print("\n⚠️  WARNINGS")
        for warning in warnings:
            print(f"   {warning}")
    
    print("\n✅ ARCHITECTURE VALIDATED")
    print("   All dependencies satisfied")
    print("   All code matches ledger")
    print("   All tests present")
    print("="*60)
    return True

def validate_code_inventory(tasks):
    """Bidirectional code validation."""
    errors = []
    
    # Top-down: declared must exist
    for task in tasks:
        if not os.path.exists(task.file_path):
            errors.append(f"Missing file: {task.file_path} (declared in {task.id})")
            continue
        
        with open(task.file_path) as f:
            tree = ast.parse(f.read())
        
        actual_classes = {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}
        actual_functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        actual_globals = {node.targets[0].id for node in ast.walk(tree) 
                         if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)}
        
        missing_classes = set(task.classes) - actual_classes
        missing_functions = set(task.functions) - actual_functions
        missing_globals = set(task.globals) - actual_globals
        
        if missing_classes:
            errors.append(f"{task.file_path}: Missing classes {missing_classes}")
        if missing_functions:
            errors.append(f"{task.file_path}: Missing functions {missing_functions}")
        if missing_globals:
            errors.append(f"{task.file_path}: Missing globals {missing_globals}")
    
    # Bottom-up: existing must be declared
    declared_files = {task.file_path for task in tasks}
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                if filepath not in declared_files:
                    errors.append(f"Undeclared file: {filepath} (not in architecture.py)")
    
    return errors

def validate_resource_budgets(designs, requirements):
    """Check if measured constraints exceed estimates and propagate."""
    warnings = []
    
    for design in designs:
        if not design.measured or not design.estimated:
            continue
        
        # Check individual design violations
        if design.measured.memory_mb > design.estimated.memory_mb * 1.5:
            warnings.append(
                f"{design.name}: Memory {design.measured.memory_mb}MB "
                f"exceeds estimate {design.estimated.memory_mb}MB"
            )
        
        # Aggregate children and check parent budget
        total = ResourceConstraints()
        for dep in design.requires:
            if dep.measured:
                total.cpu_cores += dep.measured.cpu_cores
                total.memory_mb += dep.measured.memory_mb
                # ... aggregate other constraints
        
        if total.memory_mb > design.estimated.memory_mb:
            warnings.append(
                f"{design.name}: Children require {total.memory_mb}MB, "
                f"budget is {design.estimated.memory_mb}MB"
            )
    
    return warnings

# Run validation when architecture.py executes
if __name__ == "__main__":
    # Instantiate all nodes
    intents = [IntentSecureData(), IntentResponsiveUX()]
    requirements = [ReqEncryptionAtRest(), ReqRealTimeChat()]
    designs = [DesignRedis(), DesignWebSocket()]
    tasks = [TaskRedisImplementation(), TaskWebSocketServer()]
    tests = [TestChatUAT(), TestRedisIntegration(), TestRedisUnit()]
    
    # Validate
    validate_architecture(intents, requirements, designs, tasks, tests)
```

## Benefits Summary

**Complete Accountability** - Every symbol traces from Intent to implementation. No orphans, no undocumented code.

**Explicit Dependencies** - The `requires` field makes implicit dependencies explicit and queryable.

**Conflict Detection** - Incompatible designs surface before implementation, forcing architectural decisions.

**Resource Reconciliation** - Measured reality forces budget updates when estimates are wrong.

**Dependency Visibility** - Adding "remember user state" reveals the full cascade it triggers.

**Test Coverage Enforcement** - Every level must have corresponding tests at declared locations.

**Agent Coordination** - Multiple coding agents query the same ledger to coordinate work.

**Single Source of Truth** - Replaces MIND_MAP.md and all other documentation. Architecture.py is both map and territory validator.