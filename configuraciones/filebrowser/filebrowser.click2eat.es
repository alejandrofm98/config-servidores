upstream filebrowser {
  keepalive 32; # keepalive connections
  server 127.0.0.1:8200; # jenkins ip and port
}


server {
    listen 80;
    server_name www.filebrowser.click2eat.es filebrowser.click2eat.es ;
    return 301 https://$host$request_uri;
}


server {

  server_name  www.filebrowser.click2eat.es filebrowser.click2eat.es ;
   listen 443 ssl;

    ssl_certificate /etc/letsencrypt/live/click2eat.es/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/click2eat.es/privkey.pem;

  access_log      /var/log/nginx/filebrowser.access.log;
  error_log       /var/log/nginx/filebrowser.error.log;

  # pass through headers from Jenkins that Nginx considers invalid
  ignore_invalid_headers off;

  location ~ "^/static/[0-9a-fA-F]{8}\/(.*)$" {
    # rewrite all static files into requests to the root
    # E.g /static/12345678/css/something.css will become /css/something.css
    rewrite "^/static/[0-9a-fA-F]{8}\/(.*)" /$1 last;
  }


  location / {
      sendfile off;
      proxy_pass         http://localhost:8200;
      proxy_redirect     default;
      proxy_http_version 1.1;

      # Required for Jenkins websocket agents
      proxy_set_header   Connection        'upgrade';
      proxy_set_header   Upgrade           $http_upgrade;

      proxy_set_header   Host              $http_host;
      proxy_set_header   X-Real-IP         $remote_addr;
      proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
      proxy_set_header   X-Forwarded-Proto $scheme;
      proxy_max_temp_file_size 0;

      #this is the maximum upload size
      client_max_body_size       10m;
      client_body_buffer_size    128k;

      proxy_connect_timeout      90;
      proxy_send_timeout         90;
      proxy_read_timeout         90;
      proxy_request_buffering    off; # Required for HTTP CLI commands
  }

}
