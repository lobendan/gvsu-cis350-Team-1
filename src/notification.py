from plyer import notification

notification.notify(
    title='Notification Title',
    message='This is a notification message.',
    app_name='My App',
    timeout=10  # Duration in seconds
)