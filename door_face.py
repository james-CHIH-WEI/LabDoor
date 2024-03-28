import os
import cv2
import face_recognition
from datetime import datetime
import paho.mqtt.publish as publish
import time

# import RPi.GPIO as GPIO

member_path = "./member_images"
record_path = "./record_images"
image_face_encoding_array = []
face_locations = []
face_encodings = []

ip = "healthcareiot.ntunhs.edu.tw"
user = "hiot"
password = "12345678"


# def angle_to_duty_cycle(angle):
#     duty_cycle = (0.05 * 50) + (0.19 * 50 * angle / 180)
#     return duty_cycle


# def set_angle(servo, angle, sec):
#     duty_cycle = angle_to_duty_cycle(angle)
#     servo.ChangeDutyCycle(duty_cycle)
#     time.sleep(sec)


# def open_door():
#     servoPIN = 17
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(servoPIN, GPIO.OUT)
#     servo = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
#     servo.start(0)
#     set_angle(servo, 160, 0.5)
#     set_angle(servo, 0, 0.5)
#     servo.stop()
#     time.sleep(5)


def open_door():
    publish.single(
        "app/door", "door", hostname=ip, auth={"username": user, "password": password},
    )
    time.sleep(5)


def save_img():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dir_path = record_path + "/" + current_time[:10]
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    cv2.imwrite(dir_path + "/" + current_time + ".jpg", frame)


for filename in os.listdir(member_path):
    # print(filename)
    image = face_recognition.load_image_file(member_path + "/" + filename)
    image_face_encoding = face_recognition.face_encodings(image)[0]
    image_face_encoding_array.append(image_face_encoding)

try:
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # on windows
    # video_capture = cv2.VideoCapture(0)

    print("Ready")
    while True:
        ret, frame = video_capture.read()
        cv2.imshow("Video", frame)
        # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                image_face_encoding_array, face_encoding
            )
            face_distances = face_recognition.face_distance(
                image_face_encoding_array, face_encoding
            )

            # print(face_distances)

            for face_distance in face_distances:
                if face_distance < 0.4:
                    print("Open")

                    # open_door()

                    # save_img()

                    # video_capture.release()
                    # video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # on windows
                    # video_capture = cv2.VideoCapture(0)
                    break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    print("STOP")

finally:
    video_capture.release()
    cv2.destroyAllWindows()
    # GPIO.cleanup()
