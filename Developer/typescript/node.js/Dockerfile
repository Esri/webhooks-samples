FROM node:16 AS builder
EXPOSE 3000
WORKDIR /app
COPY . .
RUN npm ci
RUN npm run build

FROM node:16
WORKDIR /app
COPY --from=builder /app/node_modules node_modules
COPY --from=builder /app/dist dist
RUN npm install pm2 -g
CMD ["pm2-runtime", "dist/app.js"]
