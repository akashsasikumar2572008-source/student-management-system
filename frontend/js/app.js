/**
 * Application Controller (SOP Section 7.4, 7.7, 8 & 9)
 * Handles UI interactions, client-side validation, rendering, and modal management.
 */

document.addEventListener('DOMContentLoaded', () => {
    // State management
    const state = {
        students: [],
        departments: [],
        filters: {
            search: '',
            department: '',
            status: ''
        },
        editingStudentId: null,
        deletingStudentId: null,
        searchTimeout: null,
    };

    // DOM Elements
    const elements = {
        connectionStatus: document.getElementById('connectionStatus'),
        studentsTable: document.getElementById('studentsTable'),
        studentsTableBody: document.getElementById('studentsTableBody'),
        loadingIndicator: document.getElementById('loadingIndicator'),
        emptyState: document.getElementById('emptyState'),
        emptyStateMessage: document.getElementById('emptyStateMessage'),
        recordsCount: document.getElementById('recordsCount'),
        refreshBtn: document.getElementById('refreshBtn'),

        // Stats
        statTotalStudents: document.getElementById('statTotalStudents'),
        statActiveStudents: document.getElementById('statActiveStudents'),
        statAvgGPA: document.getElementById('statAvgGPA'),
        statTotalDepts: document.getElementById('statTotalDepts'),

        // Search & Filters
        searchInput: document.getElementById('searchInput'),
        clearSearchBtn: document.getElementById('clearSearchBtn'),
        departmentFilter: document.getElementById('departmentFilter'),
        statusFilter: document.getElementById('statusFilter'),
        resetFiltersBtn: document.getElementById('resetFiltersBtn'),

        // Modal
        studentModal: document.getElementById('studentModal'),
        modalTitle: document.getElementById('modalTitle'),
        studentForm: document.getElementById('studentForm'),
        formStudentIdPK: document.getElementById('formStudentIdPK'),
        addStudentBtn: document.getElementById('addStudentBtn'),
        closeModalBtn: document.getElementById('closeModalBtn'),
        cancelModalBtn: document.getElementById('cancelModalBtn'),
        saveStudentBtn: document.getElementById('saveStudentBtn'),
        saveBtnText: document.getElementById('saveBtnText'),
        saveBtnSpinner: document.getElementById('saveBtnSpinner'),
        formErrorAlert: document.getElementById('formErrorAlert'),

        // Form Fields
        fieldStudentId: document.getElementById('fieldStudentId'),
        fieldFirstName: document.getElementById('fieldFirstName'),
        fieldLastName: document.getElementById('fieldLastName'),
        fieldEmail: document.getElementById('fieldEmail'),
        fieldPhone: document.getElementById('fieldPhone'),
        fieldDepartment: document.getElementById('fieldDepartment'),
        fieldEnrollmentDate: document.getElementById('fieldEnrollmentDate'),
        fieldGPA: document.getElementById('fieldGPA'),
        fieldStatus: document.getElementById('fieldStatus'),

        // Delete Modal
        deleteModal: document.getElementById('deleteModal'),
        deleteStudentName: document.getElementById('deleteStudentName'),
        confirmDeleteBtn: document.getElementById('confirmDeleteBtn'),
        cancelDeleteBtn: document.getElementById('cancelDeleteBtn'),
        closeDeleteModalBtn: document.getElementById('closeDeleteModalBtn'),

        // Toast
        toastContainer: document.getElementById('toastContainer'),
    };

    // ==========================================
    // INITIALIZATION & CONNECTION CHECK
    // ==========================================
    async function init() {
        attachEventListeners();
        checkConnection();
        await loadDepartments();
        await loadStudents();
        await loadStats();
    }

    async function checkConnection() {
        const isOnline = await api.checkHealth();
        if (isOnline) {
            elements.connectionStatus.className = 'status-indicator status-online';
            elements.connectionStatus.querySelector('.status-label').textContent = 'API Connected';
        } else {
            elements.connectionStatus.className = 'status-indicator status-offline';
            elements.connectionStatus.querySelector('.status-label').textContent = 'Backend Offline';
            showToast('Unable to connect to Django API backend at http://127.0.0.1:8000. Please ensure the server is running.', 'error', 6000);
        }
    }

    // ==========================================
    // DATA FETCHING & RENDERING
    // ==========================================
    async function loadDepartments() {
        try {
            const depts = await api.getDepartments();
            state.departments = depts;

            // Populate filter dropdown
            elements.departmentFilter.innerHTML = '<option value="">All Departments</option>';
            // Populate form dropdown
            elements.fieldDepartment.innerHTML = '<option value="">Select Department</option>';

            depts.forEach(d => {
                const optFilter = document.createElement('option');
                optFilter.value = d.id;
                optFilter.textContent = `${d.name} (${d.code})`;
                elements.departmentFilter.appendChild(optFilter);

                const optForm = document.createElement('option');
                optForm.value = d.id;
                optForm.textContent = `${d.name} (${d.code})`;
                elements.fieldDepartment.appendChild(optForm);
            });

            elements.statTotalDepts.textContent = depts.length;
        } catch (error) {
            console.error('Failed to load departments:', error);
        }
    }

    async function loadStudents() {
        showLoading(true);
        try {
            const students = await api.getStudents(state.filters);
            state.students = students;
            renderStudentsTable(students);
            elements.recordsCount.textContent = students.length;
        } catch (error) {
            renderErrorState(error.message);
        } finally {
            showLoading(false);
        }
    }

    async function loadStats() {
        const stats = await api.getStats();
        if (stats) {
            elements.statTotalStudents.textContent = stats.total_students;
            elements.statActiveStudents.textContent = stats.active_students;
            elements.statAvgGPA.textContent = stats.average_gpa.toFixed(2);
        } else {
            // Local fallback calculation
            const total = state.students.length;
            const active = state.students.filter(s => s.status === 'Active').length;
            const sumGPA = state.students.reduce((acc, s) => acc + parseFloat(s.gpa || 0), 0);
            const avg = total > 0 ? (sumGPA / total).toFixed(2) : '0.00';
            elements.statTotalStudents.textContent = total;
            elements.statActiveStudents.textContent = active;
            elements.statAvgGPA.textContent = avg;
        }
    }

    function renderStudentsTable(students) {
        elements.studentsTableBody.innerHTML = '';

        if (!students || students.length === 0) {
            elements.studentsTable.style.display = 'none';
            elements.emptyState.style.display = 'block';
            if (state.filters.search || state.filters.department || state.filters.status) {
                elements.emptyStateMessage.textContent = 'No student records match your active search and filter criteria.';
            } else {
                elements.emptyStateMessage.textContent = 'No records in the database. Click "+ Add New Student" to create your first entry.';
            }
            return;
        }

        elements.studentsTable.style.display = 'table';
        elements.emptyState.style.display = 'none';

        students.forEach(student => {
            const tr = document.createElement('tr');
            tr.dataset.id = student.id;

            const statusClass = `badge-${student.status.toLowerCase()}`;

            tr.innerHTML = `
                <td><strong>${escapeHtml(student.student_id)}</strong></td>
                <td>
                    <strong>${escapeHtml(student.first_name)} ${escapeHtml(student.last_name)}</strong>
                </td>
                <td>
                    <span class="dept-badge">${escapeHtml(student.department_code || student.department_name || 'N/A')}</span>
                </td>
                <td><a href="mailto:${escapeHtml(student.email)}">${escapeHtml(student.email)}</a></td>
                <td>${escapeHtml(student.phone || '—')}</td>
                <td>${student.enrollment_date || '—'}</td>
                <td><span class="gpa-tag">${parseFloat(student.gpa).toFixed(2)}</span></td>
                <td><span class="badge ${statusClass}">${escapeHtml(student.status)}</span></td>
                <td class="text-right">
                    <div class="action-buttons">
                        <button class="btn-icon-action btn-edit" title="Edit Student" data-id="${student.id}">
                            ✏️ Edit
                        </button>
                        <button class="btn-icon-action btn-delete" title="Delete Student" data-id="${student.id}" data-name="${escapeHtml(student.first_name + ' ' + student.last_name)}">
                            🗑️ Delete
                        </button>
                    </div>
                </td>
            `;
            elements.studentsTableBody.appendChild(tr);
        });

        // Attach action button events
        elements.studentsTableBody.querySelectorAll('.btn-edit').forEach(btn => {
            btn.addEventListener('click', () => openEditModal(btn.dataset.id));
        });

        elements.studentsTableBody.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', () => openDeleteModal(btn.dataset.id, btn.dataset.name));
        });
    }

    // ==========================================
    // MODAL & FORM OPERATIONS (CREATE & UPDATE)
    // ==========================================
    function openCreateModal() {
        state.editingStudentId = null;
        elements.modalTitle.textContent = 'Add New Student';
        elements.saveBtnText.textContent = 'Create Student';
        elements.studentForm.reset();
        elements.formStudentIdPK.value = '';
        elements.fieldStudentId.readOnly = false;
        clearFormErrors();
        elements.fieldEnrollmentDate.value = new Date().toISOString().split('T')[0];
        elements.studentModal.style.display = 'flex';
        elements.fieldStudentId.focus();
    }

    async function openEditModal(id) {
        state.editingStudentId = id;
        elements.modalTitle.textContent = 'Edit Student Details';
        elements.saveBtnText.textContent = 'Save Changes';
        clearFormErrors();

        try {
            const student = await api.getStudent(id);
            elements.formStudentIdPK.value = student.id;
            elements.fieldStudentId.value = student.student_id;
            elements.fieldStudentId.readOnly = true; // Roll number typically immutable on edit
            elements.fieldFirstName.value = student.first_name;
            elements.fieldLastName.value = student.last_name;
            elements.fieldEmail.value = student.email;
            elements.fieldPhone.value = student.phone || '';
            elements.fieldDepartment.value = student.department;
            elements.fieldEnrollmentDate.value = student.enrollment_date;
            elements.fieldGPA.value = parseFloat(student.gpa).toFixed(2);
            elements.fieldStatus.value = student.status;

            elements.studentModal.style.display = 'flex';
            elements.fieldFirstName.focus();
        } catch (error) {
            showToast(`Failed to load student details: ${error.message}`, 'error');
        }
    }

    function closeModal() {
        elements.studentModal.style.display = 'none';
        clearFormErrors();
    }

    // ==========================================
    // CLIENT-SIDE VALIDATION (SOP Section 9)
    // ==========================================
    function validateForm() {
        clearFormErrors();
        let isValid = true;

        const studentId = elements.fieldStudentId.value.trim();
        const firstName = elements.fieldFirstName.value.trim();
        const lastName = elements.fieldLastName.value.trim();
        const email = elements.fieldEmail.value.trim();
        const phone = elements.fieldPhone.value.trim();
        const department = elements.fieldDepartment.value;
        const enrollmentDate = elements.fieldEnrollmentDate.value;
        const gpa = elements.fieldGPA.value.trim();

        if (!studentId) {
            setFieldError('student_id', 'Student ID is mandatory.');
            isValid = false;
        } else if (studentId.length < 3) {
            setFieldError('student_id', 'Student ID must be at least 3 characters.');
            isValid = false;
        }

        if (!firstName) {
            setFieldError('first_name', 'First name is mandatory.');
            isValid = false;
        } else if (firstName.length < 2) {
            setFieldError('first_name', 'First name must have at least 2 characters.');
            isValid = false;
        }

        if (!lastName) {
            setFieldError('last_name', 'Last name is mandatory.');
            isValid = false;
        } else if (lastName.length < 2) {
            setFieldError('last_name', 'Last name must have at least 2 characters.');
            isValid = false;
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email) {
            setFieldError('email', 'Email address is mandatory.');
            isValid = false;
        } else if (!emailRegex.test(email)) {
            setFieldError('email', 'Please provide a valid email address (e.g. name@domain.com).');
            isValid = false;
        }

        if (phone && !/^\+?[0-9]{10,15}$/.test(phone)) {
            setFieldError('phone', 'Phone number must contain 10-15 digits.');
            isValid = false;
        }

        if (!department) {
            setFieldError('department', 'Please select a department.');
            isValid = false;
        }

        if (!enrollmentDate) {
            setFieldError('enrollment_date', 'Enrollment date is mandatory.');
            isValid = false;
        }

        const gpaNum = parseFloat(gpa);
        if (!gpa || isNaN(gpaNum)) {
            setFieldError('gpa', 'GPA must be a valid numeric value.');
            isValid = false;
        } else if (gpaNum < 0.0 || gpaNum > 4.0) {
            setFieldError('gpa', 'GPA must be within 0.00 and 4.00.');
            isValid = false;
        }

        return isValid;
    }

    function setFieldError(field, message) {
        const errorEl = document.getElementById(`err-${field}`);
        const inputEl = document.querySelector(`[name="${field}"]`);
        if (errorEl) errorEl.textContent = message;
        if (inputEl) inputEl.classList.add('is-invalid');
    }

    function clearFormErrors() {
        elements.formErrorAlert.style.display = 'none';
        elements.formErrorAlert.innerHTML = '';
        document.querySelectorAll('.field-error').forEach(el => el.textContent = '');
        document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
    }

    // ==========================================
    // FORM SUBMISSION (CREATE / UPDATE API CALL)
    // ==========================================
    async function handleFormSubmit(e) {
        e.preventDefault();

        if (!validateForm()) {
            return;
        }

        const payload = {
            student_id: elements.fieldStudentId.value.trim().toUpperCase(),
            first_name: elements.fieldFirstName.value.trim(),
            last_name: elements.fieldLastName.value.trim(),
            email: elements.fieldEmail.value.trim().toLowerCase(),
            phone: elements.fieldPhone.value.trim(),
            department: parseInt(elements.fieldDepartment.value, 10),
            enrollment_date: elements.fieldEnrollmentDate.value,
            gpa: parseFloat(elements.fieldGPA.value),
            status: elements.fieldStatus.value,
        };

        setFormLoading(true);

        try {
            if (state.editingStudentId) {
                // Update
                const res = await api.updateStudent(state.editingStudentId, payload);
                showToast(res.message || 'Student record updated successfully!', 'success');
            } else {
                // Create
                const res = await api.createStudent(payload);
                showToast(res.message || 'Student record created successfully!', 'success');
            }

            closeModal();
            await loadStudents();
            await loadStats();
        } catch (error) {
            handleServerErrors(error);
        } finally {
            setFormLoading(false);
        }
    }

    function handleServerErrors(error) {
        if (error.data && error.data.errors) {
            const errs = error.data.errors;
            let errorMessages = [];
            for (const [key, msgs] of Object.entries(errs)) {
                const messageText = Array.isArray(msgs) ? msgs.join(', ') : msgs;
                setFieldError(key, messageText);
                errorMessages.push(`<strong>${capitalize(key.replace('_', ' '))}:</strong> ${messageText}`);
            }
            elements.formErrorAlert.innerHTML = errorMessages.join('<br>');
            elements.formErrorAlert.style.display = 'block';
        } else {
            elements.formErrorAlert.innerHTML = `<strong>Error:</strong> ${error.message}`;
            elements.formErrorAlert.style.display = 'block';
        }
    }

    // ==========================================
    // DELETE OPERATIONS (SOP Section 8)
    // ==========================================
    function openDeleteModal(id, name) {
        state.deletingStudentId = id;
        elements.deleteStudentName.textContent = name;
        elements.deleteModal.style.display = 'flex';
    }

    function closeDeleteModal() {
        elements.deleteModal.style.display = 'none';
        state.deletingStudentId = null;
    }

    async function handleConfirmDelete() {
        if (!state.deletingStudentId) return;

        elements.confirmDeleteBtn.disabled = true;
        elements.confirmDeleteBtn.textContent = 'Deleting...';

        try {
            await api.deleteStudent(state.deletingStudentId);
            showToast('Student record deleted successfully.', 'success');
            closeDeleteModal();
            await loadStudents();
            await loadStats();
        } catch (error) {
            showToast(`Failed to delete record: ${error.message}`, 'error');
        } finally {
            elements.confirmDeleteBtn.disabled = false;
            elements.confirmDeleteBtn.textContent = 'Delete Record';
        }
    }

    // ==========================================
    // SEARCH & FILTER HANDLERS
    // ==========================================
    function handleSearchInput() {
        const value = elements.searchInput.value.trim();
        elements.clearSearchBtn.style.display = value ? 'block' : 'none';

        clearTimeout(state.searchTimeout);
        state.searchTimeout = setTimeout(() => {
            state.filters.search = value;
            loadStudents();
        }, 300); // 300ms debounce
    }

    function handleClearSearch() {
        elements.searchInput.value = '';
        elements.clearSearchBtn.style.display = 'none';
        state.filters.search = '';
        loadStudents();
        elements.searchInput.focus();
    }

    function handleDepartmentFilter() {
        state.filters.department = elements.departmentFilter.value;
        loadStudents();
    }

    function handleStatusFilter() {
        state.filters.status = elements.statusFilter.value;
        loadStudents();
    }

    function handleResetFilters() {
        elements.searchInput.value = '';
        elements.clearSearchBtn.style.display = 'none';
        elements.departmentFilter.value = '';
        elements.statusFilter.value = '';
        state.filters = { search: '', department: '', status: '' };
        loadStudents();
    }

    // ==========================================
    // HELPERS & UI UTILITIES
    // ==========================================
    function showLoading(isLoading) {
        elements.loadingIndicator.style.display = isLoading ? 'block' : 'none';
        if (isLoading) {
            elements.studentsTable.style.display = 'none';
            elements.emptyState.style.display = 'none';
        }
    }

    function renderErrorState(message) {
        elements.studentsTable.style.display = 'none';
        elements.emptyState.style.display = 'block';
        elements.emptyStateMessage.innerHTML = `<span style="color:var(--danger)">Unable to load records: ${escapeHtml(message)}</span>`;
    }

    function setFormLoading(isLoading) {
        elements.saveStudentBtn.disabled = isLoading;
        elements.saveBtnSpinner.style.display = isLoading ? 'inline-block' : 'none';
        elements.saveBtnText.style.display = isLoading ? 'none' : 'inline';
    }

    function showToast(message, type = 'info', duration = 4000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
        toast.innerHTML = `<span>${icon}</span> <span>${escapeHtml(message)}</span>`;

        elements.toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    // ==========================================
    // ATTACH EVENT LISTENERS
    // ==========================================
    function attachEventListeners() {
        // Search & Filters
        elements.searchInput.addEventListener('input', handleSearchInput);
        elements.clearSearchBtn.addEventListener('click', handleClearSearch);
        elements.departmentFilter.addEventListener('change', handleDepartmentFilter);
        elements.statusFilter.addEventListener('change', handleStatusFilter);
        elements.resetFiltersBtn.addEventListener('click', handleResetFilters);
        elements.refreshBtn.addEventListener('click', () => {
            checkConnection();
            loadStudents();
            loadStats();
        });

        // Modal Controls
        elements.addStudentBtn.addEventListener('click', openCreateModal);
        elements.closeModalBtn.addEventListener('click', closeModal);
        elements.cancelModalBtn.addEventListener('click', closeModal);
        elements.studentForm.addEventListener('submit', handleFormSubmit);

        // Delete Modal Controls
        elements.cancelDeleteBtn.addEventListener('click', closeDeleteModal);
        elements.closeDeleteModalBtn.addEventListener('click', closeDeleteModal);
        elements.confirmDeleteBtn.addEventListener('click', handleConfirmDelete);

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeModal();
                closeDeleteModal();
            }
        });
    }

    // Kick off initialization
    init();
});
