# Movie Recommendation System API Reference

## Introduction

The Movie Recommendation System API provides endpoints for users to interact with the recommendation system and receive personalized movie recommendations. This document outlines the available endpoints, request formats, and expected responses.

## Base URL

The base URL for the Movie Recommendation System API is:

https://capstone.herokuapp.com/api/v1


## Endpoints

### `GET /movies`

Retrieve a list of recommended movies for the user.

#### Request

- Method: GET
- Endpoint: `/movies`
- Parameters: None
- Headers: None

#### Response

- Status Code: 200 OK
- Content: JSON array of recommended movie objects

Example Response:

```json
[
  {
    "title": "Inception",
    "year": 2010,
    "genre": "Sci-Fi",
    "rating": 8.8
  },
  {
    "title": "The Shawshank Redemption",
    "year": 1994,
    "genre": "Drama",
    "rating": 9.3
  },
  // ...
]




POST /rate

Submit a user's rating for a movie.
Request

    Method: POST
    Endpoint: /rate
    Parameters: None
    Headers:
        Content-Type: application/json


Request Body:
{
  "movie_id": 123,
  "rating": 4
}


Response

    Status Code: 201 Created
    Content: JSON object with success message

Example Response:


{
  "message": "Rating submitted successfully."
}


Error Handling

The API handles common errors and returns appropriate error responses with corresponding status codes and messages. Possible error status codes include 400 (Bad Request), 404 (Not Found), and 500 (Internal Server Error).