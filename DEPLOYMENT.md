# Deployment Guide

Complete deployment guide for AI Test Generator across three free-tier platforms.

## Architecture

```
Frontend (Vercel)
    ↓ HTTP
Backend (Render) 
    ↓ HTTP
Sandbox Service (Oracle Cloud VM)
```

---

## 1. Deploy Sandbox Service (Oracle Cloud)

### Prerequisites
- Oracle Cloud Free Tier account
- VM Instance (e.g., Ubuntu/Oracle Linux)

### Steps

#### 1.1 Create Oracle Cloud VM

1. Go to Oracle Cloud Console → Compute → Instances
2. Create Instance:
   - Image: Oracle Linux 8 or Ubuntu 22.04
   - Shape: VM.Standard.E2.1.Micro (Always Free)
   - Boot Volume: 50 GB
3. Download SSH private key
4. Note public IP address

#### 1.2 Configure VM

```bash
# SSH into VM
ssh -i ~/.ssh/oracle_key opc@<PUBLIC_IP>

# Install Docker (Oracle Linux)
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# OR Install Docker (Ubuntu)
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Log out and back in for group changes
exit
ssh -i ~/.ssh/oracle_key opc@<PUBLIC_IP>
```

#### 1.3 Configure Firewall

```bash
# Oracle Linux
sudo firewall-cmd --permanent --add-port=8001/tcp
sudo firewall-cmd --reload

# Ubuntu
sudo ufw allow 8001/tcp
```

**Important:** Add ingress rule in Oracle Cloud Console:
- Networking → Virtual Cloud Networks → Your VCN → Security Lists
- Add Ingress Rule:
  - Source CIDR: `0.0.0.0/0` (or restrict to Render IPs)
  - Destination Port: `8001`
  - IP Protocol: TCP

#### 1.4 Deploy Sandbox Service

```bash
# Clone repository
git clone https://github.com/robre8/ai-test-generator.git
cd ai-test-generator

# Build sandbox Docker image
docker build -f Dockerfile.sandbox -t ai-test-sandbox:latest .

# Build and run sandbox service
cd sandbox-service
docker build -t sandbox-service:latest .

docker run -d \
  --name sandbox-service \
  --restart unless-stopped \
  -p 8001:8001 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  sandbox-service:latest
```

#### 1.5 Verify Deployment

```bash
curl http://localhost:8001/health

# Should return:
# {"status":"healthy","docker_available":true}
```

Test from your local machine:
```bash
curl http://<ORACLE_VM_PUBLIC_IP>:8001/health
```

---

## 2. Deploy Backend (Render)

### Prerequisites
- Render account (free tier)
- GitHub repository: `robre8/ai-test-generator`
- Groq API Key

### Steps

#### 2.1 Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Web Service**
3. Connect GitHub repository: `robre8/ai-test-generator`
4. Configure:
   - **Name:** `ai-test-generator-backend`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Runtime:** Docker
   - **Dockerfile Path:** `Dockerfile.backend`
   - **Instance Type:** Free

#### 2.2 Add Environment Variables

In Render service settings → Environment:

```
GROQ_API_KEY=<your_groq_api_key>
SANDBOX_SERVICE_URL=http://<ORACLE_VM_PUBLIC_IP>:8001
```

#### 2.3 Deploy

- Click **Create Web Service**
- Wait for build and deployment (~5 minutes)
- Note your backend URL: `https://ai-test-generator-backend.onrender.com`

#### 2.4 Verify Deployment

```bash
curl https://ai-test-generator-backend.onrender.com/
# Should return: {"message":"AI Test Generator API is running"}
```

---

## 3. Deploy Frontend (Vercel)

### Prerequisites
- Vercel account (free tier)
- GitHub repository: `robre8/ai-test-generator`
- Render backend URL from step 2

### Steps

#### 3.1 Create Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Add New...** → **Project**
3. Import `robre8/ai-test-generator`
4. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

#### 3.2 Add Environment Variable

In project settings → Environment Variables:

```
VITE_API_URL=https://ai-test-generator-backend.onrender.com
```

#### 3.3 Deploy

