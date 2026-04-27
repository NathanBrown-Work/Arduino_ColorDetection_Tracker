import tkinter as tk
from tkinter import ttk
from pyfirmata2 import Arduino, util
import time
import threading
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
arduino_lock = threading.Lock()  # Required to Thread Arduino Safely
tracking_lock = threading.Lock()
motor_start_lock = threading.Lock()
motor_running = False  # Required for Stepper Motor Threading
motor_state = {"stop": False}  # Required for Stepper Motor Stopping
tracking_state = {
    "x": None,
    "frame_width": 640
}
# ===========================================
# PyFirmata(2) Pin .mode Documentation
# ------------------------------------
# 0 = INPUT ; Used for .read() ; Returns True (HIGH), False (LOW), None (Not Ready)
# 1 = OUTPUT ; Used for .write(1/0) ; 1 = High, 0 = Low
# 2 = ANALOG ; Used for .read() ; Returns 0.0-1.0
# 3 = PWM / SERVO ; PWM used for .write(0-1) ; SERVO used for .write(0-180)
# =========================================================================


def arduinoControlPanel(digital_pin=None, servo_pin=None, wc_plugged="no", dir_pin=None, step_pin=None):
    """
    arduinoControlPanel is an extensive function that creates a Tkinter control panel for an
    Arduino running StandardFirmata. By default, every inner command is disabled unless enabled
    via Options, and all Options are disabled unless a valid pin(s) is passed through for said
    option. webcamBlueTracker is unique in not requiring a pin, but a "yes" string response.

    Current supported Options are an LED Switch, Servo Motor Rotator, Blue Object Tracking via
    Webcam, and a Camera Slider
    :param digital_pin:
    :param servo_pin:
    :param wc_plugged:
    :param dir_pin:
    :param step_pin:
    :return:
    """
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
    auto_camsld_bool = tk.BooleanVar(value=True)
    auto_camsld_check = tk.Checkbutton(option_frame, text="Enable Auto Cam Slider GUI",
                                       variable=auto_camsld_bool, state="disabled")
    if (dir_pin is not None) and (step_pin is not None):
        auto_camsld_check.config(state="normal")
    auto_camsld_check.pack()
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

    def update_tracking(x, frame_width):
        with tracking_lock:
            tracking_state["x"] = x
            tracking_state["frame_width"] = frame_width

    tk.Button(webcam_frame, bd=4, text="Start Webcam",
              command=lambda: threading.Thread(
                  target=wc.coloredObjTracking,
                  args=(update_tracking,),
                  daemon=True
              ).start()).pack()

    def webcamBlueTracker(*args):
        if blue_track_bool.get():
            webcam_frame.pack(fill="x", pady=2)
        else:
            webcam_frame.pack_forget()

    blue_track_bool.trace_add("write", webcamBlueTracker)
    webcamBlueTracker()

    # ------- camSldGUI -------
    camsld_frame = tk.Frame(home_frame)
    tk.Label(camsld_frame,
             text="Camera Slider Options").pack()

    def startMotorThread():
        global motor_running

        with motor_start_lock:
            if motor_running:
                return
            motor_running = True
            motor_state["stop"] = False

        def dirFromTracking():
            with tracking_lock:
                x = tracking_state["x"]
                w = tracking_state["frame_width"]

            if x is None:
                return None  # Fallback

            center = w // 2
            dead_zone = 40  # Prevents Pixel Jittering

            if x < center - dead_zone:
                return 0  # Move Left
            elif x > center + dead_zone:
                return 1  # Move Right
            else:
                return None  # Stay Same

        def run():
            global motor_running
            try:
                bf.stepperTest(dir_pin,
                               step_pin,
                               arduino_lock,
                               lambda: dirFromTracking(),
                               motor_state,
                               board)
            finally:
                motor_running = False

        threading.Thread(target=run, daemon=True).start()

    tk.Button(camsld_frame, bd=4, text="Start Motor",
              command=startMotorThread).pack()
    tk.Button(camsld_frame, bd=4, text="Change Direction",
              command=lambda: bf.toggleDIR()).pack()

    def stopMotor():
        motor_state["stop"] = True

    tk.Button(camsld_frame, bd=4, text="Stop Motor",
              command=stopMotor).pack()

    def camSldGUI(*args):
        if auto_camsld_bool.get():
            camsld_frame.pack(fill="x", pady=2)
        else:
            camsld_frame.pack_forget()

    auto_camsld_bool.trace_add("write", camSldGUI)
    camSldGUI()

    # =================
    win.mainloop()


if __name__ == "__main__":
    # ------------- Confirm closing ------------------------------------------
    win.protocol("WM_DELETE_WINDOW", lambda: bf.onClosing(board, win))
    # ========================================================================
    digital_pin, servo_pin, wc_plugged, dir_pin, step_pin = bf.introduction()
    arduinoControlPanel(digital_pin, servo_pin, wc_plugged, dir_pin, step_pin)
    exit()
