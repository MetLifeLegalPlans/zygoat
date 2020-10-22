FROM node:latest

RUN mkdir /code
WORKDIR /code
ADD package.json /code/
RUN yarn install

CMD yarn dev -p 3000