- Click **Deploy**
- Wait for build (~2 minutes)
- Note your frontend URL: `https://ai-test-generator.vercel.app`

#### 3.4 Verify Deployment

Visit your Vercel URL and test:
1. Paste Python code
2. Click "Generate Tests"
3. Verify tests are generated and executed

---

## Environment Variables Summary

### Sandbox Service (Oracle Cloud VM)
- None required

### Backend (Render)
| Variable | Value | Description |
|----------|-------|-------------|
| `GROQ_API_KEY` | Your Groq API key | Required for LLM test generation |
| `SANDBOX_SERVICE_URL` | `http://<ORACLE_VM_IP>:8001` | URL of sandbox service on Oracle VM |

### Frontend (Vercel)
| Variable | Value | Description |
|----------|-------|-------------|
| `VITE_API_URL` | `https://ai-test-generator-backend.onrender.com` | URL of backend on Render |

---

## Troubleshooting

### Sandbox Service Issues

**Health check fails:**
```bash
# Check service logs
docker logs sandbox-service

# Check Docker is running
docker ps

# Rebuild and restart
docker stop sandbox-service
docker rm sandbox-service
cd sandbox-service
docker build -t sandbox-service:latest .
docker run -d --name sandbox-service --restart unless-stopped -p 8001:8001 \
  -v /var/run/docker.sock:/var/run/docker.sock sandbox-service:latest
```

**Connection refused:**
- Verify Oracle Cloud ingress rule for port 8001
- Check VM firewall: `sudo firewall-cmd --list-all`
- Verify service is listening: `netstat -tulpn | grep 8001`

### Backend Issues

**Build fails on Render:**
- Check Dockerfile.backend syntax
- Verify all dependencies in requirements.txt
- Check Render build logs

**Cannot connect to sandbox:**
- Verify `SANDBOX_SERVICE_URL` environment variable
- Test sandbox URL directly: `curl http://<IP>:8001/health`
- Check Oracle Cloud VM is running

### Frontend Issues

**Cannot reach backend:**
- Verify `VITE_API_URL` environment variable in Vercel
- Check backend is running: `curl https://<backend-url>/`
- Check browser console for CORS errors

**Build fails:**
- Verify Root Directory is set to `frontend`
- Check Node.js version compatibility
- Review Vercel build logs

---

## Updating Deployments

### Update Sandbox Service
```bash
ssh -i ~/.ssh/oracle_key opc@<PUBLIC_IP>
cd ai-test-generator
git pull
docker build -f Dockerfile.sandbox -t ai-test-sandbox:latest .
docker restart sandbox-service
```

### Update Backend
- Push changes to GitHub `main` branch
- Render auto-deploys from GitHub

### Update Frontend
- Push changes to GitHub `main` branch
- Vercel auto-deploys from GitHub

---

## Cost Analysis

| Service | Plan | Cost |
|---------|------|------|
| Oracle Cloud VM | Always Free Tier | $0 |
| Render | Free Tier | $0 |
| Vercel | Hobby Plan | $0 |
| Groq API | Free Tier | $0 |
| **Total** | | **$0/month** |

**Limitations:**
- Render Free: 750 hours/month, sleeps after 15 min inactivity
- Oracle Always Free: 2 VMs, 1 GB RAM each
- Vercel Hobby: 100 GB bandwidth/month
- Groq Free: API rate limits apply

---

## Security Considerations

1. **Sandbox Isolation:** Tests run in Docker with strict security constraints
2. **API Keys:** Never commit API keys to git
3. **Firewall:** Consider restricting Oracle VM ingress to Render IPs only
4. **HTTPS:** Render and Vercel provide automatic HTTPS
5. **Code Validation:** AST-based static analysis before execution

---

## Monitoring

### Check Service Health

```bash
# Sandbox
curl http://<ORACLE_VM_IP>:8001/health

# Backend
curl https://ai-test-generator-backend.onrender.com/

# Frontend
curl https://ai-test-generator.vercel.app
```

### View Logs

- **Sandbox:** `ssh` into VM → `docker logs sandbox-service`
- **Backend:** Render Dashboard → Logs tab
- **Frontend:** Vercel Dashboard → Deployments → View logs
