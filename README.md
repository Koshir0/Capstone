# Casting Agency API

## Introduction

The Casting Agency API allows users to manage movies and actors in a casting agency. It provides endpoints for viewing, creating, updating, and deleting movies and actors. The API also supports role-based access control for different user roles.

## Motivation behind the Project

The project aims to create a backend API for a casting agency, enabling efficient management of movie and actor information. Role-based access control ensures that only authorized users can perform specific actions.

## Tech Stack

- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Auth0 for authentication

## Installation

1. Clone the repository:
git clone https://github.com/Koshir0/Capstone.git
cd Capstone
2. Install dependencies:
pip install -r requirements.txt


2. Run tests:
python test_app.py


## Roles and Permissions

The API includes three roles:
- Casting Assistant: Can view movies and actors
- Casting Director: Can view movies and actors, add or delete an actor, and modify actors or movies
- Executive Producer: Has all permissions of a Casting Director, and can also add or delete a movie

## Documentation

API documentation can be found in the `api-reference.md` file. It provides details about available endpoints, request formats, and expected responses.

## Heroku Link

The API is deployed on Heroku. You can access it at [Heroku App Link](https://blooming-sierra-08778-8428bc24e833.herokuapp.com/).


