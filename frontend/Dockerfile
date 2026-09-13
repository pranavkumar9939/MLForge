# Stage 1: build the static assets
FROM node:22-slim AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

# Baked in at build time - Vite env vars are resolved at build, not at
# container runtime. Override with --build-arg VITE_API_URL=... if your
# backend isn't at the default location.
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# Stage 2: serve with nginx
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://localhost/ > /dev/null || exit 1

CMD ["nginx", "-g", "daemon off;"]
