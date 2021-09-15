# Jungle Devs - Django Backend Challenge
## About The Project

This API was implemented using the Django web framework.

### Prerequisites
* Docker
* Docker Compose

### Installation
1. Build the project using the default compose file and run services in detached mode
```sh
docker-compose up --build -d
```
2. Migrate development database
```sh
docker-compose exec web python manage.py migrate
```
3. Create production database
```sh
docker-compose exec db su postgres -c 'createdb -U user jungle'
```
4. Stop the services and start running production server
```sh
docker-compose down && docker-compose -f docker-compose.prod.yml up --build -d
```
5. Migrate production database
```sh
docker-compose exec web python manage.py migrate
```
6. Collect static files in one folder
```sh
docker-compose exec web python manage.py collectstatic
```
7. Stop services
```sh
docker-compose -f docker-compose.prod.yml down
```

### Usage
1. Execute one of the following commands to run either the development or production servers, in that respective order:
   * If you wish to visualize the output, simply remove the "-d" flag from either command. 
```sh
docker-compose up -d
```
```sh
docker-compose -f docker-compose.prod.yml up -d
```

2. Access API documentation on <http://localhost:8001>

### Comments
* Database credentials were defined as "user" and "password" for the sake of simplicity.
* The environment files are included in source control for the sake of practicity, as they contain sensitive data that normaly shouldn't be public.