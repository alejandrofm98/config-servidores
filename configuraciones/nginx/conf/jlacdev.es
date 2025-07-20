server {
    listen 80;
    server_name jlacdev.es www.jlacdev.es;

    # Redirige todo el tráfico HTTP a HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name jlacdev.es www.jlacdev.es;

    ssl_certificate /etc/letsencrypt/live/jlacdev.es/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/jlacdev.es/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Root del frontend Angular
    root /usr/share/nginx/html/browser;
    index index.html;

    # IMPORTANTE: Las locations más específicas van PRIMERO

    # Ruta para Certbot challenge
    location ~ ^/.well-known/acme-challenge/ {
        root /var/www/certbot;
        allow all;
    }

    # Proxy para la API backend - DEBE IR ANTES que location /
    location /api/ {
        # Tu backend espera /api/ en la URL, así que pasamos toda la ruta
        proxy_pass http://crud-jlac-backend:8080/api/;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Headers adicionales útiles
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Para debug - MUY IMPORTANTE
        access_log /var/log/nginx/api_access.log;
        error_log /var/log/nginx/api_error.log debug;

    }

    # Angular SPA: redirige todo a index.html - VA AL FINAL
    location / {
        try_files $uri $uri/ /index.html;
    }
}