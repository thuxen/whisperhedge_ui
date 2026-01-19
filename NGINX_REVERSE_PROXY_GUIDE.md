# Nginx Reverse Proxy Setup for WhisperHedge UI

## Overview
Configure Nginx as a reverse proxy for WhisperHedge UI running on port 8000, with SSL, WebSocket support, and security headers.

## Prerequisites
- Ubuntu server with Nginx installed
- WhisperHedge UI running on port 8000
- Domain name pointing to server IP

## Step 1: Install Nginx

```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

## Step 2: Create Nginx Configuration

### Basic Configuration (HTTP only)
```bash
sudo nano /etc/nginx/sites-available/whisperhedge
```

Add the following content:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect www to non-www (optional)
    if ($host = www.yourdomain.com) {
        return 301 https://yourdomain.com$request_uri;
    }

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

### Production Configuration (with SSL and security)
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect all HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript;

    # Main Application Proxy
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Buffer settings
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        proxy_busy_buffers_size 8k;
    }

    # WebSocket Support for Reflex
    location /_ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
        
        # WebSocket specific timeouts
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }

    # Static assets (if you have any)
    location /static/ {
        alias /home/whisperhedge/whisperhedge-ui/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

## Step 3: Enable Configuration

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/whisperhedge /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

## Step 4: SSL Certificate Setup

### Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Obtain SSL Certificate
```bash
# Interactive mode
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Or non-interactive (if you already have nginx config)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com --agree-tos --email your-email@example.com --non-interactive
```

### Verify SSL
```bash
# Check certificate status
sudo certbot certificates

# Test renewal
sudo certbot renew --dry-run
```

## Step 5: Firewall Configuration

```bash
# Allow Nginx through firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable
```

## Step 6: Test Setup

### Test HTTP
```bash
curl -I http://yourdomain.com
```

### Test HTTPS
```bash
curl -I https://yourdomain.com
```

### Test WebSocket
```bash
# You can test WebSocket connection with:
wscat -c wss://yourdomain.com/_ws
```

## Step 7: Monitoring and Logs

### Access Logs
```bash
# View access logs
sudo tail -f /var/log/nginx/access.log

# View error logs
sudo tail -f /var/log/nginx/error.log
```

### Monitor Performance
```bash
# Install htop for monitoring
sudo apt install htop

# Monitor Nginx processes
sudo systemctl status nginx
```

## Advanced Configurations

### Rate Limiting
Add to server block:
```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;

location /api/ {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://127.0.0.1:8000;
}

location /login {
    limit_req zone=login burst=5 nodelay;
    proxy_pass http://127.0.0.1:8000;
}
```

### IP Whitelist (for admin areas)
```nginx
# Allow only specific IPs for admin
location /admin {
    allow 192.168.1.100;
    allow 203.0.113.5;
    deny all;
    proxy_pass http://127.0.0.1:8000;
}
```

### Custom Error Pages
```nginx
error_page 404 /404.html;
error_page 500 502 503 504 /50x.html;

location = /50x.html {
    root /usr/share/nginx/html;
}
```

## Troubleshooting

### Common Issues

1. **502 Bad Gateway**
   ```bash
   # Check if backend is running
   curl http://127.0.0.1:8000
   
   # Check nginx error log
   sudo tail -f /var/log/nginx/error.log
   
   # Check nginx config
   sudo nginx -t
   ```

2. **WebSocket not working**
   ```bash
   # Check WebSocket headers
   curl -I -H "Connection: Upgrade" -H "Upgrade: websocket" http://yourdomain.com/_ws
   
   # Verify nginx config includes WebSocket settings
   grep -A 10 "location /_ws" /etc/nginx/sites-available/whisperhedge
   ```

3. **SSL Certificate issues**
   ```bash
   # Check certificate expiration
   openssl x509 -in /etc/letsencrypt/live/yourdomain.com/cert.pem -text -noout
   
   # Force renewal
   sudo certbot renew --force-renewal
   ```

4. **High memory usage**
   ```nginx
   # Add to nginx config to reduce memory
   worker_processes auto;
   worker_connections 1024;
   ```

### Performance Optimization

### Enable HTTP/2
```nginx
server {
    listen 443 ssl http2;
    # ... rest of config
}
```

### Client Caching
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Connection Pooling
```nginx
upstream whisperhedge {
    server 127.0.0.1:8000;
    keepalive 32;
}

server {
    location / {
        proxy_pass http://whisperhedge;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

## Maintenance

### Renew SSL Certificates
```bash
# Certbot auto-renews, but you can test:
sudo certbot renew

# Check auto-renewal timer
sudo systemctl list-timers | grep certbot
```

### Update Nginx
```bash
sudo apt update
sudo apt upgrade nginx
sudo nginx -t
sudo systemctl reload nginx
```

### Backup Configuration
```bash
# Backup nginx config
sudo cp -r /etc/nginx/sites-available/whisperhedge /home/whisperhedge/nginx-backup/
```

## Multiple Domains

If you need to host multiple domains:
```nginx
server {
    listen 443 ssl http2;
    server_name app1.yourdomain.com;
    # ... config for app1
}

server {
    listen 443 ssl http2;
    server_name app2.yourdomain.com;
    # ... config for app2
}
```

## Final Checklist

- [ ] Nginx installed and running
- [ ] Configuration file created and enabled
- [ ] SSL certificate obtained and configured
- [ ] WebSocket support working
- [ ] Security headers added
- [ ] Firewall configured
- [ ] Logs monitoring setup
- [ ] Backup strategy in place

Your Nginx reverse proxy is now configured to serve WhisperHedge UI with SSL, WebSocket support, and production-ready security!
