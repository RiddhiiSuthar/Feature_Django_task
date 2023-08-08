# Base Image
FROM node:14

# Set working directory
WORKDIR /app

# Add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# Install dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@4.0.3 -g --silent

# Add app
COPY . ./frontend

# Start the app 
CMD ["npm", "start"]

# Expose port
EXPOSE 3000
