from typing import Any
from langgraph.graph import StateGraph, START, END
from src.application.workflows.interfaces import WorkflowDefinition, NodeRegistry, CheckpointStore
from src.application.workflows.state import RecruitingWorkflowState
from src.infrastructure.workflows.nodes.factory import create_service_node

class RecruitingLangGraphDefinition(WorkflowDefinition):
    def __init__(self, node_registry: NodeRegistry):
        self.name = "resume_extraction_workflow"
        self.version = "1.0.0"
        self.registry = node_registry

    def compile(self, checkpointer: CheckpointStore = None) -> Any:
        workflow = StateGraph(RecruitingWorkflowState)

        # Define all nodes
        nodes = [
            "UploadValidationNode",
            "DocumentParsingNode",
            "AIExtractionNode",
            "CandidateValidationNode",
            "ProfileEvaluationNode",
            "HumanApprovalNode",
            "EmbeddingGenerationNode",
            "CandidateMatchingNode",
            "PersistResultsNode",
            "WorkflowCompletedNode",
            "WorkflowFailedNode"
        ]

        # Add nodes to graph
        for node_name in nodes:
            node_impl = self.registry.get_node(node_name)
            workflow.add_node(node_name, node_impl.execute)

        # Routing Logic
        workflow.add_edge(START, "UploadValidationNode")
        
        # We need conditional routing here. Since it's Sprint 8 we'll mock the edges for the skeleton.
        # In a real setup, these use conditional functions reading state.
        def validate_routing(state: RecruitingWorkflowState):
            if state.get("errors"):
                return "WorkflowFailedNode"
            return "DocumentParsingNode"

        workflow.add_conditional_edges("UploadValidationNode", validate_routing)
        workflow.add_edge("DocumentParsingNode", "AIExtractionNode")
        workflow.add_edge("AIExtractionNode", "CandidateValidationNode")
        workflow.add_edge("CandidateValidationNode", "ProfileEvaluationNode")
        
        def evaluation_routing(state: RecruitingWorkflowState):
            eval_result = state.get("evaluation_result", {})
            confidence = eval_result.get("confidence_score", 1.0)
            # Threshold could be config driven
            if confidence < 0.8:
                return "HumanApprovalNode"
            return "EmbeddingGenerationNode"
            
        workflow.add_conditional_edges("ProfileEvaluationNode", evaluation_routing)
        
        def human_routing(state: RecruitingWorkflowState):
            if state.get("workflow_status") == "CANCELLED":
                return "WorkflowFailedNode"
            return "EmbeddingGenerationNode"
            
        workflow.add_conditional_edges("HumanApprovalNode", human_routing)
        
        workflow.add_edge("EmbeddingGenerationNode", "CandidateMatchingNode")
        workflow.add_edge("CandidateMatchingNode", "PersistResultsNode")
        workflow.add_edge("PersistResultsNode", "WorkflowCompletedNode")
        workflow.add_edge("WorkflowCompletedNode", END)
        workflow.add_edge("WorkflowFailedNode", END)

        return workflow.compile(checkpointer=checkpointer)
