import svgwrite
from PIL import Image

def image_to_svg(input_image_path, output_svg_path):
    # Open the image
    img = Image.open(input_image_path)

    # Get image dimensions
    width, height = img.size

    # Create an SVG drawing
    dwg = svgwrite.Drawing(output_svg_path, profile='tiny')

    # Start the SVG path
    path_data = []

    # Iterate over each pixel and create SVG path with cubic Bezier curves
    for y in range(height):
        for x in range(width):
            pixel_color = img.getpixel((x, y))
            if pixel_color[0] < 128:  # Adjust the condition based on your image
                # Move to the current pixel position
                path_data.append(f'M{x},{y}')

                # Add a cubic Bezier curve with control points to create a smooth connection
                path_data.append(f'C{x-0.5},{y-0.5} {x+0.5},{y-0.5} {x+1},{y}')

    # Create an SVG path using the collected path data
    dwg.add(dwg.path(d=path_data, stroke='black', fill='none'))

    # Save SVG file
    dwg.save()
# Example usage
input_image_path = r"C:\Users\rytha\Desktop\New folder\input_image\WhatsApp Image 2023-11-27 at 3.52.34 PM.jpeg"
output_svg_path = r"C:\Users\rytha\Desktop\New folder\output_gcodes\output9.gcode"
image_to_svg(input_image_path, output_svg_path)

