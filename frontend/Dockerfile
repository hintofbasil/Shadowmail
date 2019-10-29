FROM node

WORKDIR /app

RUN npm install -g gatsby-cli

COPY package.json package-lock.json /app/
RUN npm install

COPY . /app

ENV COMMAND serve

RUN gatsby build

CMD gatsby $COMMAND -H 0.0.0.0
