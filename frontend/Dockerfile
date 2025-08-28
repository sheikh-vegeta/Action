# Step 1: Build the Vue application
FROM node:18 as builder

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .
RUN npm run build

# Step 2: Serve the built application with a lightweight server
FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

RUN npm install --production

EXPOSE 5173

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]
