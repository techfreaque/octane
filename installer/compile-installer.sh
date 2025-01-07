source ../.venv/bin/activate
pip install -r dev-requirements.txt
pyinstaller --onefile installer.py