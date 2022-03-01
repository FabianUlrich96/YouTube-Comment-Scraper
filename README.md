# YouTube-Comment-Scraper

## Built With

* [Bootstrap](https://react-bootstrap.github.io/)
* [Celery](https://docs.celeryproject.org/en/stable/)
* [Docker](https://www.docker.com)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [MySQL](https://www.mysql.com/)
* [Node.js](https://nodejs.org/en/)
* [phpMyAdmin](https://www.phpmyadmin.net/)
* [React.js](https://reactjs.org)
* [Redis](https://redis.io/)
* [SQLAlchemy](https://www.sqlalchemy.org/)

## Getting Started

### Requirements

* [Docker](https://www.docker.com/)
* On Windows: Install [WSL](https://docs.docker.com/desktop/windows/wsl/)

### Setup

1. Clone the repository
```
git clone https://github.com/FabianUlrich96/YouTube-Comment-Scraper
```
2. Navigate to the repository folder
3. Build the application using Docker
```
docker-compose up --build
```
Add -d to run the container detached

To stop the application run 
```
docker-compose down
```

To start it up again the --build flag is not needed anymore

## Access Information:
* Frontend port: 1010
* phpMyAdmin port 1030

* MYSQL_DATABASE: 'dataapi'
* MYSQL_USER: 'dataapi'
* MYSQL_PASSWORD: 'fnmwm4d833834erjn'
* MYSQL_ROOT_PASSWORD: 'CVC93DA3D8kksa5M'

The application has a simple user authentication system, to gain access simply create a new user using the phpMyAdmin interface. 

All the access information can be changed in the [docker-compose file](../main/docker-compose.yml)

