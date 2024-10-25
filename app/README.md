# API zahageek 

## base url
https://zahageek-back.onrender.com/

## Endpoint

### login /api/auth/login method: POST
#### Query
```json
{
    "email": "youremai@domain.com",
    "password": "yourpassword"
}
```
#### Response
```json
{
    "id": 1,
    "email": "youremai@domain.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InlvdXJlbWFpQGRvbWFpbi5jb20iLCJleHAiOjE3MTkwNDgzOTd9.QYbq8REZYtYVFP1DjKFe9A08df8RrX0opzMJnV2tjI8"
}
```

### sign up /api/auth/register method: POST
#### Query
```json
{
    "firt_name": "First Name",
    "last_name": "Last Name",
    "email": "youremai@domain.com",
    "password": "yourpassword"
}
```
#### Response
```json
{
    "id": 1,
    "first_name": "",
    "last_name": "Last Name",
    "email": "youremai@domain.com",
    "profile_picture": "/images/Profile_avatar_placeholder_large.png"
}
```

### Profile /api/auth/profile method: GET
* Need authorization : Token xxxxxxxxxxxxxxxxx
#### Response
```json
{
    "id": 2,
    "first_name": "John",
    "last_name": "doe",
    "email": "johndoe@gmail.com",
    "profile_picture": "http://localhost:8000/images/Profile_avatar_placeholder_large.png"
}
```

### Profile /api/auth/profile method: PATCH
#### Query exemple to modify first_name and last_name
```json
{
    "first_name": "Johnny",
    "last_name": "Doe"
}
```
#### Response
```json
{
    "id": 2,
    "first_name": "Johnny",
    "last_name": "Doe",
    "email": "johndoe@gmail.com",
    "profile_picture": "http://localhost:8000/images/Profile_avatar_placeholder_large.png"
}
```

### Get Level /api/glish/levels method: GET
* Need authorizations Token xxxxxxxxxx
#### Response
```json
[
    {
        "id": 1,
        "order": 1,
        "name": "Level 1",
        "desc": "Level 1 desc",
        "min_point": 0
    },
    ...
]
```

### Get Modules by level ID /api/glish/levels/<int:level_id>/modules method: GET
* Need authorizations Token xxxxxxxxxx
#### Response
```json
[
    {
        "id": 1,
        "order": 1,
        "name": "Introduction to English",
        "desc": "desc",
        "level": 1
    },
    ...
]
```

### Get Modules elements by module ID /api/glish/levels/modules/<int:module_id>/module_elements method: GET
* Need authorizations Token xxxxxxxxxx
#### Response
```json
[
    {
        "id": 1,
        "order": 1,
        "name": "Alphabet and basic phonetics",
        "desc": "desc",
        "module": 1
    }
    ...
]
```

