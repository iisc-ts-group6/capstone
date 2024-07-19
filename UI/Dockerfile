FROM node:alpine

WORKDIR /src/app

COPY . /src/app

RUN npm install -g npm@latest

RUN npm install -g @angular/cli

CMD ["ng", "serve", "--host", "0.0.0.0"]
