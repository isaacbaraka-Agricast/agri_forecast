# notifications.py
# Firebase FCM Push Notifications for Agri Forecast System

import requests
import json

# -----------------------------------------------
# FIREBASE CONFIG
# -----------------------------------------------
FIREBASE_PROJECT_ID = "agri-forecast-f192d"

# Server Key from Firebase Console
# Go to: Project Settings → Cloud Messaging → Server key
# Paste it below:
FIREBASE_SERVER_KEY = "YOUR_SERVER_KEY_HERE"

FCM_URL = "https://fcm.googleapis.com/fcm/send"

# -----------------------------------------------
# SEND PUSH NOTIFICATION VIA FIREBASE FCM
# -----------------------------------------------
def send_push_notification(fcm_token, title, body, data=None):
    """
    Send a push notification to a Flutter app via Firebase FCM.
    
    Args:
        fcm_token: Device token from Flutter app
        title: Notification title
        body: Notification message
        data: Extra data dict (optional)
    """
    if not fcm_token:
        print("[FCM] No token provided, skipping push notification")
        return {"status": "skipped", "reason": "no token"}

    if FIREBASE_SERVER_KEY == "YOUR_SERVER_KEY_HERE":
        print(f"[FCM STUB] Title: {title} | Body: {body}")
        return {"status": "stub", "message": "Add your Firebase Server Key"}

    headers = {
        "Authorization": f"key={FIREBASE_SERVER_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "to": fcm_token,
        "notification": {
            "title": title,
            "body": body,
            "sound": "default",
            "icon": "ic_launcher"
        },
        "data": data or {},
        "priority": "high"
    }

    try:
        response = requests.post(FCM_URL, headers=headers, data=json.dumps(payload))
        result = response.json()

        if result.get("success") == 1:
            print(f"[FCM] ✅ Notification sent: {title}")
            return {"status": "success", "result": result}
        else:
            print(f"[FCM] ❌ Failed: {result}")
            return {"status": "error", "result": result}

    except Exception as e:
        print(f"[FCM] Exception: {str(e)}")
        return {"status": "error", "message": str(e)}

# -----------------------------------------------
# SEND SMS ALERT (stub — add Twilio later if needed)
# -----------------------------------------------
def send_sms_alert(recipient, message):
    """
    SMS stub — prints to console.
    Replace with Twilio integration if needed.
    """
    print(f"[SMS ALERT] To: {recipient} | Message: {message}")
    return {"status": "stub", "message": "SMS not configured"}

# -----------------------------------------------
# SEND FORECAST ALERT
# Convenience function to alert about forecast peaks
# -----------------------------------------------
def send_forecast_alert(fcm_token, crop_name, peak_week, peak_demand):
    """
    Send a forecast alert when a demand peak is detected.
    """
    title = f"📈 {crop_name} Demand Alert"
    body  = (
        f"{crop_name} demand will peak in Week {peak_week} "
        f"with {int(peak_demand):,} kg. Plan your harvest now!"
    )
    data = {
        "type":      "forecast_alert",
        "crop":      crop_name,
        "peak_week": str(peak_week),
        "demand_kg": str(peak_demand)
    }
    return send_push_notification(fcm_token, title, body, data)

# -----------------------------------------------
# SEND PRICE ALERT
# -----------------------------------------------
def send_price_alert(fcm_token, crop_name, best_week, max_price):
    """
    Send a price alert for best selling week.
    """
    title = f"💰 {crop_name} Price Alert"
    body  = (
        f"Best time to sell {crop_name} is Week {best_week} "
        f"at {max_price} RWF/kg!"
    )
    data = {
        "type":      "price_alert",
        "crop":      crop_name,
        "best_week": str(best_week),
        "max_price": str(max_price)
    }
    return send_push_notification(fcm_token, title, body, data)}