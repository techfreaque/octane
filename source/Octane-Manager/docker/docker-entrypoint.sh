python -m venv .venv
PATH=".venv/bin:${PATH}"

pip install -U pip>=20.0.0

pip install --prefer-binary -r source/Octane-Installer/requirements.txt
pip install -e ./source/Octane-Installer
octane-installer --start