# Docker Sandbox Command Reference

## Official Secure Command

This is the exact Docker command used by the AI Test Generator with all security constraints:

### Full Command
```bash
docker run \
  --rm \
  --memory=256m \
  --cpus=0.5 \
  --network=none \
  --read-only \
  -v /path/to/tests:/tests:ro \
  -v /tmp \
  --workdir /tests \
  ai-test-generator-sandbox:latest \
  sh -c "pytest test_generated.py -v --tb=short"
```

### Breakdown

| Flag | Purpose | Security Impact |
|------|---------|-----------------|
| `--rm` | Clean up container after exit | Prevents resource leaks |
| `--memory=256m` | Memory limit | Prevents memory DoS |
| `--cpus=0.5` | CPU limit | Prevents CPU DoS |
| `--network=none` | NO network access | **Blocks all external connections** |
| `--read-only` | Read-only filesystem | Prevents code modification |
| `-v /tests:ro` | Tests mounted read-only | Code cannot be altered |
| `-v /tmp` | Writable temp directory | pytest cache storage |
| `--workdir /tests` | Working directory | Code execution location |

### What This Prevents

```
Threat: External API calls
√ BLOCKED by: --network=none

Threat: Malicious code installation
√ BLOCKED by: --network=none + --read-only

Threat: Memory-based DoS
√ BLOCKED by: --memory=256m

Threat: CPU-based DoS
√ BLOCKED by: --cpus=0.5

Threat: File system attacks
√ BLOCKED by: --read-only

Threat: Privilege escalation
√ BLOCKED by: USER testuser
```

## Windows-Compatible Form

### PowerShell
```powershell
docker run `
  --rm `
  --memory=256m `
  --cpus=0.5 `
  --network=none `
  --read-only `
  -v "C:\tests:/tests:ro" `
  -v /tmp `
  --workdir /tests `
  ai-test-generator-sandbox:latest `
  sh -c "pytest test_generated.py -v --tb=short"
```

### Command Prompt
```batch
docker run ^
  --rm ^
  --memory=256m ^
  --cpus=0.5 ^
  --network=none ^
  --read-only ^
  -v "C:\tests:/tests:ro" ^
  -v /tmp ^
  --workdir /tests ^
  ai-test-generator-sandbox:latest ^
  sh -c "pytest test_generated.py -v --tb=short"
```

## Implementation in Python

```python
docker_cmd = [
    "docker", "run",
    "--rm",
    "--memory=256m",           # Memory protection
    "--cpus=0.5",              # CPU protection
    "--network=none",          # CRITICAL: No network
    "--read-only",             # Read-only filesystem
    "-v", f"{test_folder}:/tests:ro",  # Code mounting
    "-v", "/tmp",              # Temp storage
    "--workdir", "/tests",
    "ai-test-generator-sandbox:latest",
    "sh", "-c",
    "pytest test_generated.py -v --tb=short"
]

result = subprocess.run(
    docker_cmd,
    capture_output=True,
    text=True,
    timeout=15
)
```

## Security Verification

To verify the sandbox is working correctly:

### 1. Test Network Isolation
```bash
# This should FAIL (network is blocked)
docker run --rm --network=none python:3.11 python -c "import requests; requests.get('https://google.com')"
# Result: Connection error (expected)
```

### 2. Test Memory Limit
```bash
# This should be terminated (memory exceeded)
docker run --rm --memory=256m python:3.11 python -c "x = [1]*100000000"
# Result: Killed (memory limit exceeded)
```

### 3. Test Read-Only Filesystem
```bash
# This should FAIL (filesystem is read-only)
docker run --rm --read-only python:3.11 python -c "open('/test.txt', 'w').write('test')"
# Result: Read-only file system error (expected)
```

### 4. Test Successful Execution
```bash
# This should PASS (legitimate test execution)
docker run --rm \
  --memory=256m \
  --cpus=0.5 \
  --network=none \
  --read-only \
  -v /tmp \
  ai-test-generator-sandbox:latest \
  pytest --version
# Result: pytest version info displayed
```

## Environment Variables

The Docker sandbox does NOT inherit environment variables from the host (by design).

If you need to pass configuration:
```bash
docker run \
  --rm \
  --memory=256m \
  --cpus=0.5 \
  --network=none \
  -e KEY=value \          # Only explicitly passed vars
  ai-test-generator-sandbox:latest \
  pytest test.py
```

## Building the Image

```bash
# Build with specific tag
docker build -t ai-test-generator-sandbox:latest -f Dockerfile.sandbox .

# View image information
docker images ai-test-generator-sandbox:latest

# Inspect image details
docker inspect ai-test-generator-sandbox:latest

# Remove image
docker rmi ai-test-generator-sandbox:latest
```

## Performance Tuning

### If tests are too slow:
```bash
# Increase CPU limit (trade-off: less security)
--cpus=1.0        # Instead of 0.5
```

### If tests run out of memory:
```bash
# Increase memory limit (trade-off: less security)
--memory=512m     # Instead of 256m
```

### If tests timeout:
```python
# Increase timeout in code
timeout=30        # Instead of 15
```

## Production Deployment

For production, ensure:
1. ✅ Image is pre-built and available locally
2. ✅ No `--network=host` (it's set to `--network=none`)
3. ✅ Memory and CPU limits are appropriate for your use case
4. ✅ Timeout is set based on expected test duration
5. ✅ Logging is enabled for security auditing
6. ✅ Container resource limits are monitored

## Debugging

If a test fails in sandbox but works locally:

1. Check network access isn't needed
   ```bash
   # Run locally with network disabled to simulate
   docker run --rm --network=none python:3.11 python your_test.py
   ```

2. Check filesystem access
   ```bash
   # Your test shouldn't write to the filesystem
   # Only /tmp is available
   ```

3. Check resource usage
   ```bash
   # Monitor during execution
   docker stats <container_id>
   ```

## Additional Reading

- [Docker Run Reference](https://docs.docker.com/engine/reference/run/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Linux Namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html)
- [pytest Documentation](https://docs.pytest.org/)
