FROM node:13.8-slim as build

# dependencies
RUN npm install -g @angular/cli
COPY package.json /books-app/
WORKDIR /books-app
RUN npm install

# source
COPY . /books-app
RUN ng build
ENTRYPOINT [ "ng", "serve", "--host=0.0.0.0", "--disableHostCheck" ]

# express server for production
FROM node:13.8-slim

# server dependencies
COPY server/package.json /books-web/
WORKDIR /books-web
RUN npm install

# server code
COPY server /books-web

COPY --from=build /books-app/dist/books /books-web/static
ENTRYPOINT node index.js
