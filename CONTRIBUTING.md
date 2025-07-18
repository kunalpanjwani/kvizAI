# Contributing to kvizAI

Thank you for your interest in contributing to kvizAI! This document provides guidelines for contributing to this open-source project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/kvizai.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Code Style

### Python (Backend)
- Use Black for code formatting
- Follow PEP 8 guidelines
- Use type hints where possible
- Write docstrings for functions and classes

### TypeScript/React (Frontend)
- Use ESLint and Prettier
- Follow React best practices
- Use TypeScript for type safety
- Write meaningful component names

## Making Changes

1. Make your changes in a feature branch
2. Write tests for new functionality
3. Update documentation if needed
4. Ensure all tests pass
5. Commit your changes with clear commit messages

## Commit Message Format

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(auth): add JWT authentication`
- `fix(api): resolve CORS issue`
- `docs(readme): update setup instructions`

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the CHANGELOG.md with a note describing your changes
3. The PR will be merged once you have the sign-off of at least one maintainer

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Reporting Bugs

Please use the GitHub issue tracker to report bugs. Include:
- A clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

## Feature Requests

We welcome feature requests! Please:
- Describe the feature clearly
- Explain why it would be useful
- Provide examples if possible

## Code of Conduct

This project is committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and considerate in all interactions.

## Questions?

If you have questions about contributing, please open an issue or reach out to the maintainers.

Thank you for contributing to kvizAI! 🚀 