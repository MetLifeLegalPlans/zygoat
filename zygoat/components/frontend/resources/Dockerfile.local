FROM node:14

RUN mkdir /code
WORKDIR /code
ADD package.json /code/
RUN yarn install

CMD yarn dev -p 3000
