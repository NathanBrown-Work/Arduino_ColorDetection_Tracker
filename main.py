import tkinter as tk
from tkinter import ttk
from pyfirmata2 import Arduino, util
import time
import basic_functions as bf
import webcam as wc
# -----------------------------------------------------------
# Initialize Python Recognition of Arduino and Tkinter Window
# -----------------------------------------------------------
board = Arduino("COM3")
time.sleep(2)  # Delay for initialize time
it = util.Iterator(board)  # Background thread dedicated to reading Arduino Data
it.start()
win = tk.Tk()  # Initialize Window Identifier
# ===========================================
# PyFirmata(2) Pin .mode Documentation
# ------------------------------------
# 0 = INPUT ; Used for .read() ; Returns True (HIGH), False (LOW), None (Not Ready)
# 1 = OUTPUT ; Used for .write(1/0) ; 1 = High, 0 = Low
# 2 = ANALOG ; Used for .read() ; Returns 0.0-1.0
# 3 = PWM / SERVO ; PWM used for .write(0-1) ; SERVO used for .write(0-180)
# =========================================================================


def arduinoControlPanel(digital_pin=None, servo_pin=None, wc_plugged="no"):
    # ============ Startup ============
    win.title("Arduino Control Panel")
    win.minsize(200, 60)
    home_frame = tk.Frame(win)
    home_frame.grid(row=0, column=0, sticky="nsew")
    option_frame = tk.Frame(win)
    option_frame.grid(row=0, column=0, sticky="nsew")
    # ================================ Options Page ================================
    tk.Label(option_frame, text="Mark Active Programs\n--------------------").pack()
    tk.Button(option_frame, bd=4, text="Return Home", command=home_frame.tkraise).pack()
    led_sw_bool = tk.BooleanVar()
    led_sw_check = tk.Checkbutton(option_frame, text="Enable LED Switch GUI",
                                  variable=led_sw_bool, state="disabled")
    if digital_pin is not None:
        led_sw_check.config(state="normal")
    led_sw_check.pack()
    servo_scl_bool = tk.BooleanVar()
    servo_scl_check = tk.Checkbutton(option_frame, text="Enable Servo Motor GUI",
                                     variable=servo_scl_bool, state="disabled")
    if servo_pin is not None:
        servo_scl_check.config(state="normal")
    servo_scl_check.pack()
    blue_track_bool = tk.BooleanVar()
    blue_track_check = tk.Checkbutton(option_frame, text="Enable Webcam Blue Tracker",
                                      variable=blue_track_bool, state="disabled")
    if wc_plugged == "yes":
        blue_track_check.config(state="normal")
    blue_track_check.pack()
    # ================================== Home Page ==================================
    tk.Label(home_frame, text="This is the Home Page\n---------------------").pack()
    tk.Button(home_frame, bd=4, text="Settings", command=option_frame.tkraise).pack()
    ttk.Separator(home_frame, orient="horizontal").pack(fill="x", pady=10)

    # -------- ledSwitchGUI --------
    led_frame = tk.Frame(home_frame)
    tk.Button(led_frame, bd=4, text="LED ON",
              command=lambda: bf.digPinON(digital_pin, board)).pack(side="left")
    tk.Button(led_frame, bd=4, text="LED OFF",
              command=lambda: bf.digPinOFF(digital_pin, board)).pack(side="right")

    def ledSwitchGUI(*args):
        if led_sw_bool.get():
            led_frame.pack(fill="x", pady=2)
        else:
            led_frame.pack_forget()

    led_sw_bool.trace_add("write", ledSwitchGUI)
    ledSwitchGUI()

    # --------- servoMotorGUI ---------
    servo_frame = tk.Frame(home_frame)
    tk.Scale(servo_frame, bd=5, from_=0, to=180, orient=tk.HORIZONTAL,
             command=lambda val: bf.servoAngle(int(val), servo_pin, board)).pack()

    def servoMotorGUI(*args):
        if servo_scl_bool.get():
            servo_frame.pack(fill="x", pady=2)
        else:
            servo_frame.pack_forget()

    servo_scl_bool.trace_add("write", servoMotorGUI)
    servoMotorGUI()

    # ------- webcamBlueTracker -------
    webcam_frame = tk.Frame(home_frame)
    tk.Label(webcam_frame,
             text="Turn off the Webcam by pressing 'S'").pack()
    tk.Button(webcam_frame, bd=4, text="Start Webcam",
              command=lambda: wc.coloredObjTracking()).pack()

    def webcamBlueTracker(*args):
        if blue_track_bool.get():
            webcam_frame.pack(fill="x", pady=2)
        else:
            webcam_frame.pack_forget()

    blue_track_bool.trace_add("write", webcamBlueTracker)
    webcamBlueTracker()
    # ============
    win.mainloop()


if __name__ == "__main__":
    # ------------- Confirm closing ------------------------------------------
    win.protocol("WM_DELETE_WINDOW", lambda: bf.on_closing(board, win))
    # ========================================================================
    # tk._test()
    # bf.sanityCheck(board)
    # ledSwitchGUI(3)
    # servoMotorGUI(9)
    # wc.colorTrackingOld()
    # wc.coloredObjTracking()
    # webcamBlueTracker()

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

    arduinoControlPanel(digital_pin, servo_pin, wc_plugged)
    exit()
