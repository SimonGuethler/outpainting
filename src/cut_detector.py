import cv2
import numpy as np


def detect_vertical_cuts(image_path):
    # Load the image
    image = cv2.imread(image_path, 0)  # Load the image in grayscale

    # Apply Canny edge detection
    edges = cv2.Canny(image, 50, 150, apertureSize=3)

    # Apply HoughLines transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

    if lines is None:
        print("No vertical cuts found in the image.")
        return

    image_height = image.shape[0]
    vertical_cuts = []

    for line in lines:
        rho, theta = line[0]

        # Convert polar coordinates to Cartesian coordinates
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho

        # Calculate the endpoints of the line
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        # Calculate the angle of the line
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

        # Check if the line is approximately vertical
        if -2 <= angle <= 2:
            # Check if the line reaches 90% or more of the image height
            line_height = abs(y2 - y1)
            if line_height >= 0.9 * image_height:
                vertical_cuts.append(line)

    if len(vertical_cuts) == 0:
        print("No vertical cuts found in the image.")
    else:
        print(f"Found {len(vertical_cuts)} vertical cuts in the image.")

        # Visualize the detected lines
        color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        for line in vertical_cuts:
            rho, theta = line[0]

            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho

            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            cv2.line(color_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        cv2.imshow("Vertical Cuts", color_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# Example usage
image_path = "path/to/your/image.jpg"
detect_vertical_cuts(image_path)

# import cv2
# import numpy as np
#
#
# def detect_vertical_cuts(image_path):
#     # Load the image
#     image = cv2.imread(image_path)
#
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # Apply Canny edge detection
#     edges = cv2.Canny(gray, 50, 150, apertureSize=3)
#
#     # Apply Hough line transform
#     lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)
#
#     # Check if any lines are detected
#     if lines is not None:
#         for line in lines:
#             rho, theta = line[0]
#
#             # Convert theta to degrees
#             theta_deg = np.rad2deg(theta)
#
#             # Check if the line is approximately vertical (+-2°)
#             if abs(theta_deg - 90) <= 2:
#                 # Get the starting and ending points of the line
#                 a = np.cos(theta) * rho
#                 b = np.sin(theta) * rho
#                 x0 = a + 1000 * (-np.sin(theta))
#                 y0 = b + 1000 * (np.cos(theta))
#                 x1 = a - 1000 * (-np.sin(theta))
#                 y1 = b - 1000 * (np.cos(theta))
#
#                 # Calculate the height of the image
#                 image_height = image.shape[0]
#
#                 # Check if the line reaches 90% or more of the image height
#                 if abs(y1 - y0) >= 0.9 * image_height:
#                     cv2.line(image, (int(x0), int(y0)), (int(x1), int(y1)), (0, 255, 0), 2)
#
#     # Display the image with detected lines
#     cv2.imshow('Vertical Cuts Detection', image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
#
# # Test the function with an image file
# image_path = 'path_to_your_image.jpg'
# detect_vertical_cuts(image_path)
