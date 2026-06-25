import os
from pathlib import Path
from typing import Dict

class PromptRegistry:
    """Loads and caches prompt templates from the filesystem."""
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            self.base_dir = Path(__file__).parent
        else:
            self.base_dir = Path(base_dir)
            
        self._cache: Dict[str, str] = {}
        
    def get_prompt(self, domain: str, version: str) -> str:
        """
        Loads a prompt template.
        Example: get_prompt('resume_extraction', 'v1') -> returns contents of resume_extraction/v1.md
        """
        cache_key = f"{domain}_{version}"
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        prompt_path = self.base_dir / domain / f"{version}.md"
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt template {prompt_path} not found.")
            
        with open(prompt_path, "r", encoding="utf-8") as f:
            content = f.read()
            self._cache[cache_key] = content
            return content

# Global registry instance
registry = PromptRegistry()
