# Mariner Project API

Implementation of a REST API that models users and associated permissions. 

Project was done using Django and the Django-rest-framework libraries.

## Dependencies

This project requires the use of these tools:

* Python 3.9.x ([pyenv](https://github.com/pyenv/pyenv) is suggested to manage python versions)
* poetry (See [poetry](https://python-poetry.org/docs/#installation))
* pre-commit (See [pre-commit installation](https://pre-commit.com/#installation))
* Docker / Docker Compose

### Docker Container Services
The application uses the following containers for deployement.

* Nginx (As a web proxy and load balancer)
* Postgres (Database)
* Django & Gunicorn (WSGI web application)

## Running the Application
Run the following commands from project directory
### Build Images:
```shell
docker-compose -f docker/docker-compose.yml build 
```
### Start services
```shell
docker-compose -f docker/docker-compose.yml up -d
```
### Stop services
```shell
docker-compose -f docker/docker-compose.yml down 
```

## API Documentation

Once you start services, on your browser go to view documentation and schemas:
```shell
http://localhost/api-docs
```

## Test

Test cases uses Pytest library and can be found in project root:
```shell
tests
```