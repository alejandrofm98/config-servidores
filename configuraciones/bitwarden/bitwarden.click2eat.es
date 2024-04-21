server {
    listen 80;
    server_name bitwarden.click2eat.es www.bitwarden.click2eat.es;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name bitwarden.click2eat.es www.bitwarden.click2eat.es;

    ssl_certificate /etc/letsencrypt/live/click2eat.es/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/click2eat.es/privkey.pem;

    location / {
        proxy_pass http://localhost:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /notifications/hub/negotiate {
        proxy_pass http://localhost:9000;
    }
    
    location /notifications/hub {
        proxy_pass http://localhost:9012;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
