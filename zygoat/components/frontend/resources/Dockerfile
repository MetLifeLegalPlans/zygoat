FROM node:latest

RUN mkdir /code
WORKDIR /code

COPY package.json yarn.lock ./
RUN yarn install

COPY . .

RUN yarn build

EXPOSE 3000
CMD yarn start -p 3000
