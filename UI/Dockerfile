FROM node:alpine

WORKDIR /src/app

COPY . /src/app

RUN rm -rf node_modules

RUN npm cache clean --force

RUN npm install -g npm@8.11.0

RUN npm install -g --no-package-lock @angular/cli

CMD ["ng", "serve", "--host", "0.0.0.0"]
