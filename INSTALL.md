# Installation Guide

## For End Users

### Install from PyPI (when published)
```bash
pip install archlib
```

### Install with optional tree-sitter support
```bash
pip install archlib[treesitter]
```

### Install from source
```bash
git clone <repo-url>
cd archlib
pip install -e .
```

## For Developers

### Setup development environment
```bash
# Clone repository
git clone <repo-url>
cd archlib

# Create virtual environment
uv venv
# or
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Unix/Mac
# or
.venv\Scripts\activate  # Windows

# Install in editable mode
uv pip install -e .
# or
pip install -e .

# Install with optional dependencies
uv pip install -e ".[treesitter]"
```

### Build distribution packages
```bash
# Install build tools
uv pip install build

# Build wheel and source distribution
python -m build

# Outputs will be in dist/
# - archlib-0.1.0-py3-none-any.whl
# - archlib-0.1.0.tar.gz
```

### Test installation
```bash
python -c "from archlib import Architecture, Goal, Solution, Implementation; print('✅ Installed successfully')"
```

## Package Structure

```
archlib/
├── archlib/           # Package source
│   └── __init__.py   # Main library code
├── examples/          # Usage examples
├── tests/             # Test suite (if added)
├── pyproject.toml    # Package configuration
└── README.md         # Documentation
```

## Usage in Projects

Once installed, projects can use archlib:

```python
from archlib import Architecture, Goal, Solution, Implementation

# Define your architecture...
```

See `examples/template.py` for a complete example.




