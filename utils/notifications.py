from plyer import notification


def notify(title, message):
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="GorillaFTP",
            timeout=5
        )

    except Exception as e:
        print("Notification error:", e)