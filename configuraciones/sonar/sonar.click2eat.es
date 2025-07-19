server {
    listen 80;
    server_name sonar.click2eat.es www.sonar.click2eat.es;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name sonar.click2eat.es www.sonar.click2eat.es;

    access_log /var/log/nginx/sonar.click2eat.es.access.log;
    error_log /var/log/nginx/sonar.click2eat.es.error.log;

    ssl_certificate /etc/letsencrypt/live/click2eat.es/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/click2eat.es/privkey.pem;

    location / {
        proxy_pass http://localhost:9001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }


}
