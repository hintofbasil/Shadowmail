FROM node:lts-stretch-slim AS development
WORKDIR /app

COPY package.json package-lock.json /app/
RUN npm ci
VOLUME /app/node_modules

COPY . /app
CMD npm run serve



FROM node:lts-stretch-slim AS builder
WORKDIR /app
COPY --from=development /app /app

RUN apt-get update \
    && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-unstable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxtst6 libxss1 \
        --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN npm run build



FROM nginx:stable-alpine

USER nginx:nginx

EXPOSE 8080
COPY --from=builder /app/dist /dist
COPY nginx/nginx.conf /etc/nginx/nginx.conf
