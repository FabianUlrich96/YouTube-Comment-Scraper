FROM node:14.17.1-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./

COPY package-lock.json ./

RUN cd /app; npm install --production
RUN cd /app; npm install react-scripts@5.0.0 -g --silent

COPY . /app

COPY . ./

CMD ["npm","start"]