# Use official lightweight Nginx Alpine image
FROM nginx:alpine

# Set working directory to Nginx web root
WORKDIR /usr/share/nginx/html

# Remove default static assets
RUN rm -rf ./*

# Copy static frontend assets (HTML, CSS, JS) into Nginx web root
COPY . .

# Remove docker configuration files if copied into web root
RUN rm -f Dockerfile .dockerignore

# Expose standard HTTP port
EXPOSE 80

# Start Nginx server in the foreground
CMD ["nginx", "-g", "daemon off;"]

