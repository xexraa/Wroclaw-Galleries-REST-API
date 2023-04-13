# CONTRIBUTING

## How to run the Dockerfile locally


**Main build:**

docker build -t wroclaw-galleries-rest-api .

__Run build with this settings:__

docker run -dp 5000:5000 -w /app -v "$(pwd):/app" wroclaw-galleries-rest-api sh -c "flask run --host 0.0.0.0"


**Build for email sending:**

docker build -t wroclaw-galleries-rest-api-email .

__Run email-build with this settings:__

docker run -w /app wroclaw-galleries-rest-api-email sh -c "rq worker -u YOUR-REDIS-LINK emails"
