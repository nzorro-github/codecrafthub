# CodeCraftHub

CodeCraftHub is a simple personalized learning platform designed for developers to track courses they want to learn. The platform allows users to manage course information, including course name, description, target completion date, and current status. This project is built using Python and Flask, focusing on creating a basic REST API.

## Features

- Track course name, description, target completion date, and status (Not Started, In Progress, Completed).
- Simple data storage using a JSON file (no databases required).
- RESTful API for managing courses.

## Project Structure
```
code_craft_hub/
│
├── app.py                      # Main application file
├── data/
│   └── courses.json            # JSON file to store course data
├── requirements.txt            # Python package requirements
└── README.md                   # Project documentation
```

## Requirements

- Python 3.6 or higher
- Flask

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/nzorro-github/codecrafthub.git
   cd codecrafthub
   

### Create a virtual environment (optional but recommended):

```python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install the required packages:

```pip install -r requirements.txt```

### Running the Application

Ensure your directory structure is correct with the
data/courses.json
file present. You can start with an empty JSON file:
{}

### Run the application:

```BASH
python app.py
```

### Access the API:

The application will run on
http://127.0.0.1:5000/
. You can use Postman or curl to interact with the API.

## API Endpoints

GET /api/courses: Retrieve the list of all courses.
POST /api/courses: Add a new course. (Example data format:
{"name": "Course Name", "description": "Course Description", "target_date": "YYYY-MM-DD", "status": "Not Started"}
)
GET /api/courses/<course_id>: Retrieve a specific course by ID.
PUT /api/courses/<course_id>: Update an existing course.
DELETE /api/courses/<course_id>: Delete a course.

## Testing the Endpoints

You can use tools like Postman or
```curl```
to test the API endpoints:

### GET All Courses:

```curl http://127.0.0.1:5000/api/courses```

### Add a Course:

```curl -X POST http://127.0.0.1:5000/api/courses -H "Content-Type: application/json" -d '{"name": "Learn Python", "description": "A comprehensive Python course.", "target_completion_date": "2023-12-31", "status": "Not Started"}'```

## Contributing

If you would like to contribute to CodeCraftHub, feel free to fork the repository and submit a pull request.

License

This project is open-source and available under the MIT License.

