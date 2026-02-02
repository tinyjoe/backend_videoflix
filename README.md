# Videoflix Backend 

A modern **Django-based backend** for displaying and converting videos.  
Built for scalability using Docker, Redis, Django RQ and FFMPEG.


## Django Project

The project is called 'backend_videoflix', but project files are stored in the 'core' folder. Please refer to 'core/settings.py' for further details.


## Requirements

+ RESTful API with Django REST Framework  
+ JWT Authentication (SimpleJWT)  
+ Video transcoding via FFMPEG  
+ Asynchronous background jobs using Django RQ  
+ Fully dockerized setup  
+ Environment-based configuration  
+ Ready for cloud deployment


## Technologies

backend_kanmind uses the following technologies and tools: 

![Python](https://img.shields.io/badge/python-3.13-blue)
![Django](https://img.shields.io/badge/django-5.2.4-green)
![DRF](https://img.shields.io/badge/django--restframework-latest-red)
![Docker](https://img.shields.io/badge/docker-ready-blue)



## Tech Stack

- Python 3.13
- Django
- Django REST Framework
- SimpleJWT
- FFMPEG
- Django RQ
- Redis
- PostgreSQL
- Docker & Docker Compose


## Django Apps

Apps include: 

+ auth_app - this is for signup and login logic that don't require a token or authenticated user. It's also possible to activate an account and reset the password through an link sent in an email.
+ videoflix_app - this is for the data model of Videos and the logic for uploading Videos in the admin panel, converting and viewing videos in different resolutions. Can only be accessed by authenticated users.


## Installation

Clone the repostiory:
```sh
git clone https://github.com/tinyjoe/backend_videoflix.git
cd backend_videoflix
```

setup environment
```sh
cp .env.template .env
```

Run with Docker
```sh
docker-compose up --build
```

## Database Migrations

Run migrations
```sh
docker-compose exec backend python manage.py migrate
```

Create new migrations
After changing models:
```sh
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

Create Superuser
```
docker-compose exec backend python manage.py createsuperuser
```

Reset Database
```
docker-compose down -v
docker-compose up --build
docker-compose exec backend python manage.py migrate
```


## Upload and manage Videos in the Admin Panel
In the Admin Panel you can upload a video with title, description, category and thumbnail. 
The uploades video gets converted in different resolutions (480p, 720p, 1080p) as well as in different HLS segments.

  
