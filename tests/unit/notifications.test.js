/**
 * Unit Tests for Notification System
 */

describe('Notification System', () => {
    let notifications;
    let container;

    beforeEach(() => {
        // Setup DOM
        document.body.innerHTML = `
            <div id="notification-container">
                <div class="notification-list"></div>
            </div>
        `;
        container = document.getElementById('notification-container');
        
        // Mock notification system
        notifications = {
            items: [],
            
            add(type, icon, message) {
                const notification = {
                    id: Date.now(),
                    type,
                    icon,
                    message,
                    timestamp: new Date(),
                    read: false
                };
                this.items.unshift(notification);
                this.render();
                return notification;
            },
            
            markAsRead(id) {
                const item = this.items.find(n => n.id === id);
                if (item) {
                    item.read = true;
                    this.render();
                }
            },
            
            clearAll() {
                this.items = [];
                this.render();
            },
            
            getUnreadCount() {
                return this.items.filter(n => !n.read).length;
            },
            
            render() {
                const list = container.querySelector('.notification-list');
                if (this.items.length === 0) {
                    list.innerHTML = '<div class="empty">No notifications</div>';
                    return;
                }
                
                list.innerHTML = this.items.map(n => `
                    <div class="notification ${n.read ? 'read' : 'unread'}" data-id="${n.id}">
                        <i class="fas ${n.icon}"></i>
                        <span>${n.message}</span>
                    </div>
                `).join('');
            }
        };
    });

    describe('add', () => {
        test('should add notification to list', () => {
            notifications.add('success', 'fa-check', 'Test message');
            
            expect(notifications.items).toHaveLength(1);
        });

        test('should add notification with correct properties', () => {
            const notification = notifications.add('warning', 'fa-exclamation', 'Warning message');
            
            expect(notification.type).toBe('warning');
            expect(notification.icon).toBe('fa-exclamation');
            expect(notification.message).toBe('Warning message');
            expect(notification.read).toBe(false);
        });

        test('should add new notifications at the beginning', () => {
            notifications.add('info', 'fa-info', 'First');
            notifications.add('success', 'fa-check', 'Second');
            
            expect(notifications.items[0].message).toBe('Second');
        });
    });

    describe('markAsRead', () => {
        test('should mark notification as read', () => {
            const notification = notifications.add('info', 'fa-info', 'Test');
            
            notifications.markAsRead(notification.id);
            
            expect(notifications.items[0].read).toBe(true);
        });

        test('should not affect other notifications', () => {
            const n1 = notifications.add('info', 'fa-info', 'First');
            const n2 = notifications.add('info', 'fa-info', 'Second');
            
            notifications.markAsRead(n1.id);
            
            expect(notifications.items[0].read).toBe(false); // Second notification
            expect(notifications.items[1].read).toBe(true);  // First notification
        });
    });

    describe('clearAll', () => {
        test('should remove all notifications', () => {
            notifications.add('info', 'fa-info', 'First');
            notifications.add('info', 'fa-info', 'Second');
            
            notifications.clearAll();
            
            expect(notifications.items).toHaveLength(0);
        });
    });

    describe('getUnreadCount', () => {
        test('should return correct count of unread notifications', () => {
            notifications.add('info', 'fa-info', 'First');
            notifications.add('info', 'fa-info', 'Second');
            notifications.add('info', 'fa-info', 'Third');
            
            expect(notifications.getUnreadCount()).toBe(3);
        });

        test('should not count read notifications', () => {
            const n1 = notifications.add('info', 'fa-info', 'First');
            notifications.add('info', 'fa-info', 'Second');
            
            notifications.markAsRead(n1.id);
            
            expect(notifications.getUnreadCount()).toBe(1);
        });
    });
});
