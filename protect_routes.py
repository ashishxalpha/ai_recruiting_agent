import os
import re

endpoints_dir = "backend/src/presentation/api/v1/endpoints"

files_to_protect = [
    "workflows.py", "jobs.py", "organization.py", "memory.py",
    "agents.py", "tools.py", "coordinator.py", "resumes.py"
]

import_statement = "from src.presentation.api.dependencies.auth import get_current_user\nfrom src.infrastructure.database.models import UserModel\n"

for filename in files_to_protect:
    filepath = os.path.join(endpoints_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r') as f:
        content = f.read()
        
    # Check if already imported
    if "get_current_user" not in content:
        # Add import after APIRouter
        content = content.replace("from fastapi import APIRouter", f"from fastapi import APIRouter\n{import_statement}")
        
    # Inject current_user parameter into def functions decorated with @router.post
    # This is a bit tricky with regex, we can just replace `@router.post(...)` and the next line `async def xxx(`
    # Let's find all `async def ` that follow `@router.post`
    
    # regex to match: @router.post(.*?)\nasync def ([a-zA-Z0-9_]+)\(
    pattern = r'(@router\.post.*?\n(?:@[a-zA-Z0-9_.]+.*?\n)*?async def [a-zA-Z0-9_]+\()'
    replacement = r'\1current_user: UserModel = Depends(get_current_user), '
    
    new_content = re.sub(pattern, replacement, content)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
        
print("Routes protected.")
