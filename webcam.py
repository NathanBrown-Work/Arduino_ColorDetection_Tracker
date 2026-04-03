import cv2
import numpy as np


def color_tracking_old():
    cap = cv2.VideoCapture(0)

    # --- HSV Color Ranges ---
    # Blue
    lower_blue = np.array([90, 80, 100])
    upper_blue = np.array([130, 255, 255])

    # Red (wraps around hue range)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    while True:
        isTrue, bgr_frame = cap.read()
        if not isTrue:
            break

        hsv_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)

        # --- Create color masks ---
        mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)
        mask_red1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)

        # Combine both masks
        combined_mask = cv2.bitwise_or(mask_blue, mask_red)

        # Optional cleanup
        kernel = np.ones((5, 5), np.uint8)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)

        # --- Create isolated color frame (only red and blue visible) ---
        color_only_frame = cv2.bitwise_and(bgr_frame, bgr_frame, mask=combined_mask)

        # --- Count blue objects ---
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blue_count = sum(1 for c in contours_blue if cv2.contourArea(c) > 500)

        # --- Count red objects ---
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        red_count = sum(1 for c in contours_red if cv2.contourArea(c) > 500)

        # --- Overlay counts and deliver to Teensy ---
        data = f"{blue_count},{red_count}\n".encode()
        cv2.putText(color_only_frame, f"Blue Objects: {blue_count}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(color_only_frame, f"Red Objects: {red_count}", (20, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # --- Show only the color detections ---
        cv2.imshow('Color Detection', color_only_frame)

        # ----------------------End Program By Hitting 's'----------------------
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    cap.release()
    cv2.destroyAllWindows()


def coloredObjTracking():
    cap = cv2.VideoCapture(0)

    # HSV Values
    lower_blue = np.array([90, 80, 100])
    upper_blue = np.array([130, 255, 255])

    while True:
        isTrue, bgr_frame = cap.read()
        if not isTrue:
            break

        # --- Convert frame from BGR to HSV ---
        hsv_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)
        # --- Create color mask ---
        mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)
        # --- Create isolated color frame (only red and blue visible) ---
        color_only_frame = cv2.bitwise_and(bgr_frame, bgr_frame, mask=mask_blue)
        # --- Find blue contours and determine center of largest contour ---
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cx, cy = -1, -1  # default if nothing found

        if contours_blue:
            # Get the largest contour by area
            largest_blue = max(contours_blue, key=cv2.contourArea)

            if cv2.contourArea(largest_blue) > 500:
                # Compute centroid using moments
                # Documentation briefing on moments:
                # https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html
                M = cv2.moments(largest_blue)

                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # Draw center point
                    cv2.circle(color_only_frame, (cx, cy), 6, (0, 255, 0), -1)

                    # Show coordinates
                    cv2.putText(color_only_frame, f"({cx},{cy})",
                                (cx + 10, cy),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, (0, 255, 0), 2)

        # --- Show the results ---
        cv2.imshow('Color Detection', color_only_frame)

        # ----------------------End Program By Hitting 's'----------------------
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    cap.release()
    cv2.destroyAllWindows()
