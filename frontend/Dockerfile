FROM node:19-alpine as build-step
WORKDIR /app
COPY . .
RUN npm ci 
RUN npm run build

# Build step #2: build an nginx container
FROM nginx:stable-alpine
COPY --from=build-step /app/build /usr/share/nginx/html
COPY ./ngnix.conf /etc/nginx/conf.d/default.conf
