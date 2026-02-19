#!/usr/bin/env pwsh
<#
.SYNOPSIS
Build the Docker Sandbox image with pytest pre-installed

.DESCRIPTION
Creates an optimized Docker image for secure test execution with:
- pytest pre-installed (no network needed during execution)
- Memory limit: 256MB
- CPU limit: 0.5 cores
- No network access (--network=none)
- Read-only filesystem
- User isolation (non-root execution)
#>

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Building Docker Sandbox Image" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    $dockerVersion = docker --version 2>$null
    if (-not $?) {
        throw "Docker not found"
    }
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[1/2] Building image: ai-test-generator-sandbox:latest" -ForegroundColor Yellow
Write-Host "Status: Installing pytest and dependencies..." -ForegroundColor Gray
Write-Host ""

try {
    & docker build -t ai-test-generator-sandbox:latest -f Dockerfile.sandbox . -q
    if ($LASTEXITCODE -ne 0) {
        throw "Build failed with exit code $LASTEXITCODE"
    }
} catch {
    Write-Host ""
    Write-Host "✗ Error: Failed to build Docker image" -ForegroundColor Red
    Write-Host "Details: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[2/2] Verifying image..." -ForegroundColor Yellow

try {
    docker inspect ai-test-generator-sandbox:latest | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Verification failed"
    }
} catch {
    Write-Host ""
    Write-Host "✗ Error: Image build failed verification" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Success! Image built successfully" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Image details:" -ForegroundColor Cyan
docker images ai-test-generator-sandbox:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Start the backend: python -m uvicorn app.main:app --port 8000" -ForegroundColor Gray
Write-Host "2. Tests will now use the optimized sandbox image with:" -ForegroundColor Gray
Write-Host "   - Memory limit: 256MB" -ForegroundColor Gray
Write-Host "   - CPU limit: 0.5 cores" -ForegroundColor Gray
Write-Host "   - Network: COMPLETELY ISOLATED (--network=none)" -ForegroundColor Gray
Write-Host "   - Filesystem: Read-only (security hardened)" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to close"
