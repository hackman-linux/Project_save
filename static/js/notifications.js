/**
 * Notifications Manager - Handles all notification functionality
 * Save as: static/js/notifications.js
 */
class NotificationManager {
    constructor(config) {
        this.config = {
            markReadUrl: '/notifications/mark-as-read/',
            deleteUrl: '/notifications/delete/',
            markAllReadUrl: '/notifications/mark-all-read/',
            csrfToken: '',
            autoRefreshInterval: 30000, // 30 seconds
            ...config
        };
        
        this.isLoading = false;
        this.autoRefreshTimer = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.startAutoRefresh();
        this.setupFilterHandlers();
        this.updateNotificationCount();
    }

    setupEventListeners() {
        const notificationsList = document.getElementById('notificationsList');
        const markAllReadBtn = document.getElementById('markAllReadBtn');
        const refreshBtn = document.getElementById('refreshBtn');

        // Event delegation for notification actions
        if (notificationsList) {
            notificationsList.addEventListener('click', (e) => {
                const markReadBtn = e.target.closest('.mark-read-btn');
                const deleteBtn = e.target.closest('.delete-btn');
                
                if (markReadBtn) {
                    e.preventDefault();
                    const notificationId = markReadBtn.dataset.id;
                    const notificationItem = markReadBtn.closest('.notification-item');
                    this.markAsRead(notificationId, notificationItem);
                }
                
                if (deleteBtn) {
                    e.preventDefault();
                    const notificationId = deleteBtn.dataset.id;
                    const notificationItem = deleteBtn.closest('.notification-item');
                    this.deleteNotification(notificationId, notificationItem);
                }
            });
        }

        // Mark all as read
        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.markAllAsRead();
            });
        }

        // Refresh button
        if (refreshBtn) {
            refreshBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.refreshNotifications();
            });
        }
    }

    setupFilterHandlers() {
        const filterForm = document.getElementById('filterForm');
        const typeFilter = document.getElementById('filterByType');
        const statusFilter = document.getElementById('filterByStatus');
        const timeFilter = document.getElementById('filterByTime');

        if (typeFilter) {
            typeFilter.addEventListener('change', () => this.applyFilters());
        }
        
        if (statusFilter) {
            statusFilter.addEventListener('change', () => this.applyFilters());
        }
        
        if (timeFilter) {
            timeFilter.addEventListener('change', () => this.applyFilters());
        }
    }

    async markAsRead(notificationId, notificationItem) {
        if (this.isLoading) return;
        
        try {
            this.isLoading = true;
            this.showLoading(notificationItem);
            
            const response = await fetch(`${this.config.markReadUrl}${notificationId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.config.csrfToken,
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();
            
            if (data.success) {
                // Update UI
                notificationItem.classList.remove('unread');
                notificationItem.dataset.status = 'read';
                
                // Remove mark as read button
                const markReadBtn = notificationItem.querySelector('.mark-read-btn');
                if (markReadBtn) {
                    markReadBtn.remove();
                }
                
                // Remove unread badge
                const unreadBadge = notificationItem.querySelector('.badge.bg-warning.text-dark');
                if (unreadBadge) {
                    unreadBadge.remove();
                }
                
                this.updateNotificationCount(-1);
                this.showToast('Notification marked as read', 'success');
            } else {
                this.showToast('Failed to mark notification as read', 'error');
            }
        } catch (error) {
            console.error('Error marking notification as read:', error);
            this.showToast('Error marking notification as read', 'error');
        } finally {
            this.isLoading = false;
            this.hideLoading();
        }
    }

    async deleteNotification(notificationId, notificationItem) {
        if (this.isLoading) return;
        
        // Show confirmation
        if (!confirm('Are you sure you want to delete this notification? This action cannot be undone.')) {
            return;
        }
        
        try {
            this.isLoading = true;
            this.showLoading(notificationItem);
            
            const response = await fetch(`${this.config.deleteUrl}${notificationId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.config.csrfToken,
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();
            
            if (data.success) {
                // Animate removal
                notificationItem.style.transition = 'all 0.3s ease';
                notificationItem.style.opacity = '0';
                notificationItem.style.transform = 'translateX(-20px)';
                
                setTimeout(() => {
                    notificationItem.remove();
                    this.checkForEmptyState();
                }, 300);
                
                this.updateNotificationCount();
                this.showToast('Notification deleted', 'success');
            } else {
                this.showToast('Failed to delete notification', 'error');
            }
        } catch (error) {
            console.error('Error deleting notification:', error);
            this.showToast('Error deleting notification', 'error');
        } finally {
            this.isLoading = false;
            this.hideLoading();
        }
    }

    async markAllAsRead() {
        const unreadItems = document.querySelectorAll('.notification-item.unread');
        
        if (unreadItems.length === 0) {
            this.showToast('No unread notifications to mark', 'info');
            return;
        }
        
        if (!confirm(`Mark all ${unreadItems.length} unread notifications as read?`)) {
            return;
        }
        
        try {
            this.isLoading = true;
            const markAllBtn = document.getElementById('markAllReadBtn');
            if (markAllBtn) {
                markAllBtn.disabled = true;
                markAllBtn.innerHTML = '<i class="spinner-border spinner-border-sm me-2"></i>Marking...';
            }
            
            const response = await fetch(this.config.markAllReadUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.config.csrfToken,
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();
            
            if (data.success) {
                // Update all unread notifications
                unreadItems.forEach(item => {
                    item.classList.remove('unread');
                    item.dataset.status = 'read';
                    
                    // Remove mark as read button
                    const markReadBtn = item.querySelector('.mark-read-btn');
                    if (markReadBtn) {
                        markReadBtn.remove();
                    }
                    
                    // Remove unread badge
                    const unreadBadge = item.querySelector('.badge.bg-warning.text-dark');
                    if (unreadBadge) {
                        unreadBadge.remove();
                    }
                });
                
                this.updateNotificationCount();
                this.showToast(`${unreadItems.length} notifications marked as read`, 'success');
            } else {
                this.showToast('Failed to mark all notifications as read', 'error');
            }
        } catch (error) {
            console.error('Error marking all as read:', error);
            this.showToast('Error marking all notifications as read', 'error');
        } finally {
            this.isLoading = false;
            const markAllBtn = document.getElementById('markAllReadBtn');
            if (markAllBtn) {
                markAllBtn.disabled = false;
                markAllBtn.innerHTML = '<i class="bi bi-check-all me-2"></i>Mark All as Read';
            }
        }
    }

    refreshNotifications() {
        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.classList.add('refreshing');
        }
        
        // Reload the current page with existing filters
        setTimeout(() => {
            window.location.reload();
        }, 500);
    }

    applyFilters() {
        const form = document.getElementById('filterForm');
        if (form) {
            form.submit();
        }
    }

    updateNotificationCount(delta = 0) {
        const countElement = document.getElementById('notificationCount');
        const sidebarBadge = document.querySelector('.nav-link .badge');
        const unreadStat = document.querySelector('.stats-card.bg-warning .card-title');
        
        if (delta !== 0) {
            // Update with delta
            if (countElement) {
                const current = parseInt(countElement.textContent) || 0;
                countElement.textContent = Math.max(0, current + delta);
            }
            
            if (sidebarBadge && delta < 0) {
                const current = parseInt(sidebarBadge.textContent) || 0;
                const newCount = Math.max(0, current + delta);
                if (newCount === 0) {
                    sidebarBadge.style.display = 'none';
                } else {
                    sidebarBadge.textContent = newCount;
                }
            }
            
            if (unreadStat && delta < 0) {
                const current = parseInt(unreadStat.textContent) || 0;
                unreadStat.textContent = Math.max(0, current + delta);
            }
        } else {
            // Recalculate from DOM
            const totalNotifications = document.querySelectorAll('.notification-item').length;
            const unreadNotifications = document.querySelectorAll('.notification-item.unread').length;
            
            if (countElement) {
                countElement.textContent = totalNotifications;
            }
            
            if (sidebarBadge) {
                if (unreadNotifications === 0) {
                    sidebarBadge.style.display = 'none';
                } else {
                    sidebarBadge.textContent = unreadNotifications;
                    sidebarBadge.style.display = 'inline';
                }
            }
            
            if (unreadStat) {
                unreadStat.textContent = unreadNotifications;
            }
        }
    }

    checkForEmptyState() {
        const notificationsList = document.getElementById('notificationsList');
        const notifications = notificationsList.querySelectorAll('.notification-item');
        
        if (notifications.length === 0) {
            notificationsList.innerHTML = `
                <div class="empty-notifications text-center py-5">
                    <i class="bi bi-bell fs-1 text-muted"></i>
                    <h5 class="mt-3 text-muted">No Notifications</h5>
                    <p class="text-muted">You're all caught up! No new notifications to display.</p>
                </div>
            `;
        }
    }

    showLoading(element = null) {
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.classList.remove('d-none');
        }
        
        if (element) {
            element.style.opacity = '0.6';
            element.style.pointerEvents = 'none';
        }
    }

    hideLoading() {
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.classList.add('d-none');
        }
        
        // Re-enable all notification items
        document.querySelectorAll('.notification-item').forEach(item => {
            item.style.opacity = '';
            item.style.pointerEvents = '';
        });
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('notificationToast');
        const toastMessage = document.getElementById('toastMessage');
        
        if (!toast || !toastMessage) return;
        
        // Set message
        toastMessage.textContent = message;
        
        // Set color based on type
        const toastHeader = toast.querySelector('.toast-header');
        const icon = toastHeader.querySelector('i');
        
        toastHeader.className = 'toast-header';
        icon.className = 'me-2';
        
        switch(type) {
            case 'success':
                toastHeader.classList.add('bg-success', 'text-white');
                icon.classList.add('bi-check-circle-fill');
                break;
            case 'error':
                toastHeader.classList.add('bg-danger', 'text-white');
                icon.classList.add('bi-exclamation-triangle-fill');
                break;
            case 'warning':
                toastHeader.classList.add('bg-warning');
                icon.classList.add('bi-exclamation-triangle-fill');
                break;
            default:
                toastHeader.classList.add('bg-info', 'text-white');
                icon.classList.add('bi-info-circle-fill');
        }
        
        // Show toast
        const bsToast = new bootstrap.Toast(toast, {
            autohide: true,
            delay: 3000
        });
        bsToast.show();
    }

    startAutoRefresh() {
        // Clear existing timer
        if (this.autoRefreshTimer) {
            clearInterval(this.autoRefreshTimer);
        }
        
        // Set new timer for auto-refresh
        this.autoRefreshTimer = setInterval(() => {
            this.checkForNewNotifications();
        }, this.config.autoRefreshInterval);
    }

    async checkForNewNotifications() {
        try {
            const response = await fetch('/notifications/count/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                const currentUnread = document.querySelectorAll('.notification-item.unread').length;
                
                if (data.unread_count > currentUnread) {
                    // New notifications available
                    this.showNewNotificationAlert(data.unread_count - currentUnread);
                }
            }
        } catch (error) {
            console.error('Error checking for new notifications:', error);
        }
    }

    showNewNotificationAlert(newCount) {
        // Show a subtle alert for new notifications
        const alert = document.createElement('div');
        alert.className = 'alert alert-info alert-dismissible fade show position-fixed';
        alert.style.cssText = 'top: 20px; right: 20px; z-index: 1055; min-width: 300px;';
        alert.innerHTML = `
            <i class="bi bi-bell-fill me-2"></i>
            <strong>${newCount}</strong> new notification${newCount > 1 ? 's' : ''} received!
            <button type="button" class="btn btn-sm btn-outline-primary ms-2" onclick="window.location.reload()">
                Refresh
            </button>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alert);
        
        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 10000);
    }

    destroy() {
        // Clean up event listeners and timers
        if (this.autoRefreshTimer) {
            clearInterval(this.autoRefreshTimer);
        }
    }
}

// Global functions for backward compatibility
window.markAllAsRead = function() {
    if (window.notificationManager) {
        window.notificationManager.markAllAsRead();
    }
};

window.refreshNotifications = function() {
    if (window.notificationManager) {
        window.notificationManager.refreshNotifications();
    }
};

window.loadMoreNotifications = function() {
    // Handle pagination if needed
    const nextPageLink = document.querySelector('.pagination .page-item:last-child a');
    if (nextPageLink && !nextPageLink.parentElement.classList.contains('disabled')) {
        window.location.href = nextPageLink.href;
    }
};

// Cleanup when page unloads
window.addEventListener('beforeunload', function() {
    if (window.notificationManager) {
        window.notificationManager.destroy();
    }
});