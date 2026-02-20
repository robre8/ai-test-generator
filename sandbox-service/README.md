# AI Test Sandbox Service

Isolated test execution service running in Docker with security constraints.

## Setup on Oracle Cloud VM

### 1. Install Docker

```bash
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### 2. Build Sandbox Image

```bash
git clone https://github.com/robre8/ai-test-generator.git
cd ai-test-generator
docker build -f Dockerfile.sandbox -t ai-test-sandbox:latest .
```

### 3. Run Sandbox Service

```bash
cd sandbox-service
docker build -t sandbox-service:latest .

# Run service
docker run -d \
  --name sandbox-service \
  --restart unless-stopped \
  -p 8001:8001 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  sandbox-service:latest
```

### 4. Configure Firewall

```bash
# Oracle Cloud: Add ingress rule for port 8001
# Security List: Allow TCP 8001 from your backend IP or 0.0.0.0/0 (if public)

# VM Firewall
sudo firewall-cmd --permanent --add-port=8001/tcp
sudo firewall-cmd --reload
```

### 5. Test Service

```bash
curl http://<oracle-vm-ip>:8001/health
```

## API Endpoints

### Health Check
```http
GET /health
```

### Execute Tests
```http
POST /execute
Content-Type: application/json

{
  "code": "def add(a, b):\n    return a + b",
  "tests": "import pytest\nfrom user_code import add\n\ndef test_add():\n    assert add(1, 2) == 3"
}
```

## Security

- Docker socket mounted (requires VM with Docker access)
- Each execution runs in isolated container
- Memory limit: 256MB
- CPU limit: 0.5 cores
- Network: disabled
- Filesystem: read-only

## Environment Variables

None required. Service runs on port 8001 by default.
