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
    servo_status = GPIO.gpio_function(servoPIN)
    print(servo_status)
    # if servo_status == 0:
    #     GPIO.cleanup()
    #     GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    servo = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
    servo.start(0)
    # set_angle(servo, 160, 0.5)
    # set_angle(servo, 0, 0.5)
    servo.stop()
    time.sleep(5)


open_door()
