from typing import Dict, List, Optional
from src.application.workflows.interfaces import WorkflowDefinition, WorkflowDefinitionRegistry

class InMemoryWorkflowDefinitionRegistry(WorkflowDefinitionRegistry):
    """
    In-memory implementation of the WorkflowDefinitionRegistry.
    Stores versions in a nested dictionary mapping name -> version -> definition.
    """
    def __init__(self):
        self._definitions: Dict[str, Dict[str, WorkflowDefinition]] = {}
        
    def register(self, definition: WorkflowDefinition) -> None:
        if definition.name not in self._definitions:
            self._definitions[definition.name] = {}
            
        self._definitions[definition.name][definition.version] = definition
        
    def get(self, name: str, version: Optional[str] = None) -> WorkflowDefinition:
        if name not in self._definitions:
            raise ValueError(f"Workflow '{name}' not found in registry.")
            
        if version is None:
            version = self.latest_version(name)
            
        if version not in self._definitions[name]:
            raise ValueError(f"Version '{version}' for workflow '{name}' not found.")
            
        return self._definitions[name][version]
        
    def list(self) -> List[WorkflowDefinition]:
        result = []
        for name_versions in self._definitions.values():
            for definition in name_versions.values():
                result.append(definition)
        return result
        
    def exists(self, name: str, version: Optional[str] = None) -> bool:
        if name not in self._definitions:
            return False
            
        if version is None:
            return True
            
        return version in self._definitions[name]
        
    def latest_version(self, name: str) -> Optional[str]:
        if name not in self._definitions or not self._definitions[name]:
            return None
            
        # Assuming semantic versioning or lexically sortable version strings
        versions = list(self._definitions[name].keys())
        versions.sort(reverse=True)
        return versions[0]
