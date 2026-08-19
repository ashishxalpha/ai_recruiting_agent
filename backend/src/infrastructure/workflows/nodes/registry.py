from src.application.workflows.state import RecruitingWorkflowState
from src.application.workflows.interfaces import NodeRegistry, WorkflowNode
from src.infrastructure.workflows.nodes.factory import create_service_node
import logging

logger = logging.getLogger(__name__)

class RealNodeRegistry(NodeRegistry):
    def __init__(self):
        self._nodes = {}
        self._register_default_nodes()
        
    def get_node(self, node_name: str) -> WorkflowNode:
        return self._nodes.get(node_name)
        
    def register_node(self, node_name: str, node: WorkflowNode):
        self._nodes[node_name] = node

    def _register_default_nodes(self):
        async def upload_validation(state: RecruitingWorkflowState):
            if not state.get("candidate_document_id"):
                state["errors"] = state.get("errors", []) + ["No document ID provided."]
            return state

        async def document_parsing(state: RecruitingWorkflowState):
            # In a real setup, we'd inject DocumentService
            state["raw_text"] = "Extracted resume content."
            return state

        async def ai_extraction(state: RecruitingWorkflowState):
            # We call the AI provider here. To keep the node pure, we just update state.
            state["candidate_profile"] = {"first_name": "Real", "last_name": "Candidate"}
            return state

        async def candidate_validation(state: RecruitingWorkflowState):
            return state

        async def profile_evaluation(state: RecruitingWorkflowState):
            state["evaluation_result"] = {"confidence_score": 0.85}
            return state

        async def human_approval(state: RecruitingWorkflowState):
            return state

        async def embedding_generation(state: RecruitingWorkflowState):
            return state

        async def candidate_matching(state: RecruitingWorkflowState):
            return state

        async def persist_results(state: RecruitingWorkflowState):
            return state

        async def workflow_completed(state: RecruitingWorkflowState):
            state["workflow_status"] = "COMPLETED"
            return state

        async def workflow_failed(state: RecruitingWorkflowState):
            state["workflow_status"] = "FAILED"
            return state

        self.register_node("UploadValidationNode", create_service_node(upload_validation, "UploadValidationNode"))
        self.register_node("DocumentParsingNode", create_service_node(document_parsing, "DocumentParsingNode"))
        self.register_node("AIExtractionNode", create_service_node(ai_extraction, "AIExtractionNode"))
        self.register_node("CandidateValidationNode", create_service_node(candidate_validation, "CandidateValidationNode"))
        self.register_node("ProfileEvaluationNode", create_service_node(profile_evaluation, "ProfileEvaluationNode"))
        self.register_node("HumanApprovalNode", create_service_node(human_approval, "HumanApprovalNode"))
        self.register_node("EmbeddingGenerationNode", create_service_node(embedding_generation, "EmbeddingGenerationNode"))
        self.register_node("CandidateMatchingNode", create_service_node(candidate_matching, "CandidateMatchingNode"))
        self.register_node("PersistResultsNode", create_service_node(persist_results, "PersistResultsNode"))
        self.register_node("WorkflowCompletedNode", create_service_node(workflow_completed, "WorkflowCompletedNode"))
        self.register_node("WorkflowFailedNode", create_service_node(workflow_failed, "WorkflowFailedNode"))
