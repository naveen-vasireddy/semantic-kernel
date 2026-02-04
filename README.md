# Semantic Kernel Python Starter

This minimal project creates a virtual environment and installs Microsoft's Semantic Kernel.

Quick start (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python src\main.py
```
Using the venv (Windows PowerShell):

```powershell
# Create the venv (only if you haven't already)
python -m venv .venv

# Activate the venv
. .venv\Scripts\Activate.ps1

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Run the example
python src\main.py
```

Using the venv in VS Code:

- Open the workspace folder in VS Code.
- Press Ctrl+Shift+P -> "Python: Select Interpreter" and choose the interpreter at `.venv\Scripts\python.exe`.
- Run `src/main.py` from the Run view or integrated terminal (after activating `.venv`).

If you'd like, I can add a small `run.ps1` helper to simplify activation and running.
