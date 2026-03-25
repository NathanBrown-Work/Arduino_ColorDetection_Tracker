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
    on-board LED (also known as digitalPin 13). If the LED does not turn on:
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


def digPin_ON(digitalPin, board):
    """
    digPin_ON turns on the designated digitalPin
    :param digitalPin:
    :param board:
    :return:
    """
    board.digital[digitalPin].mode = 1
    board.digital[digitalPin].write(1)
    print(f"{digitalPin} On")


def digPin_OFF(digitalPin, board):
    """
    digPin_OFF turns off the designated digitalPin
    :param digitalPin:
    :param board:
    :return:
    """
    board.digital[digitalPin].mode = 1
    board.digital[digitalPin].write(0)
    print(f"{digitalPin} Off")


def servoAngle(angle, servoPin, board):
    """
    servoAngle writes the desired angle to the designated servoPin; Will clamp 0-180 automatically
    :param angle:
    :param servoPin:
    :param board:
    :return:
    """
    board.digital[servoPin].mode = 4
    angle = max(0, min(180, int(angle)))
    board.digital[servoPin].write(angle)
    print(f"{angle} Achieved")


def on_closing(board, win):
    """
    on_closing ensures both the Ardunio's COM Port and Tkinter's window closes
    :param board:
    :param win:
    :return:
    """
    board.exit()
    win.destroy()
