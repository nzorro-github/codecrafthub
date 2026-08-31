# Running Tests manually

Before running these tests, start your Flask app locally (it typically runs on [http://127.0.0.1:5000](http://127.0.0.1:5000) or http://localhost:5000).

## Happy Path Tests (Successful Operations)
1. Create a New Course (POST)
Creates a course record and returns the created object with a generated ID and timestamp.

```BASH
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Fundamentals",
    "description": "Learn basic to intermediate Python concepts.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }'
  ```


Expected Response (201 Created):

```JSON
{
  "created_at": "2026-08-31T14:50:00.123456",
  "description": "Learn basic to intermediate Python concepts.",
  "id": 1,
  "name": "Python Fundamentals",
  "status": "Not Started",
  "target_date": "2026-12-31"
}
```

2. Get All Courses (GET)
Retrieves a list of all courses currently stored.

```BASH
curl -X GET http://127.0.0.1:5000/api/courses
```


Expected Response (200 OK):

```JSON
[
  {
    "created_at": "2026-08-31T14:50:00.123456",
    "description": "Learn basic to intermediate Python concepts.",
    "id": 1,
    "name": "Python Fundamentals",
    "status": "Not Started",
    "target_date": "2026-12-31"
  }
]
```

3. Get Course by ID (GET)
Fetches a single course using its specific ID (1).

```BASH
curl -X GET http://127.0.0.1:5000/api/courses/1
```
Expected Response (200 OK):
```JSON
{
  "created_at": "2026-08-31T14:50:00.123456",
  "description": "Learn basic to intermediate Python concepts.",
  "id": 1,
  "name": "Python Fundamentals",
  "status": "Not Started",
  "target_date": "2026-12-31"
}
```

4. Update Course (PUT)
Updates specific attributes of course 1.
```BASH
curl -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "In Progress",
    "description": "Updated course description."
  }'
  ```
Expected Response (200 OK):
```JSON
{
  "created_at": "2026-08-31T14:50:00.123456",
  "description": "Updated course description.",
  "id": 1,
  "name": "Python Fundamentals",
  "status": "In Progress",
  "target_date": "2026-12-31"
}
```

5. Delete Course (DELETE)
Removes course 1 from the system.

```BASH
curl -i -X DELETE http://127.0.0.1:5000/api/courses/1
```

Expected Response (204 No Content):
(Returns an empty body with HTTP status 204)

## Error Scenario Tests

1. Missing Required Fields on Creation
Fails when required fields (like target_date and status) are missing from the payload.
```BASH
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Incomplete Course",
    "description": "Missing date and status."
  }'
  ```

Expected Response (400 Bad Request):
```JSON
{
  "message": "Missing required fields: name, description, target_date, status"
}
```
2. Invalid Status Value on Creation
Fails when passing a status string outside ['Not Started', 'In Progress', 'Completed'].

```BASH
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Status Course",
    "description": "Testing invalid status.",
    "target_date": "2026-12-31",
    "status": "Finished"
  }'
  ```
  Expected Response (400 Bad Request):
  
  ```JSON
  {
  "message": "Invalid status value, must be one of: Not Started, In Progress, Completed"
}
```

3. Invalid Status Value on Update
Fails when attempting to update a course to an invalid status string.

```BASH
curl -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Archived"
  }'
```
Expected Response (400 Bad Request):
```JSON
{
  "message": "Invalid status value, must be one of: Not Started, In Progress, Completed"
}
```

4. Course Not Found (GET / PUT / DELETE)
Fails when referencing an ID that does not exist in the database (e.g., ID 999).

```BASH
curl -X GET http://127.0.0.1:5000/api/courses/999
```
Expected Response (404 Not Found):

```JSON
{
  "message": "Course not found"
}
```
