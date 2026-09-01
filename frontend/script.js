const API_URL = 'http://localhost:5000/api/courses';
let currentCourses = [];

// UI Elements
const notificationEl = document.getElementById('notification');
const loaderEl = document.getElementById('loader');
const courseTableBody = document.getElementById('courseTableBody');
const editModal = document.getElementById('editModal');

// Utility: Show Notifications
function showNotification(message, type = 'success') {
    notificationEl.textContent = message;
    notificationEl.className = type === 'success' ? 'notify-success' : 'notify-error';
    notificationEl.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
    setTimeout(() => { notificationEl.style.display = 'none'; }, 5000);
}

// Utility: Toggle Loader
function toggleLoader(show) {
    loaderEl.style.display = show ? 'block' : 'none';
}

// Utility: Format Date
function formatDate(isoString) {
    if (!isoString) return 'N/A';
    const date = new Date(isoString);
    return date.toLocaleDateString();
}

// API Call Wrapper
async function apiCall(endpoint, method = 'GET', body = null) {
    toggleLoader(true);
    try {
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        if (body) options.body = JSON.stringify(body);

        const response = await fetch(`${API_URL}${endpoint}`, options);
        
        // Handle 204 No Content for DELETE
        if (response.status === 204) return null;

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.description || data.message || 'API request failed');
        }
        
        return data;
    } catch (error) {
        showNotification(error.message, 'error');
        throw error;
    } finally {
        toggleLoader(false);
    }
}

// 1. GET - Fetch All Courses
async function fetchCourses() {
    try {
        const courses = await apiCall('');
        currentCourses = courses;
        renderTable(courses);
    } catch (error) {
        courseTableBody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:red;">Failed to load courses. Is the backend running?</td></tr>';
    }
}

// Render Table
function renderTable(courses) {
    courseTableBody.innerHTML = '';
    if (courses.length === 0) {
        courseTableBody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No courses found. Create one above!</td></tr>';
        return;
    }

    courses.forEach(course => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>#${course.id}</strong></td>
            <td>
                <strong>${course.name}</strong>
                <div style="font-size: 0.85rem; color: var(--text-light); margin-top: 4px;">${course.description}</div>
                <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">Created: ${formatDate(course.created_at)}</div>
            </td>
            <td>${course.target_date}</td>
            <td>
                <span style="font-weight:600; color: ${
                    course.status === 'Completed' ? 'var(--primary)' : 
                    course.status === 'In Progress' ? 'var(--success)' : 'var(--text-light)'
                }">${course.status}</span>
            </td>
            <td>
                <div class="actions">
                    <button class="btn btn-success" onclick="openModal(${course.id})">Edit</button>
                    <button class="btn btn-delete" onclick="deleteCourse(${course.id})">Delete</button>
                </div>
            </td>
        `;
        courseTableBody.appendChild(tr);
    });
}

// 2. POST - Create New Course
document.getElementById('addCourseForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const newCourse = {
        name: document.getElementById('name').value.trim(),
        description: document.getElementById('description').value.trim(),
        target_date: document.getElementById('target_date').value,
        status: document.getElementById('status').value
    };

    try {
        await apiCall('', 'POST', newCourse);
        showNotification('Course created successfully!');
        document.getElementById('addCourseForm').reset();
        fetchCourses();
    } catch (error) {
        // Error handled in apiCall
    }
});

// Modal Logic
function openModal(id) {
    const course = currentCourses.find(c => c.id === id);
    if (!course) {
        showNotification('Course data not found locally.', 'error');
        return;
    }

    document.getElementById('edit_id').value = course.id;
    document.getElementById('edit_name').value = course.name;
    document.getElementById('edit_description').value = course.description;
    document.getElementById('edit_target_date').value = course.target_date;
    document.getElementById('edit_status').value = course.status;

    editModal.style.display = 'flex';
}

function closeModal() {
    editModal.style.display = 'none';
    document.getElementById('editCourseForm').reset();
}

// 3. PUT - Update Course
document.getElementById('editCourseForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('edit_id').value;
    
    const updatedCourse = {
        name: document.getElementById('edit_name').value.trim(),
        description: document.getElementById('edit_description').value.trim(),
        target_date: document.getElementById('edit_target_date').value,
        status: document.getElementById('edit_status').value
    };

    try {
        await apiCall(`/${id}`, 'PUT', updatedCourse);
        showNotification('Course updated successfully!');
        closeModal();
        fetchCourses();
    } catch (error) {
        // Error handled in apiCall
    }
});

// 4. DELETE - Remove Course
async function deleteCourse(id) {
    if (!confirm(`Are you sure you want to delete Course #${id}? This action cannot be undone.`)) {
        return;
    }

    try {
        await apiCall(`/${id}`, 'DELETE');
        showNotification('Course deleted successfully!');
        fetchCourses();
    } catch (error) {
        // Error handled in apiCall
    }
}

// Initialize App
document.addEventListener('DOMContentLoaded', fetchCourses);