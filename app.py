from flask import Flask, jsonify, request, abort
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data/courses.json'

# Ensure the data file exists, create it if it doesn't
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as file:
        json.dump([], file)  # Initialize with an empty list

# Read data from JSON file
def read_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except Exception as e:
        abort(500, description="Error reading data: " + str(e))

# Write data to JSON file
def write_data(data):
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        abort(500, description="Error writing data: " + str(e))

# Helper function to generate a new course ID
def generate_id(courses):
    if not courses:
        return 1
    return max(course['id'] for course in courses) + 1

# Endpoint to add a new course (POST /api/courses)
@app.route('/api/courses', methods=['POST'])
def add_course():
    data = request.json
    # Check for required fields
    required_fields = ['name', 'description', 'target_date', 'status']
    if not all(field in data for field in required_fields):
        abort(400, description="Missing required fields: " + ", ".join(required_fields))

    # Validate status
    valid_statuses = ['Not Started', 'In Progress', 'Completed']
    if data['status'] not in valid_statuses:
        abort(400, description="Invalid status value, must be one of: " + ", ".join(valid_statuses))
    
    courses = read_data()

    # Create new course
    new_course = {
        'id': generate_id(courses),
        'name': data['name'],
        'description': data['description'],
        'target_date': data['target_date'],
        'status': data['status'],
        'created_at': datetime.utcnow().isoformat()
    }
    courses.append(new_course)
    write_data(courses)

    return jsonify(new_course), 201

# Endpoint to get all courses (GET /api/courses)
@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = read_data()
    return jsonify(courses), 200

# Endpoint to get a specific course by ID (GET /api/courses/<id>)
@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    courses = read_data()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course is None:
        abort(404, description="Course not found")
    
    return jsonify(course), 200

# Endpoint to update an existing course by ID (PUT /api/courses/<id>)
@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    courses = read_data()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course is None:
        abort(404, description="Course not found")

    # Update course fields if provided in the request
    data = request.json
    if 'name' in data:
        course['name'] = data['name']
    if 'description' in data:
        course['description'] = data['description']
    if 'target_date' in data:
        course['target_date'] = data['target_date']
    if 'status' in data:
        if data['status'] not in ['Not Started', 'In Progress', 'Completed']:
            abort(400, description="Invalid status value, must be one of: Not Started, In Progress, Completed")
        course['status'] = data['status']

    write_data(courses)
    return jsonify(course), 200

# Endpoint to delete a course by ID (DELETE /api/courses/<id>)
@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    courses = read_data()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course is None:
        abort(404, description="Course not found")
    
    courses.remove(course)
    write_data(courses)
    return jsonify({'result': 'Course deleted'}), 204

if __name__ == '__main__':
    app.run(debug=True)
    