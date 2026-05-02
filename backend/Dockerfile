# This Dockerfile is for the FRONTEND service (ai-hospital-alliance)
# Backend service uses Dockerfile.backend at root
FROM node:20-alpine AS builder
WORKDIR /app

# Copy package files from parent (build context must be repo root)
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy entire project
COPY . .

ENV VITE_API_BASE_URL=https://zesty-recreation-production-6b62.up.railway.app
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY --from=builder /app/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
