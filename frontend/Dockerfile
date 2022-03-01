FROM node:14.17.1-alpine

WORKDIR /reactapp

COPY package.json /reactapp

COPY . /reactapp

RUN npm install --silent

CMD ["npm", "start"]