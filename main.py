import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Concept for Kinematic Equations Loop
"""
l1 = 4
l2 = 7
theta1 = np.radians(120)
theta2 = np.radians(56)

x_final = l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2)
y_final = l1 * np.sin(theta1) + l2 * np.sin(theta1 + theta2)
    In theory:
    robot_len = [2, 5, 3, 2, 4]
    robot_theta = [46, 50, 120, 80, 47]
    robot_theta_cum = 0
    x_cords = [0]
    y_cords = [0]
    for i in range(len(robot_len)):
        robot_theta_cum += np.radians(robot_theta[i])
        x_cords.append(x_cords[-1] + robot_len[i] * np.cos(robot_theta_cum))
        y_cords.append(y_cords[-1] + robot_len[i] * np.sin(robot_theta_cum))
"""


def robotArmCalc(robot_lens, robot_pitches):
    """
    Calculates coordinates of each joint.
        - robot_lens: list of segment lengths
        - robot_pitches: list of pitch angles (X-Y plane) in degrees
    """
    robot_pitches_cum = 0
    x_cords = [0]
    y_cords = [0]
    for i in range(len(robot_lens)):
        robot_pitches_cum += np.radians(robot_pitches[i])
        x_cords.append(x_cords[-1] + robot_lens[i] * np.cos(robot_pitches_cum))
        y_cords.append(y_cords[-1] + robot_lens[i] * np.sin(robot_pitches_cum))

    return x_cords, y_cords


def intersect_test(p1, p2, q1, q2):
    """
    Check if segment p1->p2 intersects segment q1->q2:
        - First check, do p1->p2 lie opposite of q1->q2
        - Second check, do q1->q2 lie opposite of p1->p2
            - If both True, segments intersect and return True
            - Otherwise, return False
    """
    def ccw(a, b, c):
        """
        Counterclockwise test via determinant to achieve orientation:
            - If det > 0, a->b->c is counterclockwise, which returns True
            - Otherwise, returns False
        """
        return (c[1]-a[1])*(b[0]-a[0]) > (b[1]-a[1])*(c[0]-a[0])
    return (ccw(p1, q1, q2) != ccw(p2, q1, q2)) and (ccw(p1, p2, q1) != ccw(p1, p2, q2))


def self_collision_test(x_cords, y_cords):
    segments = len(x_cords)-1
    for i in range(segments):
        for j in range(i+2, segments): # skip adjacent links
            p1 = (x_cords[i], y_cords[i])
            p2 = (x_cords[i+1], y_cords[i+1])
            q1 = (x_cords[j], y_cords[j])
            q2 = (x_cords[j+1], y_cords[j+1])
            if intersect_test(p1, p2, q1, q2):
                return True
    return False


def plotGraph3D(robot_lens, robot_pitches, robot_yaw=0, segment_width=0.2, segment_height=0.2):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect('equal')

    x_cords, y_cords = robotArmCalc(robot_lens, robot_pitches)

    if self_collision_test(x_cords, y_cords):
        print("Warning: Arm crosses itself!")
        ax.set_title("Self-Collision Detected!")
    else:
        ax.set_title("Robot Arm Kinematics")

    # if robot_yaw is None:
        # z_cords = [0] * len(x_cords)
    z_cords = [0] * len(x_cords)

    for i in range(len(x_cords) - 1):
        p0 = np.array([x_cords[i], y_cords[i], z_cords[i]])
        p1 = np.array([x_cords[i + 1], y_cords[i + 1], z_cords[i + 1]])

        # Direction vector
        d = p1 - p0
        d = d / np.linalg.norm(d)

        # First perpendicular (use global z unless parallel)
        perp1 = np.cross(d, np.array([0, 0, 1]))
        if np.linalg.norm(perp1) == 0:
            perp1 = np.cross(d, np.array([0, 1, 0]))
        perp1 = perp1 / np.linalg.norm(perp1) * (segment_width / 2)

        # Second perpendicular (orthogonal to both)
        perp2 = np.cross(d, perp1)
        perp2 = perp2 / np.linalg.norm(perp2) * (segment_height / 2)

        # 8 corners of the box
        corners = []
        for base in [p0, p1]:
            for s1 in [-1, 1]:
                for s2 in [-1, 1]:
                    corners.append(base + s1 * perp1 + s2 * perp2)

        # Define faces (6 sides)
        faces = [
            [corners[0], corners[1], corners[3], corners[2]],
            [corners[4], corners[5], corners[7], corners[6]],
            [corners[0], corners[1], corners[5], corners[4]],
            [corners[2], corners[3], corners[7], corners[6]],
            [corners[0], corners[2], corners[6], corners[4]],
            [corners[1], corners[3], corners[7], corners[5]],
        ]

        poly = Poly3DCollection(faces, facecolor='skyblue', edgecolors='navy', alpha=0.9)
        ax.add_collection3d(poly)

    # Plot joints
    ax.scatter(x_cords, y_cords, z_cords, color='red')
    ax.set_zlim(-1, 1)

    ax.set_xlabel('X-axis', fontsize=10, labelpad=10)
    ax.set_ylabel('Y-axis', fontsize=10, labelpad=10)
    ax.set_zlabel('Z-axis', fontsize=10, labelpad=10)
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=38, azim=38, roll=116)
    plt.show()


