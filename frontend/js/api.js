/**
 * API Client Module (SOP Section 7.6 & 7.7: REST API Integration)
 * Encapsulates all HTTP operations, error handling, and JSON serialization.
 */

const API_BASE = 'http://127.0.0.1:8000/api';

const api = {
    /**
     * Generic helper for fetch requests with standardized error parsing
     */
    async request(endpoint, options = {}) {
        const url = `${API_BASE}${endpoint}`;
        const defaultHeaders = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        };

        const config = {
            ...options,
            headers: {
                ...defaultHeaders,
                ...options.headers,
            },
        };

        try {
            const response = await fetch(url, config);

            // Handle 204 No Content
            if (response.status === 204) {
                return { success: true };
            }

            let data;
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                data = await response.text();
            }

            if (!response.ok) {
                const error = new Error(
                    (data && data.message) || `HTTP Error ${response.status}: ${response.statusText}`
                );
                error.status = response.status;
                error.data = data;
                throw error;
            }

            return data;
        } catch (error) {
            console.error(`API Error on [${config.method || 'GET'} ${endpoint}]:`, error);
            throw error;
        }
    },

    /**
     * Check backend connectivity (SOP Section 17: Checklist)
     */
    async checkHealth() {
        try {
            const res = await fetch(`${API_BASE}/departments/`, { method: 'GET' });
            return res.ok;
        } catch (e) {
            return false;
        }
    },

    /**
     * Read All Students with optional search and filter parameters (SOP Section 7.6 & 8)
     */
    async getStudents(filters = {}) {
        const query = new URLSearchParams();
        if (filters.search) query.append('search', filters.search);
        if (filters.department) query.append('department', filters.department);
        if (filters.status) query.append('status', filters.status);

        const queryString = query.toString() ? `?${query.toString()}` : '';
        const data = await this.request(`/students/${queryString}`);
        // Support either direct list or paginated response
        return Array.isArray(data) ? data : (data.results || []);
    },

    /**
     * Read One Student by ID (SOP Section 7.6 & 8)
     */
    async getStudent(id) {
        return await this.request(`/students/${id}/`);
    },

    /**
     * Create New Student (SOP Section 7.6 & 8)
     */
    async createStudent(studentData) {
        return await this.request('/students/', {
            method: 'POST',
            body: JSON.stringify(studentData),
        });
    },

    /**
     * Update Existing Student (SOP Section 7.6 & 8)
     */
    async updateStudent(id, studentData) {
        return await this.request(`/students/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(studentData),
        });
    },

    /**
     * Delete Student (SOP Section 7.6 & 8)
     */
    async deleteStudent(id) {
        return await this.request(`/students/${id}/`, {
            method: 'DELETE',
        });
    },

    /**
     * Fetch all Departments for dropdown options
     */
    async getDepartments() {
        const data = await this.request('/departments/');
        return Array.isArray(data) ? data : (data.results || []);
    },

    /**
     * Fetch aggregate statistics for dashboard
     */
    async getStats() {
        try {
            return await this.request('/students/stats/');
        } catch (e) {
            return null;
        }
    }
};

window.api = api;
