# Etapa 1: build de Angular
FROM node:20-alpine AS builder

WORKDIR /app
COPY . .

RUN npm install && npm run build --prod
#CMD ["tail", "-f", "/dev/null"]

# Etapa 2: servir con Nginx
FROM nginx:stable-alpine

COPY --from=builder /app/dist/demo /usr/share/nginx/html
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80