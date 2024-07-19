FROM node:20.11.1-alpine

WORKDIR /src/app

COPY . /src/app

RUN npm install --foreground-scripts

RUN npm install -g @angular/cli

CMD ["ng", "serve"]
