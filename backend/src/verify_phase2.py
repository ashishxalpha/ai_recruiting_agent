import asyncio
import os
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from sqlalchemy.pool import NullPool

from src.infrastructure.workflows.langgraph_engine import LangGraphWorkflowEngine
from src.infrastructure.workflows.checkpoints.database import DatabaseCheckpointStore
from src.application.workflows.workflow_registry import InMemoryWorkflowDefinitionRegistry
from src.infrastructure.database.models import WorkflowExecutionModel
from src.application.workflows.interfaces import WorkflowNode, NodeRetryPolicy
from src.application.workflows.state import RecruitingWorkflowState
from src.application.workflows.interfaces import WorkflowDefinition
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://copilot:copilot_password@localhost:5432/ai_recruiting")

# We create a dummy test workflow
class TestWorkflowDefinition(WorkflowDefinition):
    def __init__(self, node_registry):
        self.name = "test_workflow"
        self.version = "1.0.0"
        self.registry = node_registry
        self.configuration = {}
        self.supported_states = ["RUNNING", "PAUSED", "COMPLETED", "FAILED"]
        self.required_capabilities = []

    def compile(self, checkpointer=None):
        workflow = StateGraph(RecruitingWorkflowState)
        
        node_1 = self.registry.get_node("Node1")
        node_2 = self.registry.get_node("Node2")
        
        workflow.add_node("Node1", node_1.execute)
        
        from langgraph.types import RetryPolicy
        pol = node_2.retry_policy
        workflow.add_node("Node2", node_2.execute, retry=RetryPolicy(
            initial_interval=pol.backoff_multiplier,
            backoff_factor=pol.backoff_multiplier,
            max_attempts=pol.max_attempts,
            retry_on=lambda exc: type(exc) in pol.retry_on_exceptions
        ))
        
        workflow.add_edge(START, "Node1")
        workflow.add_edge("Node1", "Node2")
        workflow.add_edge("Node2", END)
        
        return workflow.compile(checkpointer=checkpointer)

class MockNodeRegistry:
    class Node1(WorkflowNode):
        @property
        def retry_policy(self): return None
        async def execute(self, state):
            # We interrupt here to test pause/resume
            val = interrupt({"action": "wait"})
            state["candidate_document_id"] = val.get("injected_val")
            return state
        async def rollback(self, state): return state

    class Node2(WorkflowNode):
        class TestRetryPolicy(NodeRetryPolicy):
            max_attempts = 2
            backoff_multiplier = 0.1
            retry_on_exceptions = [ValueError]
        
        def __init__(self):
            self.attempts = 0
            
        @property
        def retry_policy(self): return self.TestRetryPolicy()
        
        async def execute(self, state):
            self.attempts += 1
            if self.attempts < 2:
                raise ValueError("Simulated temporary failure")
            state["job_id"] = "success_after_retry"
            return state
            
        async def rollback(self, state): return state

    def __init__(self):
        self.n1 = self.Node1()
        self.n2 = self.Node2()
        
    def get_node(self, name):
        if name == "Node1": return self.n1
        if name == "Node2": return self.n2

async def test_engine():
    engine = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)
    AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        checkpointer = DatabaseCheckpointStore(session)
        registry = InMemoryWorkflowDefinitionRegistry()
        node_registry = MockNodeRegistry()
        registry.register(TestWorkflowDefinition(node_registry))
        
        workflow_engine = LangGraphWorkflowEngine(registry, checkpointer, session)
        
        # Start Execution
        initial_state = {
            "workflow_id": str(uuid.uuid4()),
            "candidate_document_id": str(uuid.uuid4())
        }
        print("Starting workflow execution...")
        result_state = await workflow_engine.execute("test_workflow", initial_state)
        
        # It should pause at Node1 due to interrupt
        print(f"State after start (should be paused): {result_state}")
        
        # Check Execution Record
        res = await session.execute(text(f"SELECT id, status, current_node FROM workflow_executions WHERE thread_id = '{initial_state['workflow_id']}'"))
        record = res.fetchone()
        execution_id = record[0]
        print(f"Execution Record Status: {record[1]} at node: {record[2]}")
        assert record[1] == "PAUSED"
        assert record[2] == "Node1"
        
        # Resume Execution
        print("Resuming workflow execution...")
        final_state = await workflow_engine.resume(execution_id, {"injected_val": "resumed_val"})
        print(f"State after resume (should be completed): {final_state}")
        assert final_state["candidate_document_id"] == "resumed_val"
        assert final_state["job_id"] == "success_after_retry"
        
        res = await session.execute(text(f"SELECT status FROM workflow_executions WHERE id = '{execution_id}'"))
        record = res.fetchone()
        assert record[0] == "COMPLETED"
        
        print("All Phase 2 Engine Tests Passed!")

if __name__ == "__main__":
    asyncio.run(test_engine())
