# AI Test Generator

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18%2B-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Hardened%20Sandbox-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

**Automatic test generation using AI with secure, isolated execution.** Generate comprehensive unit tests from code snippets using the Groq API, executed safely in hardened Docker sandboxes with multi-layer security.

**Status**: ✅ **Production Ready** - Security hardened, fully tested, professional API response format

## ⚡ Key Features

- **🤖 AI-Powered Test Generation** - Uses Groq API (llama-3.1-8b-instant) to intelligently generate unit tests
- **🔒 Security-First Architecture** - Docker sandbox isolation, AST validation, capability dropping, read-only filesystem
- **📊 Professional API** - Status codes, execution timing, error classification
- **⚙️ Production Configuration** - Memory/CPU limits, non-root execution, network isolation
- **🚀 Optimized Performance** - Pre-built Docker image with pytest (221MB)

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI (Python 3.11), Uvicorn |
| **Frontend** | React 18, TypeScript, Tailwind CSS, Vite |
| **LLM** | Groq API (llama-3.1-8b-instant) |
| **Isolation** | Docker with security hardening |
| **Testing** | pytest 9.0.2 |
| **Validation** | Pydantic, AST parsing |

## 🚀 Quick Start

### Prerequisites

- Docker Desktop (running)
- Python 3.11+
- Node.js 18+
- Groq API key ([Get free key](https://console.groq.com))

### 1. Clone and Configure

```bash
git clone https://github.com/yourname/ai-test-generator.git
cd ai-test-generator
cp .env.example .env
# Edit .env with your GROQ_API_KEY
```

### 2. Backend Setup

```bash
cd backend
pip install -r ../requirements.txt

# Build Docker sandbox image
../build-sandbox-image.ps1  # PowerShell
# OR
../build-sandbox-image.bat  # Command Prompt

# Start backend
python -m uvicorn app.main:app --port 8000
```

### 3. Frontend Setup (new terminal)

```bash
cd frontend
npm install
npm run dev
```

**Access**:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## 📡 API Endpoints

### Generate Tests

```http
POST /api/generate-tests
Content-Type: application/json

{
  "code": "def add(a, b):\n    return a + b"
}
```

**Response (200 OK)**:
```json
{
  "status": "success",
  "generated_tests": "import pytest\nfrom user_code import add\n\ndef test_add():\n    assert add(1, 2) == 3",
  "execution_output": "====== 1 passed in 0.08s ======",
  "passed": true,
  "execution_time": 2.35,
  "error": null,
  "error_type": null
}
```

**Status**: `success` | `failed` | `validation_error` | `execution_error` | `timeout`

### Validate Code

```http
POST /api/validate-code
Content-Type: application/json

{
  "code": "def hello():\n    pass"
}
```

Returns: Safety assessment without execution

## 🔐 Security Architecture

### Multi-Layer Defense

1. **Static Analysis** (AST)
   - Blocks: `os`, `subprocess`, `sys`, `socket`, etc.
   - Prevents: `eval()`, `exec()`, `open()`
   - Disallows: network access, file operations

2. **Docker Isolation**
   - `--network=none` - Complete network isolation
   - `--cap-drop=ALL` - Drop all capabilities
   - `--read-only` - Read-only filesystem
   - `--memory=256m` - Memory limit
   - `--cpus=0.5` - CPU limit
   - Non-root user execution

3. **Runtime Protection**
   - Temporary isolated directories
   - 5-second timeout per execution
   - Process limit (64)

✅ **All constraints verified and tested** in `test_sandbox_security.py`

## 📁 Project Structure

```
ai-test-generator/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry
│   │   ├── api/
│   │   │   └── routes.py        # API endpoints
│   │   ├── services/
│   │   │   ├── llm_service.py           # Groq integration
│   │   │   ├── test_generation_service.py    # Orchestration
│   │   │   ├── test_execution_service.py     # Docker runner
│   │   │   └── code_validator.py        # AST validation
│   │   └── schemas/
│   │       └── test_schema.py   # Pydantic models
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.ts
├── Dockerfile.sandbox           # Production sandbox image
├── Dockerfile.backend           # Backend container
├── docker-compose.yml
├── build-sandbox-image.ps1      # Build script (PowerShell)
├── build-sandbox-image.bat      # Build script (CMD)
├── SECURITY.md                  # Security details
└── README.md
```

## ⚙️ Configuration

### Environment Variables

```bash
# .env
GROQ_API_KEY=your_api_key_here
LOG_LEVEL=info
MAX_CODE_LENGTH=5000
DOCKER_IMAGE=ai-test-sandbox:latest
```

### Docker Build

```powershell
# Build custom sandbox image with pre-installed pytest
.\build-sandbox-image.ps1
```

The sandbox image includes:
- Python 3.11
- pytest 9.0.2
- Essential testing dependencies
- Non-root user (`testuser`)

## 📊 Performance

- **Generation Time**: ~1-2 seconds (LLM API call)
- **Execution Time**: ~0.1-1 second (Docker container)
- **Total Request**: ~2-3 seconds
- **Memory Limit**: 256MB per sandbox
- **CPU Limit**: 0.5 cores per sandbox

## 🧪 Development & Testing

### Run Test Suite

```bash
# Test sandbox security constraints
python test_sandbox_security.py

# Test API integration
python test_professional_api.py

# Test Docker execution
python test_api_docker.py
```

### Code Quality

- Type hints with Pydantic
- FastAPI automatic documentation (`/docs`)
- Comprehensive error handling
- AST-based code validation

## 🐳 Deployment

### Docker Compose

```bash
docker-compose up -d
```

### Manual Docker

```bash
# Build images
docker build -f Dockerfile.sandbox -t ai-test-sandbox:latest .
docker build -f Dockerfile.backend -t ai-test-backend:latest .

# Run backend
docker run -d --name backend -p 8000:8000 \
  -e GROQ_API_KEY=$GROQ_API_KEY \
  ai-test-backend:latest
```

## 📋 Error Handling

| Error Type | Meaning |
|-----------|---------|
| `CodeInvalid` | Code failed static validation |
| `SecurityViolation` | Security constraint violation |
| `TestFailure` | Tests executed but didn't pass |
| `DockerError` | Docker execution failed |
| `Timeout` | Execution exceeded time limit |
| `Unknown` | Unexpected error |

## 🚀 Roadmap

- [ ] WebSocket support for real-time test execution
- [ ] Test coverage analysis and reporting
- [ ] Multiple language support (JavaScript, Go, Rust)
- [ ] Database persistence for generated tests
- [ ] Rate limiting and API authentication
- [ ] Metrics and analytics dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📝 License

MIT License - See LICENSE file for details

## 📞 Support

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Security**: See [SECURITY.md](SECURITY.md) for security concerns
- **Docs**: [DOCKER_COMMAND_REFERENCE.md](DOCKER_COMMAND_REFERENCE.md) for Docker details

---

**Built with ❤️ for safe, automated test generation**
