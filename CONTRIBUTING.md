# Contributing to AI Test Generator

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker Desktop
- Git

### Local Setup

```bash
# 1. Clone and enter directory
git clone https://github.com/yourname/ai-test-generator.git
cd ai-test-generator

# 2. Create Python virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
cd backend
pip install -r ../requirements.txt

# 4. Setup frontend
cd ../frontend
npm install
cd ..

# 5. Configure environment
cp .env.example .env
# Edit .env with your GROQ_API_KEY

# 6. Build Docker sandbox image
.\build-sandbox-image.ps1  # PowerShell
# OR
build-sandbox-image.bat  # Command Prompt

# 7. Run tests
python test_professional_api.py
python test_api_docker.py
```

## Code Style

### Python
- Follow PEP 8 with Black formatter
- Use type hints on all functions
- Maximum line length: 100 characters
- Use meaningful variable names

```python
# Good
def validate_code_safety(code: str) -> tuple[bool, str, list[str]]:
    """Validate code doesn't contain dangerous operations."""
    is_safe = check_ast(code)
    return is_safe, message, items

# Avoid
def check(c):
    return validate(c)
```

### TypeScript/React
- Use functional components with hooks
- Props should be typed with interfaces
- Use meaningful component names
- Export types separately

```typescript
// Good
interface CodeEditorProps {
  code: string;
  onChange: (code: string) => void;
  disabled?: boolean;
}

export const CodeEditor: React.FC<CodeEditorProps> = ({ code, onChange, disabled }) => {
  // Component logic
};
```

## Commit Messages

Follow conventional commits format:

```
feat: add feature description
fix: bug fix description
refactor: code restructuring
docs: documentation updates
test: add/update tests
chore: maintenance tasks
```

### Examples (GOOD)
```
feat: add websocket support for real-time execution
feat: integrate Groq LLM for test generation
fix: handle docker timeout scenarios
refactor: modularize test execution service
docs: update security architecture section
test: add coverage for code validation
```

### Examples (AVOID)
```
update
fix bug
changes
update stuff
minor fix
```

## Testing

### Before Submitting PR

```bash
# 1. Run security tests
python test_sandbox_security.py

# 2. Run API integration tests
python test_professional_api.py

# 3. Run Docker execution tests
python test_api_docker.py

# 4. Check code style (if Black installed)
black backend/app --check
```

### Writing Tests
- Place unit tests near the code being tested
- Use descriptive test names: `test_<function>_<scenario>`
- Test both success and failure paths

## Pull Request Process

1. **Fork and branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes**
   - Keep commits atomic and focused
   - Update tests if changing behavior
   - Update docs if adding features

3. **Push and create PR**
   ```bash
   git push origin feature/my-feature
   ```
   Include:
   - Clear description of changes
   - Why the change was needed
   - Testing done
   - Screenshots if UI changes

4. **PR Reviews**
   - Address feedback promptly
   - Keep commits clean (squash if needed)
   - Request re-review once changes made

## Architecture Guidelines

### Backend Services
- Keep services focused on single responsibility
- Use type hints throughout
- Handle errors with proper status codes
- Log important operations

### Docker Sandbox
- Never relax security constraints without security review
- Always test capability drops with test_sandbox_security.py
- Document any new Docker flags added

### Frontend
- Reusable components in `/components`
- Keep component files small (<200 lines)
- Use context for shared state
- Optimize re-renders with React.memo for expensive components

## Security

### Important
- Never commit `.env` files
- Never commit credentials or API keys
- Always validate user input (both frontend and backend)
- Report security issues privately (don't open public issues)

### Code Review Checklist
- [ ] No hardcoded credentials
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak sensitive info
- [ ] Docker security constraints still enforced

## Documentation

Update docs for:
- New features
- API changes
- Configuration options
- Setup/deployment steps

Documentation should be:
- Clear and concise
- Include examples
- Explain the "why" not just the "how"

## Questions?

Open an issue with label `question` or reach out to project maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
