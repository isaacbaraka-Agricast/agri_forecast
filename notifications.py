def send_sms_alert(message, recipient=None):
    print("[SMS ALERT] To: " + str(recipient) + " | Message: " + str(message))

def send_push_notification(title, body, recipient=None):
    print("[PUSH NOTIFICATION] To: " + str(recipient) + " | " + str(title) + ": " + str(body))