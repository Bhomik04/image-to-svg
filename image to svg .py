import svgwrite
from PIL import Image
from skimage import measure
import numpy as np
#The code you provided uses the Ramer-Douglas-Peucker algorithm for path simplification.
 #The specific function simplify_path implements this algorithm. 
#The Ramer-Douglas-Peucker algorithm is a common algorithm used for reducing the number of points in a curve while maintaining its overall shape. 
#It works by recursively dividing a path into subpaths and eliminating points that contribute little to the overall curvature of the path, based on a user-defined tolerance. 
#This process helps to simplify complex paths and reduce the size of the resulting SVG file.


def simplify_path(points, tolerance):
    if len(points) < 3:
        return points

    np_points = np.array(points)
    distances = measure.rdist(np_points[0], np_points[-1], np_points)

    index = np.argmax(distances)

    if distances[index] > tolerance:
        left = simplify_path(np_points[:index + 1], tolerance)
        right = simplify_path(np_points[index:], tolerance)
        result = np.concatenate([left[:-1], right])
    else:
        result = np.array([np_points[0], np_points[-1]])

    return result

def find_nearby_pixels(img, x, y, radius=1):
    width, height = img.size
    nearby_pixels = []

    for i in range(max(0, x - radius), min(width, x + radius + 1)):
        for j in range(max(0, y - radius), min(height, y + radius + 1)):
            pixel_color = img.getpixel((i, j))
            if pixel_color[0] < 128:
                nearby_pixels.append((i, j))

    return nearby_pixels

def generate_smoothed_bezier_path(x, y, nearby_pixels, simplify_tolerance):
    path_data = f"M{x},{y}"

    for pixel in nearby_pixels:
        path_data += f" Q{(x + pixel[0]) / 2},{(y + pixel[1]) / 2} {pixel[0]},{pixel[1]}"

    path_commands = [item.strip() for item in path_data.split() if item.strip()]

    points = []
    for i in range(1, len(path_commands), 2):
        command = path_commands[i][0]
        coords = path_commands[i][1:].split(',')

        if command == 'Q' and len(coords) == 4:
            points.append(((x + float(coords[0])) / 2, (y + float(coords[1])) / 2))
            points.append((float(coords[0]), float(coords[1])))

    if len(points) >= 2:
        simplified_points = simplify_path(points, simplify_tolerance)

        simplified_path_data = f"M{simplified_points[0][0]},{simplified_points[0][1]}"
        for i in range(1, len(simplified_points), 2):
            simplified_path_data += f" Q{simplified_points[i][0]},{simplified_points[i][1]} {simplified_points[i + 1][0]},{simplified_points[i + 1][1]}"

        return simplified_path_data
    else:
        return path_data
# Adjusting the parameters radius, line_length, and simplify_tolerance in your code will have different effects on the output SVG file and the time it takes for the draw bot to complete the drawing.
# Here's a general explanation of what happens when you increase each parameter:

# Increase radius:
# Effect on SVG Output: A larger radius will result in a wider search for nearby pixels, potentially leading to smoother and more connected curves.
# Effect on Drawing Time: A larger radius might increase the number of pixels considered for each point, resulting in longer paths and increased drawing time.

# Increase line_length:
# Effect on SVG Output: Larger line_length will create longer individual line segments in the SVG, potentially resulting in fewer segments overall.
# Effect on Drawing Time: Longer line segments might reduce the number of commands in the SVG, potentially speeding up the drawing process.

# Increase simplify_tolerance:
# Effect on SVG Output: A larger simplify_tolerance will result in more aggressive simplification of the curves in the SVG, potentially reducing detail.
# Effect on Drawing Time: Increasing simplify_tolerance may reduce the number of points in the SVG, leading to faster processing and drawing times.


def image_to_svg(input_image_path, output_svg_path, line_length=50, radius=3, simplify_tolerance=5):
    # Open the image
    original_img = Image.open(input_image_path)

    # Resize image for processing
    new_size = (int(original_img.size[0] // 1.5), int(original_img.size[1] // 2.0))
    resized_img = original_img.resize(new_size)

    # Create an SVG drawing
    dwg = svgwrite.Drawing(output_svg_path, profile='tiny', size=(resized_img.size[0], resized_img.size[1]))

    # Iterate over each pixel and create SVG curved lines
    for y in range(0, resized_img.size[1]):
        for x in range(0, resized_img.size[0]):
            pixel_color = resized_img.getpixel((x, y))
            if pixel_color[0] < 128:
                nearby_pixels = find_nearby_pixels(resized_img, x, y, radius)
                if nearby_pixels:
                    path_data = generate_smoothed_bezier_path(x, y, nearby_pixels, simplify_tolerance)
                    dwg.add(dwg.path(d=path_data, stroke='black', fill='none'))

    # Save SVG file
    dwg.save()

# Example usage
input_image_path = r"C:\Users\rytha\Desktop\image to svg\input_image\WhatsApp Image 2023-11-27 at 3.52.34 PM.jpeg"  # import location
output_svg_path = r"C:\Users\rytha\Desktop\image to svg\output_gcodes\output_smoothed_lines_resized_1.svg"  # export location
image_to_svg(input_image_path, output_svg_path)
print("DONE! CHECK THE SVG FILE.")