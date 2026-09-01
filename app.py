from flask import Flask, jsonify, request, abort, make_response
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)

# Disable strict slashes so that both /api/courses and /api/courses/ match the same route
app.url_map.strict_slashes = False

# ==============================================================================
# CORS Configuration & Preflight Handling
# ==============================================================================
# Configure allowed frontend origins from environment variables or sensible defaults
FRONTEND_ORIGIN = os.getenv('FRONTEND_URL', 'http://localhost:3000')

ALLOWED_ORIGINS = [
    FRONTEND_ORIGIN,
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://*.run.app"
]

# Initialize CORS with route-specific granular controls and credentials support
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ALLOWED_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Accept"],
            "supports_credentials": True,
            "max_age": 3600
        }
    }
)

# Global Preflight Interceptor: Ensures OPTIONS requests never return 404
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.status_code = 204
        origin = request.headers.get('Origin', '*')
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Max-Age'] = '3600'
        return response

# Ensure CORS headers on all outbound responses (including errors)
@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept'
    return response

DATA_FILE = 'data/courses.json'

# Ensure the data directory and file exist
os.makedirs(os.path.dirname(DATA_FILE) or '.', exist_ok=True)
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

# Endpoint to add a new course (POST /api/courses or /api/courses/)
@app.route('/api/courses', methods=['POST'])
@app.route('/api/courses/', methods=['POST'])
def add_course():
    data = request.json or {}
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

# Endpoint to get all courses (GET /api/courses or /api/courses/)
@app.route('/api/courses', methods=['GET'])
@app.route('/api/courses/', methods=['GET'])
def get_courses():
    courses = read_data()
    return jsonify(courses), 200

# Endpoint to get course statistics (GET /api/courses/stats or /api/courses/stats/)
@app.route('/api/courses/stats', methods=['GET'])
@app.route('/api/courses/stats/', methods=['GET'])
def get_course_stats():
    courses = read_data()
    
    # Initialize counts for each valid status
    status_counts = {
        'Not Started': 0,
        'In Progress': 0,
        'Completed': 0
    }
    
    # Aggregate stats
    for course in courses:
        status = course.get('status')
        if status in status_counts:
            status_counts[status] += 1

    stats = {
        'total_courses': len(courses),
        'by_status': status_counts
    }
    
    return jsonify(stats), 200

# Endpoint to get a specific course by ID (GET /api/courses/<id>)
@app.route('/api/courses/<int:course_id>', methods=['GET'])
@app.route('/api/courses/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    courses = read_data()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course is None:
        abort(404, description="Course not found")
    
    return jsonify(course), 200

# Endpoint to update an existing course by ID (PUT /api/courses/<id>)
@app.route('/api/courses/<int:course_id>', methods=['PUT'])
@app.route('/api/courses/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    courses = read_data()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course is None:
        abort(404, description="Course not found")

    # Update course fields if provided in the request
    data = request.json or {}
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
@app.route('/api/courses/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    courses = read_data()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course is None:
        abort(404, description="Course not found")
    
    courses.remove(course)
    write_data(courses)
    return jsonify({'result': 'Course deleted'}), 204

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
