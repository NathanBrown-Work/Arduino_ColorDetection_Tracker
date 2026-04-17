import time
# ------------------------------------
# PyFirmata(2) Pin .mode Documentation
# ------------------------------------
# 0 = INPUT ; Used for .read() ; Returns True (HIGH), False (LOW), None (Not Ready)
# 1 = OUTPUT ; Used for .write(1/0) ; 1 = High, 0 = Low
# 2 = ANALOG ; Used for .read() ; Returns 0.0-1.0
# 3 = PWM ; Used for .write(0.0-1.0)
# 4 = SERVO ; Used for .write(0-180)
# =========================================================================


def sanityCheck(board):  # NOTE! Upload StandardFirmware, if any code is not working, from ArduinoIDE
    """
    sanityCheck tests Python's interaction with the Arduino Mega 2560 by turning on and off the
    on-board LED (also known as digital[13]). If the LED does not turn on:
    1. Double-check StandardFirmware is uploaded to your Arduino via ArduinoIDE;
    2. Double-check the COM port you are uploading to is correct;
    3. Double-check no other application using your Arduino's COM port is active (For example, close ArduinoIDE)
    :param board:
    :return:
    """
    board.digital[13].mode = 1
    print("sanityCheck has started!")
    board.digital[13].write(1)  # turn ON
    time.sleep(3)
    board.digital[13].write(0)  # turn OFF
    print("sanityCheck has ended!")


def introduction():
    """
    introduction asks the user to provide required information regarding the control panel's functionality
    :return:
    """
    digital_pin = (input("If you have a pin wired for an LED, enter its number here. If not, enter no: ")
                   .strip().lower())
    servo_pin = (input("If you have a pin wired for a Servo Motor, enter its number here. If not, enter no: ")
                 .strip().lower())
    wc_plugged = input("If you have a plugged in webcam, enter yes. If not, enter no: ").strip().lower()

    if digital_pin == "no":
        digital_pin = None
    else:
        try:
            digital_pin = int(digital_pin)
        except ValueError:
            print("Invalid number for led pin")
            exit()
    if servo_pin == "no":
        servo_pin = None
    else:
        try:
            servo_pin = int(servo_pin)
        except ValueError:
            print("Invalid number for motor pin")
            exit()
    if wc_plugged not in ("yes", "no"):
        print("Invalid yes/no for webcam state")
        exit()
    return digital_pin, servo_pin, wc_plugged


def digPinON(digital_pin, board):
    """
    digPin_ON turns on the designated digitalPin
    :param digital_pin:
    :param board:
    :return:
    """
    board.digital[digital_pin].mode = 1
    board.digital[digital_pin].write(1)
    print(f"{digital_pin} On")


def digPinOFF(digital_pin, board):
    """
    digPin_OFF turns off the designated digitalPin
    :param digital_pin:
    :param board:
    :return:
    """
    board.digital[digital_pin].mode = 1
    board.digital[digital_pin].write(0)
    print(f"{digital_pin} Off")


def servoAngle(angle, servo_pin, board):
    """
    servoAngle writes the desired angle to the designated servoPin; Will clamp 0-180 automatically
    :param angle:
    :param servo_pin:
    :param board:
    :return:
    """
    board.digital[servo_pin].mode = 4
    angle = max(0, min(180, int(angle)))
    board.digital[servo_pin].write(angle)
    print(f"{angle} Achieved")


def stepperTest(dir_pin, step_pin, board):
    # Move forward
    delay = 0.002  # Seconds

    step_angle = 18  # Degrees
    steps_per_rev = 360 / step_angle  # 1 Full Motor Rotation -> 20 steps at 18 degrees

    lead_screw_pitch = 0.5  # Millimeters
    steps_per_mm = steps_per_rev/lead_screw_pitch  # Steps to Move Approx 1 Millimeter -> 40 Steps at 0.5 screw pitch

    board.digital[dir_pin].mode = 1
    board.digital[step_pin].mode = 1
    board.digital[dir_pin].write(1)

    for _ in range(int(steps_per_mm*4)):
        board.digital[step_pin].write(1)
        # time.sleep(delay)
        board.digital[step_pin].write(0)
        time.sleep(delay)


def on_closing(board, win):
    """
    on_closing ensures both the Ardunio's COM Port and Tkinter's window closes
    :param board:
    :param win:
    :return:
    """
    board.exit()
    win.destroy()


def placeHolder():
    print("This is placeholder text")

