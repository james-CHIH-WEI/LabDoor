import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time


def angle_to_duty_cycle(angle):
    duty_cycle = (0.05 * 50) + (0.19 * 50 * angle / 180)
    return duty_cycle


def set_angle(servo, angle, sec):
    duty_cycle = angle_to_duty_cycle(angle)
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(sec)


def open_door():
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    servo = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
    servo.start(0)
    # set_angle(servo, 160, 0.5)
    # set_angle(servo, 0, 0.5)
    servo.stop()
    time.sleep(5)
    GPIO.cleanup()


def on_connect(client, userdata, flags, rc):
    print("ready")

    client.subscribe("app/door")


def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode("utf-8"))
    topic = msg.topic
    if topic == "app/door":
        print("linebot open")
        open_door()


client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message

client.username_pw_set("hiot", "12345678")

client.connect("healthcareiot.ntunhs.edu.tw", 1883, 60)


try:
    client.loop_forever()

except KeyboardInterrupt:
    print("STOP")

finally:
    GPIO.cleanup()


# mosquitto_pub -h healthcareiot.ntunhs.edu.tw -t app/door -u hiot -P 12345678 -m 1
