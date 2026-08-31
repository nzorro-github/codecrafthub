from flask import Flask, jsonify, request, abort
import json
import os

app = Flask(__name__)
DATA_FILE = 'data/courses.json'

# Helper function to read data from the JSON file
def read_data():
    if not os.path.exists(DATA_FILE):
        return []  # Return an empty list if the file does not exist
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

# Helper function to write data to the JSON file
def write_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Endpoint to get all courses
@app.route('/courses', methods=['GET'])
def get_courses():
    courses = read_data()
    return jsonify(courses), 200

# Endpoint to add a new course
@app.route('/courses', methods=['POST'])
def add_course():
    new_course = request.json
    courses = read_data()
    
    # Add an ID for tracking (just using length for simplicity)
    new_course['id'] = len(courses) + 1
    courses.append(new_course)
    write_data(courses)
    
    return jsonify(new_course), 201

# Endpoint to get a specific course by ID
@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    courses = read_data()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course is None:
        abort(404)
    
    return jsonify(course), 200

# Endpoint to update an existing course
@app.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    courses = read_data()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course is None:
        abort(404)
    
    updated_course = request.json
    course.update(updated_course)
    write_data(courses)
    
    return jsonify(course), 200

# Endpoint to delete a course
@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    courses = read_data()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course is None:
        abort(404)
    
    courses.remove(course)
    write_data(courses)
    
    return jsonify({'result': 'Course deleted'}), 204

if __name__ == '__main__':
    app.run(debug=True)