# Arduino_ColorDetection_Tracker
Personal project to develop a functional Python-Arduino integration. This project uses OpenCV and a webcam to detect colored objects, which an Arduino will use to move a camera slide bar based on which side of the frame said object is.

This code was developed on Windows OS.

IMPORTANT! -> The step motor, in current iteration, will continuously move the desired direction WITHOUT stopping unless the object is center of the frame. Be careful not to break the pulley object due to this lack of safeguard.

IMPORTANT! -> The STL File for Foot_ThrIns_MotorSd is roughly 2mm too short. Use longer screws to actually reach (I used M3 x 12mm)

IMPORTANT! -> robotarm_generator.py is not necessary for this project's goals. It was left for documentation and convenience reasons if the user wants to use it. The entire file runs independently from the rest and has its own main.

Camera Slider Components (Amazon Link Attached):
1. 2020 V Slot Aluminum Extrusion Linear Rail (11.81 Inches) (https://www.amazon.com/dp/B087PVM2NT?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)
2. Nema 17 Stepper Motor 12V 0.4A (https://www.amazon.com/dp/B00PNEQ9T4?ref=ppx_yo2ov_dt_b_fed_asin_title)
3. Small V-Wheel Plate 65mm x 65mm for 2020V Aluminum (https://www.amazon.com/dp/B0CHRYLV1V?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)
4. GT2 Timing Belt Pulley 2mm Pitch 6mm Wide ---> https://www.amazon.com/dp/B07XG9JN5B?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1
5. 5mm 20 Teeth Pulley Wheel -----------------/\
6. 12V 5A Power Supply and Adapter for Wires (https://www.amazon.com/dp/B01GEA8PQA?ref=ppx_yo2ov_dt_b_fed_asin_title)
7. Ball Bearing 6mm x 19mm x 6mm (https://www.amazon.com/dp/B07FMV2ZHR?ref=ppx_yo2ov_dt_b_fed_asin_title)
8. Attached STL Files (Expects heat-set threaded inserts for Foot files. They are designed for M3 x 8mm screws, while the four screws
   for mounting the motor are M3 x 6mm. PLEASE READ IMPORTANT ABOVE ABOUT MotorSd!
