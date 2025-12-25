# Stage 1: Build
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY app/package.json app/package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY app/ ./

# Build the app
RUN npm run build

# Stage 2: Serve
FROM nginx:alpine

# Copy built assets
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx config
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
