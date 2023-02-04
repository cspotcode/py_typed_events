# On windows, you might need to help `just` find a bash shell.  This is the one installed by Git for Windows
set windows-shell := ["C:/Program Files/Git/bin/bash.exe", "-c"]

default:
    just --list --unsorted

formatSources := "src"

# Install some necessary development tools *globally* on Windows. Only use this for convenience if you understand what it will do.
install-devtools-globally-windows:
    # Assumes https://scoop.sh/
    # install just
    scoop install just

    # install pdm via pip
    pip install pdm

    # Alternative: install pdm via scoop
    #scoop bucket add frostming https://github.com/frostming/scoop-frostming.git
    #scoop install pdm

# Install python dependencies
bootstrap:
    # pip install .[test]
    # https://github.com/pdm-project/pdm
    pdm install -d

# Reformat all code
fmt:
    pdm run isort .
    pdm run black $formatSources

# Alias of lint
check: lint

# Check code formatting
lint:
    pdm run isort --check .
    pdm run black --check $formatSources

# Run to install a git pre-commit hook. If installed, committing will error-out when code doesn't match the formatter.  `make fmt` or Ctrl+Shift+B can fix this.
install-git-hooks:
    pdm run python scripts/install-git-hooks.py

# Uninstall the pre-commit hook
uninstall-git-hooks:
    pdm run python scripts/uninstall-git-hooks.py

# This is run by the pre-commit hook to verify formatting
pre-commit:
    @python scripts/pre-commit.py

example:
    pdm run python -m examples.example