def plotGraph2D(robot_lens, robot_pitches, segment_width=0.2):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')

    x_cords, y_cords = robotArmCalc(robot_lens, robot_pitches)

    if self_collision_test(x_cords, y_cords):
        print("Warning: Arm crosses itself!")
        ax.set_title("Self-Collision Detected!")
    else:
        ax.set_title("Robot Arm Kinematics")

    for i in range(len(x_cords)-1):
        x0, y0 = x_cords[i], y_cords[i]
        x1, y1 = x_cords[i+1], y_cords[i+1]

        # Segment direction
        dx = x1 - x0
        dy = y1 - y0
        length = np.hypot(dx, dy)
        if length == 0:
            continue

        # Unit perpendicular vector
        perp_x = -dy / length
        perp_y = dx / length

        # Rectangle corners
        corners = [
            (x0 + perp_x*segment_width/2, y0 + perp_y*segment_width/2),
            (x0 - perp_x*segment_width/2, y0 - perp_y*segment_width/2),
            (x1 - perp_x*segment_width/2, y1 - perp_y*segment_width/2),
            (x1 + perp_x*segment_width/2, y1 + perp_y*segment_width/2)
        ]

        poly = Polygon(corners, closed=True, facecolor='skyblue', edgecolor='navy')
        ax.add_patch(poly)

    ax.plot(x_cords, y_cords, 'o', color='red')  # joint markers
    ax.set_xlabel('X-axis', fontsize=10, labelpad=10)
    ax.set_ylabel('Y-axis', fontsize=10, labelpad=10)
    plt.show()

"""
class RobotArm:
    def __init__(self, links):
        self.links = links

    def greet(self):
        print("Hello " + str(self.links))
"""

if __name__ == "__main__":
    """
    Example: valid 3-segment arm:   [3,2,1], [45,90,90]
             invalid 3-segment arm: [3,2,8], [0,135,140]
    """
    #plotGraph3D([3, 2, 8], [0, 135, 140])
    #r1 = RobotArm(2)
    #print(r1.links)
    #r1.greet()
    segments = int(input("Enter how many segments your robot arm has: "))
    user_input = input("Enter segment lengths, bottom to top, separated by spaces: ")
    robot_lens = [float(x) for x in user_input.strip().split()]
    if len(robot_lens) != segments:
        print("Error: Number of lengths and segment count do not match.")
        exit()
    user_input = input("Enter segment thetas marking pitch, bottom to top, separated by spaces: ")
    robot_pitches = [float(x) for x in user_input.strip().split()]
    if len(robot_pitches) != segments:
        print("Error: Number of angles and segment count do not match.")
        exit()
    user_input = input("Enter '2D' for a 2D graph, otherwise enter '3D' for a 3D graph: ").strip().upper()
    if user_input == "3D":
        plotGraph3D(robot_lens, robot_pitches)
    else:
        plotGraph2D(robot_lens, robot_pitches)
