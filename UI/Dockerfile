FROM node:alpine

WORKDIR /src/app

COPY . /src/app

RUN rm -rf node_modules

RUN npm cache clean --force

RUN npm install -g npm

RUN npm install -g @angular/cli

CMD ["ng", "serve", "--host", "0.0.0.0"]
