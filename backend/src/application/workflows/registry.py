from typing import Dict
from src.application.workflows.interfaces import NodeRegistry, WorkflowNode

class InMemoryNodeRegistry(NodeRegistry):
    def __init__(self):
        self._nodes: Dict[str, WorkflowNode] = {}

    def register_node(self, node_name: str, node: WorkflowNode) -> None:
        self._nodes[node_name] = node

    def get_node(self, node_name: str) -> WorkflowNode:
        if node_name not in self._nodes:
            raise ValueError(f"Node {node_name} not found in registry.")
        return self._nodes[node_name]
