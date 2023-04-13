# Wroclaw-Galleries-REST-API

This is a RESTful API developed with Flask and SQLAlchemy. It allows users to register, and they will receive a welcome email upon successful registration. Emails are sent via a Queue using "rq" and "redis". The project also fully utilizes flask_jwt_extended for token-based authentication. The required environment variables can be found in the .env file, which includes the:
- DATABASE_URL
- MAILGUN_API_KEY
- MAILGUN_DOMAIN
- REDIS_URL
- JWT_SECRET_KEY 

Swagger documentation for the API can be found at /swagger-ui.

## Getting Started

To get started, clone this repository and create a virtual environment using your preferred tool (e.g., venv, pipenv, conda). Then, install the necessary dependencies using:

**pip install -r requirements.txt**

You will also need to set the necessary environment variables. You can find a sample .env file in the project root directory. Rename it to .env and set the appropriate values for your environment. Note that if DATABASE_URL is not specified, the code will create a new database locally.

To run the API, execute:

- **flask db init**
- **flask migrate**
- **flask run**

This will start the Flask development server, and you can access the API at http://localhost:5000.

## Docker
Alternatively, you can use Docker to run the API. Ensure that Docker is installed and running, then build the Docker image:

**docker build -t wroclaw-galleries-rest-api .**

This will build the Docker image with the name "wroclaw-galleries-rest-api". Then, you can run the container using:

**docker run -dp 5000:5000 -w /app -v "$(pwd):/app" wroclaw-galleries-rest-api sh -c "flask run --host 0.0.0.0"**

This will run the container and map the container's port 5000 to your local machine's port 5000. It will also mount the current directory to the container's /app directory and run the Flask development server inside the container.

Additionally, you can run a second container for sending emails using the following commands:

- **docker build -t wroclaw-galleries-rest-api-email .**
- **docker run -w /app wroclaw-galleries-rest-api-email sh -c "rq worker -u REDIS_URL emails"**

This will build the Docker image with the name "wroclaw-galleries-rest-api-email". Then, it will run the container and execute the "rq worker" command to process the email queue. You will need to replace REDIS_URL with the appropriate Redis URL for your environment.

Link example: __rediss://example_example@frankfurt-redis.render.com:1111__

## Authentication
This API utilizes token-based authentication using flask_jwt_extended. To obtain a token, send a POST request to the /auth/login endpoint with valid credentials. The API will respond with a JWT token that can be used to access protected endpoints.

## Sample Response
After adding a new item to the main table, the API will respond with a JSON object in the following format:

![ogólnie](https://user-images.githubusercontent.com/121942715/231760771-013e0cdb-e4e5-4c80-a401-26a6050cd76a.png)

You can use this sample response to understand how the API works and to see what kind of data you can expect to receive from it. The JSON object contains various fields, such as the name, city, street, postal code, and opening/closing times of the venue, as well as the number of parking spaces available and a URL to its location on Google Maps.

## Swagger Documentation
Swagger documentation for the API can be found at /swagger-ui. This documentation provides detailed information on the available endpoints and request/response formats.
