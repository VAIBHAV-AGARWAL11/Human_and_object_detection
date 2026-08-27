from ultralytics import YOLO
import cv2
import time
import threading
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ssl

# ==========================================
# THREADED CAMERA CLASS
# ==========================================

class ThreadedCamera:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        # Set buffer size to 1 to minimize driver-level frame buffering
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.ret, self.frame = self.cap.read()
        self.stopped = False
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True

    def start(self):
        self.thread.start()
        return self

    def update(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            if not ret:
                self.stopped = True
                continue
            with self.lock:
                self.ret = ret
                self.frame = frame
            time.sleep(0.01)  # small pause to reduce CPU usage

    def read(self):
        with self.lock:
            if self.frame is not None:
                return self.ret, self.frame.copy()
            return self.ret, None

    def release(self):
        self.stopped = True
        self.thread.join(timeout=1.0)
        self.cap.release()

# ==========================================
# EMAIL CONFIGURATION
# ==========================================

sender = "vv3151773@gmail.com"
app_password = "ermi zvzu vimv dwrs"

receivers = [
    "akshatkumar67353@gmail.com",
    "vaibhavagarwal1127@gmail.com"
]

# ==========================================
# LOAD YOLO MODEL
# ==========================================

model = YOLO("yolov8n.pt")

# ==========================================
# CAMERA
# ==========================================

cam = ThreadedCamera(0).start()

# Warm up camera to let auto-exposure adjust
print("Warming up camera...")
time.sleep(1.5)


# ==========================================
# TRACKING & ALERT STATE
# ==========================================

tracked_objects = {}  # Maps track_id -> { 'first_seen': float, 'last_seen': float, 'alert_count': int, 'last_alert_time': float }
total_emails_sent = 0
last_global_alert_time = 0.0
ALERT_INTERVAL = 5.0  # seconds between alerts
INACTIVE_THRESHOLD = 30  # Remove object if not seen for 30 seconds

print("====================================")
print("JKLC HUMAN DETECTION SYSTEM STARTED")
print("====================================")

# ==========================================
# MAIN LOOP
# ==========================================

while True:

    ret, frame = cam.read()

    if not ret:
        print("Failed to access camera.")
        break

    # Run YOLO Tracking
    results = model.track(frame, persist=True, classes=[0], conf=0.3)

    # Draw bounding boxes (annotated frame will show tracked boxes and IDs)
    annotated_frame = results[0].plot()

    active_track_ids = []

    # Check detections
    if results[0].boxes is not None and results[0].boxes.id is not None:
        for box in results[0].boxes:
            track_id = int(box.id[0])
            active_track_ids.append(track_id)

    current_time = time.time()

    # Update state for currently detected objects
    for track_id in active_track_ids:
        if track_id not in tracked_objects:
            tracked_objects[track_id] = {
                'first_seen': current_time,
                'last_seen': current_time,
                'alert_count': 0,
                'last_alert_time': 0.0
            }
        else:
            tracked_objects[track_id]['last_seen'] = current_time

    # Remove inactive objects (not seen for INACTIVE_THRESHOLD seconds)
    inactive_ids = [tid for tid, obj in tracked_objects.items() if current_time - obj['last_seen'] > INACTIVE_THRESHOLD]
    for tid in inactive_ids:
        del tracked_objects[tid]

    # Check for active objects that need repeating alert emails (max 4 times, every 5 seconds)
    new_alerts_to_send = []
    if current_time - last_global_alert_time >= ALERT_INTERVAL:
        for track_id, obj in tracked_objects.items():
            if obj['alert_count'] < 4 and (current_time - obj['last_alert_time'] >= ALERT_INTERVAL):
                new_alerts_to_send.append(track_id)

    # ==========================================
    # SEND ALERT
    # ==========================================

    if len(new_alerts_to_send) > 0:

        timestamp = time.strftime("%d-%m-%Y_%H-%M-%S")

        image_name = f"alert_{timestamp}.jpg"

        # Update alert counts and last alert times BEFORE sending email to prevent duplicate triggers
        for track_id in new_alerts_to_send:
            tracked_objects[track_id]['alert_count'] += 1
            tracked_objects[track_id]['last_alert_time'] = current_time
        
        last_global_alert_time = current_time

        # Format details for logging and email
        details_list = [f"ID {tid} (Alert {tracked_objects[tid]['alert_count']}/4)" for tid in new_alerts_to_send]

        print(f"Sending Alerts for: {details_list} at {timestamp}")

        email_content = f"""Dear Concerned Team,

This is an automated alert generated by the JK Lakshmi Cement Human Detection Monitoring System.

A human presence has been detected by the surveillance camera.

====================================

DETECTION DETAILS

Event Type      : Human Detection
Detection Time  : {time.strftime('%d-%m-%Y %H:%M:%S')}
Camera Source   : Monitoring Camera
Alert Level     : High
Status          : Detection Confirmed
Tracked ID(s)   : {details_list}

====================================

A screenshot captured during the detection event has been attached for review.

Recommended Actions:

1. Verify the detected individual.
2. Review camera footage if required.
3. Take necessary action as per company security policy.

This is an automatically generated alert.

Please do not reply to this email.

Regards,

Human Detection Monitoring System
JK Lakshmi Cement Ltd.
"""

        # Send email alert and save image in background thread to prevent camera lag
        def send_email_bg(subject, content, frame_copy, image_path):
            try:
                # Save screenshot asynchronously inside background thread to avoid GUI lag
                cv2.imwrite(image_path, frame_copy)
                print(f"Screenshot Saved: {image_path}")
                
                # Create standard MIME email structure
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = ", ".join(receivers)
                msg['Subject'] = subject

                # Attach email body
                msg.attach(MIMEText(content, 'plain'))

                # Attach screenshot file
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={os.path.basename(image_path)}'
                        )
                        msg.attach(part)

                # Send email using standard smtplib with ssl context bypass for macOS
                context = ssl._create_unverified_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=10) as server:
                    server.login(sender, app_password)
                    server.sendmail(sender, receivers, msg.as_string())
                
                print("Email Alert Sent Successfully in background!")
            except Exception as e:
                print("Email Sending Failed in background!")
                print(e)

        print(email_content)
        
        # Increment total emails count
        total_emails_sent += 1
        
        # Start background email sending thread (not daemon, so it can finish sending after we break the loop)
        threading.Thread(
            target=send_email_bg,
            args=("SECURITY ALERT | Human Presence Detected", email_content, annotated_frame.copy(), image_name),
            daemon=False
        ).start()

        # Stop the system once the limit of 4 emails is reached
        if total_emails_sent >= 4:
            print("Maximum limit of 4 email alerts reached. Automatically stopping system...")
            break

    # ==========================================
    # DISPLAY WINDOW
    # ==========================================

    cv2.imshow("JKLC Human Detection System", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ==========================================
# CLEANUP
# ==========================================

cam.release()
cv2.destroyAllWindows()

print("System Stopped.")