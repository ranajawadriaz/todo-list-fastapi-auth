python -m venv newEnv
newEnv\Scripts\activate    \\use "deactivate" to deactivate environment 
pip install fastapi uvicorn
optional: pip freeze > requirements.txt //but not required here as it has already been created
uvicorn main:app --reload