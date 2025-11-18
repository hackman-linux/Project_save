/**
 * Notifications Manager - Clean Rebuild
 * Handles persistent notifications display with AJAX
 */
class NotificationManager {
    constructor(config) {
        this.config = {
            fetchUrl: '/notifications/fetch/',       // ✅ fetch latest list
            countUrl: '/notifications/count/',       // ✅ only unread count
            markReadUrl: '/notifications/mark-read/',
            deleteUrl: '/notifications/delete/',
            markAllReadUrl: '/notifications/mark-all-read/',
            csrfToken: '',
            autoRefreshInterval: 0,  // disabled by default
            ...config
        };

        this.isLoading = false;
        this.autoRefreshTimer = null;

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFilterHandlers();
        this.updateNotificationCount();
        this.addManualRefreshButton();

        if (this.config.autoRefreshInterval > 0) {
            this.startAutoRefresh();
        }
    }

    setupEventListeners() {
        const list = document.getElementById('notificationsList');
        const markAllReadBtn = document.getElementById('markAllReadBtn');

        if (list) {
            list.addEventListener('click', (e) => {
                const markBtn = e.target.closest('.mark-read-btn');
                const deleteBtn = e.target.closest('.delete-btn');

                if (markBtn) {
                    e.preventDefault();
                    this.markAsRead(markBtn.dataset.id, markBtn.closest('.notification-item'));
                }
                if (deleteBtn) {
                    e.preventDefault();
                    this.deleteNotification(deleteBtn.dataset.id, deleteBtn.closest('.notification-item'));
                }
            });
        }

        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.markAllAsRead();
            });
        }
    }

    addManualRefreshButton() {
        const pageActions = document.querySelector('.page-actions, #pageActions, .card-header');
        if (pageActions && !document.getElementById('manualRefreshBtn')) {
            const btn = document.createElement('button');
            btn.id = 'manualRefreshBtn';
            btn.className = 'btn btn-outline-info me-2';
            btn.innerHTML = '<i class="bi bi-arrow-clockwise me-2"></i>Check for New';
            btn.addEventListener('click', () => this.fetchNotifications(true));
            pageActions.appendChild(btn);
        }
    }

    setupFilterHandlers() {
        ['filterByType', 'filterByStatus', 'filterByTime'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.addEventListener('change', () => this.applyFilters());
        });
    }

    async fetchNotifications(showAlert = false) {
        const btn = document.getElementById('manualRefreshBtn');
        if (btn) {
            btn.innerHTML = '<i class="spinner-border spinner-border-sm me-2"></i>Checking...';
            btn.disabled = true;
        }

        try {
            const response = await fetch(this.config.fetchUrl, {
                method: 'GET',
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });

            if (response.ok) {
                const data = await response.json();
                const list = document.getElementById('notificationsList');
                if (list) list.innerHTML = data.html;

                this.updateUnreadBadge(data.unread_count);
                if (showAlert) {
                    if (data.unread_count > 0) {
                        this.showNewNotificationAlert(data.unread_count);
                    } else {
                        this.showToast('No new notifications', 'info');
                    }
                }
            }
        } catch (err) {
            console.error('Fetch error:', err);
            if (showAlert) this.showToast('Error fetching notifications', 'error');
        } finally {
            if (btn) {
                btn.innerHTML = '<i class="bi bi-arrow-clockwise me-2"></i>Check for New';
                btn.disabled = false;
            }
        }
    }

    async markAsRead(id, item) {
        if (!item) return;
        try {
            const res = await fetch(`${this.config.markReadUrl}${id}/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': this.config.csrfToken }
            });
            const data = await res.json();
            if (data.success) {
                item.classList.remove('unread');
                item.dataset.status = 'read';
                item.querySelector('.mark-read-btn')?.remove();
                this.updateNotificationCount(-1);
                this.showToast('Marked as read', 'success');
            }
        } catch (err) {
            console.error(err);
            this.showToast('Failed to mark as read', 'error');
        }
    }

    async deleteNotification(id, item) {
        if (!item || !confirm('Delete this notification?')) return;
        try {
            const res = await fetch(`${this.config.deleteUrl}${id}/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': this.config.csrfToken }
            });
            const data = await res.json();
            if (data.success) {
                item.remove();
                this.checkForEmptyState();
                this.updateNotificationCount();
                this.showToast('Notification deleted', 'success');
            }
        } catch (err) {
            console.error(err);
            this.showToast('Failed to delete', 'error');
        }
    }

    async markAllAsRead() {
        const unreadItems = document.querySelectorAll('.notification-item.unread');
        if (!unreadItems.length) {
            this.showToast('No unread notifications', 'info');
            return;
        }
        if (!confirm(`Mark all ${unreadItems.length} as read?`)) return;

        try {
            const res = await fetch(this.config.markAllReadUrl, {
                method: 'POST',
                headers: { 'X-CSRFToken': this.config.csrfToken }
            });
            const data = await res.json();
            if (data.success) {
                unreadItems.forEach(item => {
                    item.classList.remove('unread');
                    item.dataset.status = 'read';
                    item.querySelector('.mark-read-btn')?.remove();
                });
                this.updateNotificationCount();
                this.showToast('All marked as read', 'success');
            }
        } catch (err) {
            console.error(err);
            this.showToast('Failed to mark all as read', 'error');
        }
    }

    applyFilters() {
        const form = document.getElementById('filterForm');
        if (form) form.submit();
    }

    updateNotificationCount(delta = 0) {
        const countElement = document.getElementById('notificationCount');
        const sidebarBadge = document.querySelector('.nav-link .badge');
        const unreadStat = document.querySelector('.stats-card.bg-warning .card-title');

        const total = document.querySelectorAll('.notification-item').length;
        const unread = document.querySelectorAll('.notification-item.unread').length;

        if (countElement) countElement.textContent = total;
        if (sidebarBadge) {
            sidebarBadge.textContent = unread;
            sidebarBadge.style.display = unread ? 'inline' : 'none';
        }
        if (unreadStat) unreadStat.textContent = unread;
    }

    updateUnreadBadge(unread) {
        const sidebarBadge = document.querySelector('.nav-link .badge');
        if (sidebarBadge) {
            sidebarBadge.textContent = unread;
            sidebarBadge.style.display = unread ? 'inline' : 'none';
        }
        const unreadStat = document.querySelector('.stats-card.bg-warning .card-title');
        if (unreadStat) unreadStat.textContent = unread;
    }

    checkForEmptyState() {
        const list = document.getElementById('notificationsList');
        if (list && !list.querySelector('.notification-item')) {
            list.innerHTML = `
                <div class="empty-notifications text-center py-5">
                    <i class="bi bi-bell fs-1 text-muted"></i>
                    <h5 class="mt-3 text-muted">No Notifications</h5>
                    <p class="text-muted">You're all caught up!</p>
                </div>`;
        }
    }

    showToast(msg, type = 'info') {
        const toast = document.getElementById('notificationToast');
        const msgEl = document.getElementById('toastMessage');
        if (!toast || !msgEl) return;

        msgEl.textContent = msg;
        const header = toast.querySelector('.toast-header');
        const icon = header.querySelector('i');
        header.className = 'toast-header';
        icon.className = 'me-2';

        switch (type) {
            case 'success': header.classList.add('bg-success','text-white'); icon.classList.add('bi-check-circle-fill'); break;
            case 'error':   header.classList.add('bg-danger','text-white'); icon.classList.add('bi-exclamation-triangle-fill'); break;
            case 'warning': header.classList.add('bg-warning'); icon.classList.add('bi-exclamation-triangle-fill'); break;
            default:        header.classList.add('bg-info','text-white'); icon.classList.add('bi-info-circle-fill');
        }

        new bootstrap.Toast(toast, { autohide: false }).show();
    }

    showNewNotificationAlert(newCount) {
        document.querySelector('.new-notification-alert')?.remove();
        const alert = document.createElement('div');
        alert.className = 'alert alert-primary alert-dismissible fade show new-notification-alert';
        alert.style.cssText = 'position: sticky; top: 0; z-index: 1050; margin-bottom: 20px;';
        alert.innerHTML = `
            <i class="bi bi-bell-fill me-2"></i>
            <strong>${newCount}</strong> new notification${newCount > 1 ? 's' : ''}!
            <button type="button" class="btn btn-sm btn-outline-primary ms-2" onclick="window.notificationManager.fetchNotifications(true)">
                <i class="bi bi-arrow-clockwise me-1"></i>Refresh
            </button>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.getElementById('notificationsList')?.prepend(alert);
    }

    startAutoRefresh() {
        if (this.config.autoRefreshInterval > 0) {
            this.autoRefreshTimer = setInterval(() => this.fetchNotifications(), this.config.autoRefreshInterval);
        }
    }

    destroy() {
        if (this.autoRefreshTimer) clearInterval(this.autoRefreshTimer);
    }
}

// Global helpers
window.checkForNewNotifications = () => window.notificationManager?.fetchNotifications(true);
window.markAllAsRead = () => window.notificationManager?.markAllAsRead();
window.refreshNotifications = () => window.notificationManager?.fetchNotifications(true);

window.addEventListener('beforeunload', () => window.notificationManager?.destroy());
