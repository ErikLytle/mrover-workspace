import Adafruit_BBIO.PWM as PWM
import lcm
from rover_msgs import ServoCmd


# Don't know if this is the same for the servo we're using
SERVO_MAX_DC = 10.0
SERVO_MIN_DC = 4.0

ammonia_blue = "P9_14"
amino_blue = "P9_16"

ammonia_white = "P8_13"
amino_white = "P8_19"

ammonia_yellow = "P9_21"
amino_yellow = "P9_22"

lcm_ = lcm.LCM()


def angle_to_dc(degrees):
    percent = degrees / 120.0
    dc = SERVO_MIN_DC + (percent * (SERVO_MAX_DC - SERVO_MIN_DC))
    return dc


def run_servo(pin, degrees):
    dc = angle_to_dc(degrees)
    PWM.set_duty_cycle(pin, dc)


def servo_init(pin, degrees):
    dc = angle_to_dc(degrees)
    PWM.start(pin, dc, 50)


def servocmd_callback(channel, msg):
    servo = ServoCmd.decode(msg)

    # Blue callback
    if (servo.id == "amino_blue"):
        run_servo(amino_blue, servo.position)
    elif (servo.id == "ammonia_blue"):
        run_servo(ammonia_blue, servo.position)

    # White callback
    elif (servo.id == "amino_white"):
        run_servo(amino_white, servo.position)
    elif (servo.id == "ammonia_white"):
        run_servo(ammonia_white, servo.position)

    # Yellow callback
    elif (servo.id == "amino_yellow"):
        run_servo(amino_yellow, servo.position)
    elif (servo.id == "ammonia_yellow"):
        run_servo(ammonia_yellow, servo.position)


def main():

    servo_init(amino_blue, 0)
    servo_init(ammonia_blue, 0)

    servo_init(amino_white, 0)
    servo_init(ammonia_white, 0)

    servo_init(amino_yellow, 0)
    servo_init(ammonia_yellow, 0)
    # Might need a manual set to 0, not sure if init sets to angle 0 initially

    lcm_.subscribe("/servo_cmd", servocmd_callback)

    while(1):
        lcm_.handle()
