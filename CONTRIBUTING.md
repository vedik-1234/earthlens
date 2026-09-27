# Contributing to EarthLens

Thank you for your interest in contributing to EarthLens!

## Development Setup

### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

### Frontend
```bash
cd frontend
npm install
```

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Max line length: 100
- Run `black` and `flake8`

### JavaScript
- Use ESLint configuration
- Follow React best practices
- Use functional components
- Meaningful component names

## Testing

- Write tests for new features
- Maintain >80% code coverage
- Run full test suite before submitting PR

## Commit Messages

- Use imperative mood ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Reference issues and PRs
- Example: `Add seasonal decomposition analysis (#42)`

## Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make focused changes
4. Write descriptive PR title and description
5. Ensure all tests pass
6. Request review

## Reporting Issues

Include:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment info (OS, Python/Node version)
- Screenshots or logs if applicable

Thank you for improving EarthLens!
