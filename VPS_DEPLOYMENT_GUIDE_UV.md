# WhisperHedge UI - VPS Deployment Guide (using uv)

## Overview
Deploy WhisperHedge UI to a fresh Ubuntu VPS using `uv` for Python package management with SSL, automatic restarts, and production configuration.

## Prerequisites
- Ubuntu 22.04 or 20.04
- Domain name pointing to VPS IP
- SSH access to VPS
- Supabase project URL and service role key

## Step 1: Initial Server Setup

### Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### Create Application User
```bash
sudo adduser whisperhedge
sudo usermod -aG sudo whisperhedge
sudo su - whisperhedge
```

### Install Dependencies
```bash
# Python and build tools
sudo apt install -y python3 python3-venv git curl

# Nginx and SSL
sudo apt install -y nginx certbot python3-certbot-nginx unzip

# Systemd (usually pre-installed)
sudo apt install -y systemd
```

## Step 2: Install uv

### Install uv (Recommended Method)
```bash
# Install using the official installer
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH (add to ~/.bashrc)
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify installation
uv --version
```

### Alternative: Install via pip
```bash
# If the above doesn't work, install via pip
pip install uv
```

## Step 3: Application Setup

### Clone Repository
```bash
cd /home/whisperhedge
git clone <your-repo-url> whisperhedge-ui
cd whisperhedge-ui
```

### Create Python Virtual Environment with uv
```bash
# Create virtual environment
uv venv

# Activate environment
source .venv/bin/activate

# Or use uv to run commands directly (no activation needed)
uv python --version
```

### Install Dependencies with uv
```bash
# Install from requirements.txt
uv pip install -r requirements.txt

# Or if you have pyproject.toml
uv sync
```

### Create Environment File
```bash
cp .env.example .env
nano .env
```

Add your environment variables:
```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Application Configuration
REFLEX_HOST=0.0.0.0
REFLEX_PORT=8000
REFLEX_ENV=production

# Optional: Custom domain
REFLEX_DOMAIN=yourdomain.com
```

## Step 4: Test Application

### Run in Development Mode First
```bash
# Option 1: Activate venv first
source .venv/bin/activate
reflex run --host 0.0.0.0 --port 8000

# Option 2: Use uv run (no activation needed)
uv run reflex run --host 0.0.0.0 --port 8000
```

Test the application at `http://your-vps-ip:8000`

## Step 5: Systemd Service

### Create Service File
```bash
sudo nano /etc/systemd/system/whisperhedge.service
```
[Unit]
Description=WhisperHedge UI
After=network.target

[Service]
Type=simple
User=deltree
Group=deltree
WorkingDirectory=/home/deltree/whisperhedge_ui
# We set the environment variables here instead of the command line
Environment="PATH=/home/deltree/whisperhedge_ui/.venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="REFLEX_ENV=prod"
Environment="REFLEX_BACKEND_PORT=8000"
Environment="REFLEX_BACKEND_HOST=0.0.0.0"
Environment="__VITE_ADDITIONAL_SERVER_ALLOWED_HOSTS=whisperhedge.com"
# Load your Supabase/Private keys
EnvironmentFile=/home/deltree/whisperhedge_ui/web_ui/.env

# Use the simplest possible start command
ExecStart=/home/deltree/whisperhedge_ui/.venv/bin/reflex run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable whisperhedge
sudo systemctl start whisperhedge
```

### Check Service Status
```bash
sudo systemctl status whisperhedge
sudo journalctl -u whisperhedge -f
```

## Step 6: Nginx Reverse Proxy

### Create Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/whisperhedge
```

Add the following configuration:
```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    server_name whisperhedge.com;
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    # WebSocket support for Reflex
    location /_ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    location /_event {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/whisperhedge.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/whisperhedge.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}
server {
    if ($host = whisperhedge.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    server_name whisperhedge.com;
    return 404; # managed by Certbot


}
```

### Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/whisperhedge /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Step 7: SSL Certificate

### Obtain SSL Certificate
```bash
sudo certbot --nginx -d yourdomain.com
```

Follow the prompts to obtain and install the certificate.

### Verify Auto-Renewal
```bash
sudo certbot renew --dry-run
```

## Step 8: Security Hardening

### Configure Firewall
```bash
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### Disable Root SSH (Optional)
```bash
sudo nano /etc/ssh/sshd_config
```
Set `PermitRootLogin no` and restart SSH:
```bash
sudo systemctl restart ssh
```

## Step 9: Monitoring and Logs

### Application Logs
```bash
# View application logs
sudo journalctl -u whisperhedge -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Step 10: Updates and Maintenance

### Update Application with uv
```bash
cd /home/whisperhedge/whisperhedge-ui
git pull origin main

# Update dependencies with uv
uv pip install -r requirements.txt

# Or if using pyproject.toml
uv sync

# Restart service
sudo systemctl restart whisperhedge
```

### Update uv itself
```bash
uv self update
```

### Update System
```bash
sudo apt update && sudo apt upgrade -y
sudo systemctl restart nginx
```

## Step 11: uv-Specific Benefits

### Faster Package Installation
```bash
# uv is much faster than pip for installing packages
uv pip install -r requirements.txt
```

### Better Dependency Resolution
```bash
# uv has superior dependency resolution
uv add package-name  # Adds to pyproject.toml
uv remove package-name
```

### Lock File Management
```bash
# Generate lock file for reproducible builds
uv pip compile requirements.in -o requirements.txt
```

### Virtual Environment Management
```bash
# List virtual environments
uv venv list

# Remove virtual environment
uv venv remove .venv

# Create with specific Python version
uv venv --python 3.11
```

## Troubleshooting

### uv-Specific Issues

1. **uv not found after installation**
   ```bash
   # Add to PATH manually
   echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Virtual environment issues**
   ```bash
   # Remove and recreate venv
   rm -rf .venv
   uv venv
   uv pip install -r requirements.txt
   ```

3. **Permission issues**
   ```bash
   # Ensure correct ownership
   sudo chown -R whisperhedge:whisperhedge /home/whisperhedge/whisperhedge-ui
   ```

### Common Issues

1. **Service won't start**
   ```bash
   sudo journalctl -u whisperhedge -n 50
   ```

2. **502 Bad Gateway**
   - Check if Reflex is running: `sudo systemctl status whisperhedge`
   - Check Nginx config: `sudo nginx -t`

3. **SSL Certificate issues**
   ```bash
   sudo certbot certificates
   sudo certbot renew
   ```

## Alternative: Using uv run in Systemd

If you prefer to use `uv run` directly in the systemd service:

```ini
[Unit]
Description=WhisperHedge UI
After=network.target

[Service]
Type=simple
User=whisperhedge
Group=whisperhedge
WorkingDirectory=/home/whisperhedge/whisperhedge-ui
EnvironmentFile=/home/whisperhedge/whisperhedge-ui/.env
ExecStart=/home/whisperhedge/.cargo/bin/uv run reflex run --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Final Checklist

- [ ] uv installed and in PATH
- [ ] Application running with uv virtual environment
- [ ] Nginx reverse proxy configured
- [ ] SSL certificate installed
- [ ] Systemd service enabled
- [ ] Firewall configured
- [ ] Domain pointing correctly
- [ ] HTTPS working

## Performance Benefits of uv

- **10-100x faster** package installation
- **Better dependency resolution** with fewer conflicts
- **Built-in caching** for faster subsequent installs
- **Modern Python tooling** with active development

Your WhisperHedge UI should now be running in production with the modern uv package manager for better performance and reliability!
