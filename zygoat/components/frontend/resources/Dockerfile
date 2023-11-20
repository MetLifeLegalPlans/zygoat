FROM node:latest

RUN mkdir /code
WORKDIR /code

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000
CMD npm run start -p 3000
