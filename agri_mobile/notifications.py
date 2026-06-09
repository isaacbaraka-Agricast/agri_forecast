# notifications.py

def send_sms_alert(phone, message):
    print(f"SMS to {phone}: {message}")
    return {"status": "sent", "type": "sms"}

def send_push_notification(token, title, body, data=None):
    print(f"Push to {token}: {title} - {body}")
    return {"status": "sent", "type": "push"}