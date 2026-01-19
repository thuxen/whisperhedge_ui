# WhisperHedge UI - VPS Deployment Guide

## Overview
Deploy WhisperHedge UI to a fresh Ubuntu VPS with SSL, automatic restarts, and production configuration.

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
sudo apt install -y python3 python3-pip python3-venv git curl

# Nginx and SSL
sudo apt install -y nginx certbot python3-certbot-nginx

# Systemd (usually pre-installed)
sudo apt install -y systemd
```

## Step 2: Application Setup

### Clone Repository
```bash
cd /home/whisperhedge
git clone <your-repo-url> whisperhedge-ui
cd whisperhedge-ui
```

### Create Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
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

## Step 3: Database Setup

### Verify Supabase Connection
```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Supabase URL:', os.getenv('SUPABASE_URL'))
print('Service Key configured:', bool(os.getenv('SUPABASE_SERVICE_ROLE_KEY')))
"
```

### Run Database Migrations (if applicable)
```bash
# If you have migration scripts
python scripts/migrate.py
```

## Step 4: Test Application

### Run in Development Mode First
```bash
source venv/bin/activate
reflex run --host 0.0.0.0 --port 8000
```

Test the application at `http://your-vps-ip:8000`

## Step 5: Systemd Service

### Create Service File
```bash
sudo nano /etc/systemd/system/whisperhedge.service
```

Add the following content:
```ini
[Unit]
Description=WhisperHedge UI
After=network.target

[Service]
Type=simple
User=whisperhedge
Group=whisperhedge
WorkingDirectory=/home/whisperhedge/whisperhedge-ui
Environment=PATH=/home/whisperhedge/whisperhedge-ui/venv/bin
EnvironmentFile=/home/whisperhedge/whisperhedge-ui/.env
ExecStart=/home/whisperhedge/whisperhedge-ui/venv/bin/reflex run --host 0.0.0.0 --port 8000
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
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
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
    }
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

### Create Log Rotation (Optional)
```bash
sudo nano /etc/logrotate.d/whisperhedge
```

Add:
```
/home/whisperhedge/.local/share/whisperhedge/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 whisperhedge whisperhedge
}
```

## Step 10: Backup Strategy

### Backup Configuration
```bash
# Create backup script
sudo nano /home/whisperhedge/backup.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/home/whisperhedge/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup application files
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /home/whisperhedge/whisperhedge-ui

# Backup environment file
cp /home/whisperhedge/whisperhedge-ui/.env $BACKUP_DIR/env_$DATE

# Clean old backups (keep 7 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "env_*" -mtime +7 -delete

echo "Backup completed: $DATE"
```

Make executable:
```bash
chmod +x /home/whisperhedge/backup.sh
```

### Add Cron Job for Daily Backups
```bash
crontab -e
```

Add:
```
0 2 * * * /home/whisperhedge/backup.sh
```

## Step 11: Updates and Maintenance

### Update Application
```bash
cd /home/whisperhedge/whisperhedge-ui
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart whisperhedge
```

### Update System
```bash
sudo apt update && sudo apt upgrade -y
sudo systemctl restart nginx
```

## Troubleshooting

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

4. **Database connection issues**
   - Verify Supabase credentials in `.env`
   - Check network connectivity

### Performance Optimization

1. **Enable Gzip Compression** (add to Nginx config):
   ```nginx
   gzip on;
   gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
   ```

2. **Configure Connection Pooling** (if needed)
   - Adjust `REFLEX_MAX_CONNECTIONS` in `.env`

## Final Checklist

- [ ] Application running on port 8000
- [ ] Nginx reverse proxy configured
- [ ] SSL certificate installed
- [ ] Systemd service enabled
- [ ] Firewall configured
- [ ] Backups scheduled
- [ ] Monitoring setup
- [ ] Domain pointing correctly
- [ ] HTTPS working

## Support

If you encounter issues:
1. Check logs: `sudo journalctl -u whisperhedge -f`
2. Verify configuration files
3. Test locally first
4. Check Supabase connection

Your WhisperHedge UI should now be running in production with SSL, automatic restarts, and proper monitoring!
