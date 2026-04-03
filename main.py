import tkinter as tk
from tkinter import messagebox
from pyfirmata2 import Arduino, util
import time
import basic_functions as bf
import webcam as wc
# ----------------------------------------------------
# Initialize Python Recognition of Arduino and Tkinter
# ----------------------------------------------------
board = Arduino("COM3")
time.sleep(2)  # Delay for initialize time
it = util.Iterator(board)  # Background thread dedicated to reading Arduino Data
it.start()
win = tk.Tk()  # Initialize Window Identifier
# ==========================================
# PyFirmata(2) Pin .mode Documentation
# ------------------------------------
# 0 = INPUT ; Used for .read() ; Returns True (HIGH), False (LOW), None (Not Ready)
# 1 = OUTPUT ; Used for .write(1/0) ; 1 = High, 0 = Low
# 2 = ANALOG ; Used for .read() ; Returns 0.0-1.0
# 3 = PWM / SERVO ; PWM used for .write(0-1) ; SERVO used for .write(0-180)
# =========================================================================


def ledSwitchGUI(digitalPin):  # Creates a Tkinter GUI for turning a wired LED on and off
    """
    ledSwitchGUI creates a GUI for turning an LED on or off via input digitalPin turning on or off
    :param digitalPin:
    :return:
    """
    # Initialize window with title and min-size
    win.title("L E D")
    win.minsize(200, 60)
    # Label widget and placement
    label = tk.Label(win, text="click to turn ON/OFF")
    label.grid(column=1, row=1)
    # On-Off Button widgets and placements
    ONbtn = tk.Button(win, bd=4, text="LED ON", command=lambda: bf.digPin_ON(digitalPin, board))
    ONbtn.grid(column=1, row=2)
    OFFbtn = tk.Button(win, bd=4, text="LED OFF", command=lambda: bf.digPin_OFF(digitalPin, board))
    OFFbtn.grid(column=2, row=2)
    # Run window
    win.mainloop()


def servoMotorGUI(servoPin):
    """
    servoMotorGUI creates a GUI for rotating a Servo-Motor via 0-180 sliding bar. Input servoPin is the Servo-Motor
    signal pin
    :param servoPin:
    :return:
    """
    # Initialize window with title and min-size
    win.title("ServoMotor Control")
    win.minsize(235, 150)
    # Scale widget and placement
    s_motor_angle = tk.Scale(win, bd=5, from_=0, to=180, orient=tk.HORIZONTAL,
                             command=lambda val: bf.servoAngle(int(val), servoPin, board))
    s_motor_angle.grid(column=1, row=1)
    # Label widget and placement
    tk.Label(win, text="Angle of ServoMotor").grid(column=1, row=2)
    # Run window
    win.mainloop()


if __name__ == "__main__":
    # ------------- Confirm closing ------------------------------------------
    win.protocol("WM_DELETE_WINDOW", lambda: bf.on_closing(board, win))
    # ========================================================================

    # tk._test()
    # bf.sanityCheck(board)
    # ledSwitchGUI(3)
    # servoMotorGUI(9)
    # wc.color_tracking_old()
    # wc.coloredObjTracking()
    exit()
