FROM 818831340115.dkr.ecr.us-east-1.amazonaws.com/node:22

COPY package.json package-lock.json ./
RUN npm install --omit=dev

COPY . .

RUN npm run build
CMD npm run start -p 3000
