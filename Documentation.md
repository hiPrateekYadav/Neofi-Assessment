# Your Project Name - API Documentation


## Overview

Welcome to the API documentation for Your Project Name. This API provides access to various functionalities related to notes.


## Authentication

These API uses JSON Web Token (JWT) for authentication. Include the JWT token in the `Authorization` header of your requests.

  ```
  Authorization : 'Bearer <access_token>'
  ```


### User Endpoints

#### Signup

- **URL**: `/signup/`
- **Method**: `POST`
- **Description**: Creates new user
- **Authorization**: Not Required
- **Request Example**:
  ```
  {
    "username": "tempo",
    "email" : "tempo@temp.temp",
    "password" : "tempo"
    }
  ```
- **Response Example**:
  ```
    {
        "success": true,
        "message": "Signup successful"
    }
  ```

#### Login

- **URL**: `/login/`
- **Method**: `POST`
- **Description**: Login a user
- **Authorization**: Not Required
- **Request Example**:
  ```
  {
    "identifier": "tempo@temp.temp",
    "password": "tempo"
  }
  ```
- **Response Example**:
  ```
    {
        "success": true,
        "refresh": "eyJhbGciOiJIUz...",
        "access": "eyJhbGciOiJIUz..."
    }
  ```

#### Logout

- **URL**: `/logout/`
- **Method**: `POST`
- **Description**: Logout the user
- **Authorization**: Required
- **Request Example**:
  ```
  {
    "access_token": "your_access_token_here"
  }
  ```
- **Response Example**:
  ```
    {
        "success": true,
        "message": "Logout successful"
    }
  ```

#### Refresh Token

- **URL**: `/token/refresh/`
- **Method**: `POST`
- **Description**: Creates a New Access Token
- **Authorization**: Not Required
- **Request Example**:
  ```
    {
        "refresh" : "your_refresh_token_here"
    }
  ```
- **Response Example**:
  ```
    {
        "access": "eyJhbGciOiJIUz..."
    }
  ```


#### Notes Endpoints

#### Create a Note

- **URL**: `/notes/create/`
- **Method**: `POST`
- **Description**: Creates a New Note
- **Authorization**: Required
- **Request Example**:
  ```
    {
        "content": "test"
    }
  ```
- **Response Example**:
  ```
    {
        "success": true,
        "message": "Note created successfully",
        "note_id": 2
    }
  ```

#### Get a Note

- **URL**: `/notes/{note_id}/`
- **Method**: `GET`
- **Description**: Get details of a Note
- **Authorization**: Required
- **Response Example**:
  ```
    {
        "success": true,
        "note": {
            "id": 1,
            "author": {
                "username": "user1"
            },
            "content": "Your note content here",
            "shared_with": [
                {
                    "username": "user2"
                }
            ],
            "created_at": "2022-01-01T12:00:00Z"
        }
    }
  ```

#### Share Note

- **URL**: `/notes/share/`
- **Method**: `POST`
- **Description**: Give Access of the Note to others
- **Authorization**: Required
- **Request Example**:
  ```
    {
        "note_id": 1,
        "shared_with_usernames": ["user1", "user2"]
    }
  ```
- **Response Example**:
  ```
    {
        "success": true,
        "message": "Note shared successfully"
    }
  ```

#### Update a Note

- **URL**: `/notes/{note_id}/`
- **Method**: `PUT`
- **Description**: Updates Note Content
- **Authorization**: Required
- **Request Example**:
  ```
    {
        "content" : "new content"
    }
  ```
- **Response Example**:
  ```
    {
        "success": true,
        "message": "Note updated successfully",
        "note": {
            "id": 1,
            "author": {
                "username": "user1"
            },
            "content": "new content",
            "shared_with": ["user2"],
            "created_at": "2024-02-25T05:00:53.096851Z"
        }
    }
  ```

#### Get Version History of Note

- **URL**: `/notes/version-history/{note_id}/`
- **Method**: `GET`
- **Description**: Get all history of changes in Note
- **Authorization**: Required
- **Response Example**:
  ```
    {
        "success": true,
        "data": {
            "current_version": {
                "id": 2,
                "author": {
                    "username": "user1"
                },
                "content": "new content",
                "shared_with": [
                    {
                        "username": "user2"
                    },
                    {
                        "username": "user3"
                    }
                ],
                "created_at": "2024-02-25T04:56:24.784460Z"
            },
            "history": [
                {
                    "note": 2,
                    "content": "old content",
                    "updated_at": "2024-02-25T06:44:50.070775Z",
                    "updated_by": {
                        "username": "user2"
                    }
                }
            ]
        }
    }
  ```


