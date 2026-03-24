# Contributing to Brain-System

Thank you for your interest in contributing to Brain-System! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- macOS (for LaunchAgent features)
- Obsidian (for testing)

### Development Setup

```bash
# Clone the repository
cd ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Brain-System

# Create development environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flask

# Install in development mode
chmod +x brain
mkdir -p ~/.brain
ln -sf $(pwd)/multi-brain.py ~/.brain/
ln -sf $(pwd)/sync.py ~/.brain/
ln -sf $(pwd)/web.py ~/.brain/

# Test installation
brain vaults
```

## Development Workflow

1. **Fork and Branch**

```bash
# Create a feature branch
git checkout -b feature/your-feature-name
```

2. **Make Changes**

3. **Test Your Changes**

```bash
# Run tests
python3 -m pytest tests/

# Manual testing
brain sync
brain search "test"
python3 web.py
```

4. **Commit**

```bash
git add .
git commit -m "feat: add new feature"
```

## Coding Standards

### Python Style Guide

- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black default)
- Use type hints for public functions

### Example

```python
from typing import Optional, List
from pathlib import Path


def search_notes(
    query: str,
    limit: int = 20,
    vault: Optional[str] = None
) -> List[dict]:
    """Search notes across vaults.

    Args:
        query: Search string
        limit: Maximum results to return
        vault: Vault name or None for all

    Returns:
        List of note dictionaries
    """
    # Implementation here
    pass
```

### Naming Conventions

- **Modules**: `snake_case` (e.g., `multi_brain.py`)
- **Classes**: `PascalCase` (e.g., `MultiBrain`)
- **Functions**: `snake_case` (e.g., `import_vault`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `VAULTS`)

### Documentation

- Use docstrings for all public functions and classes
- Include Args and Returns sections
- Keep docstrings concise but informative

## Testing

### Writing Tests

Create tests in the `tests/` directory:

```python
import pytest
from multi_brain import MultiBrain


def test_search_returns_results():
    brain = MultiBrain("realm")
    results = brain.search("test")
    assert isinstance(results, list)


def test_add_task():
    brain = MultiBrain("realm")
    task_id = brain.add_task("Test task")
    assert task_id is not None
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Run specific test
pytest tests/test_multi_brain.py::test_search
```

## Documentation

### Updating Documentation

When adding features, update:

1. **README.md** - User-facing changes
2. **API.md** - New or modified APIs
3. **ARCHITECTURE.md** - Structural changes
4. **CHANGELOG.md** - Version history
5. **docs/** - Detailed guides

### Documentation Style

- Use clear, concise language
- Include examples for all APIs
- Add diagrams for complex flows
- Keep user docs separate from dev docs

## Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(cli): add vault filtering command
fix(web): resolve graph rendering on mobile
docs(api): update search endpoint documentation
test(sync): add tests for vault detection
```

## Submitting Changes

### Pull Request Process

1. Update documentation
2. Add/update tests
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit pull request with description

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] CHANGELOG updated
```

## Areas to Contribute

### High Priority

- [ ] Better error handling and messages
- [ ] Cross-platform support (Linux, Windows)
- [ ] Enhanced graph algorithms
- [ ] Performance optimizations

### Medium Priority

- [ ] Additional vault types
- [ ] Plugin system
- [ ] Export functionality
- [ ] Import from other tools

### Low Priority

- [ ] UI themes
- [ ] Additional link types
- [ ] Alternative search algorithms
- [ ] Statistics dashboard

## Questions?

Open an issue with the `question` label.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
