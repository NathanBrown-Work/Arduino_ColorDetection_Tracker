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

DIR = 0  # Direction of Stepper Motor, should only be 0 or 1


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


def getIntOrNone(prompt, err_msg):
    while True:
        response = input(prompt).strip().lower()
        if response == "no":
            return None
        try:
            return int(response)
        except ValueError:
            print(err_msg)


def getYesOrNo(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ("yes", "no"):
            return response
        print("Invalid Input. Please enter 'yes' or 'no'.")


def introduction():
    """
    introduction asks the user to provide required information regarding the control panel's functionality
    :return:
    """
    digital_pin = getIntOrNone(
        "If you have a pin wired for an LED, enter its number here. If not, enter 'no': ",
        "Invalid number for LED pin. Type the number or enter 'no'."
    )

    servo_pin = getIntOrNone(
        "If you have a pin wired for a Servo Motor, enter its number here. If not, enter 'no': ",
        "Invalid number for Motor Pin. Type the number or enter 'no'."
    )

    wc_plugged = getYesOrNo(
        "If you have a plugged in webcam, enter 'yes'. If not, enter 'no': "
    )

    dir_pin = getIntOrNone(
        "If you have a direction pin wired for a Stepper Motor, enter its number here. If not, enter 'no': ",
        "Invalid number for Direction Pin. Type the number or enter 'no'."
    )
    if dir_pin is not None:
        step_pin = getIntOrNone(
            "Enter your stepper motor Step Pin here: ",
            "Invalid number for a Step Pin. Type the number here: "
        )

    return digital_pin, servo_pin, wc_plugged, dir_pin, step_pin


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


def stepperTest(dir_pin, step_pin, lock, getDir, motor_state, board):
    # Move forward
    delay = 0.002  # Seconds

    step_angle = 18  # Degrees
    steps_per_rev = 360 / step_angle  # 1 Full Motor Rotation -> 20 steps at 18 degrees

    lead_screw_pitch = 0.5  # Millimeters
    steps_per_mm = steps_per_rev/lead_screw_pitch  # Steps to Move Approx 1 Millimeter -> 40 Steps at 0.5 screw pitch

    last_direction = 0

    with lock:
        board.digital[dir_pin].mode = 1
        board.digital[step_pin].mode = 1

    while not motor_state["stop"]:
        direction = getDir()  # Reads live direction
        if direction is None:
            time.sleep(delay)
            continue

        last_direction = direction

        with lock:
            board.digital[dir_pin].write(direction)
            board.digital[step_pin].write(1)

        time.sleep(delay)

        with lock:
            board.digital[step_pin].write(0)

        time.sleep(delay)


def toggleDIR():
    global DIR
    DIR = 0 if DIR == 1 else 1


def onClosing(board, win):
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
