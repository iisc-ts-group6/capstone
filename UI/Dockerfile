FROM node:alpine

WORKDIR /src/app

COPY . /src/app

RUN npm install npm@latest

RUN npm install -g @angular/cli

CMD ["ng", "serve"]
