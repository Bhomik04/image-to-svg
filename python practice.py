import svgwrite
from PIL import Image

def image_to_svg(input_image_path, output_svg_path, line_length=3):
    # Open the image
    img = Image.open(input_image_path)

    # Get image dimensions
    width, height = img.size

    # Create an SVG drawing
    dwg = svgwrite.Drawing(output_svg_path, profile='tiny')

    # Iterate over each pixel and create SVG curved lines
    for y in range(height):
        for x in range(width):
            pixel_color = img.getpixel((x, y))
            if pixel_color[0] < 128:  # Adjust the condition based on your image
                # Find nearby pixels and connect with a curved line
                nearby_pixels = find_nearby_pixels(img, x, y)
                if nearby_pixels:
                    path_data = generate_bezier_path(x, y, nearby_pixels)
                    dwg.add(dwg.path(d=path_data, stroke='black', fill='none'))

    # Save SVG file
    dwg.save()

def find_nearby_pixels(img, x, y, radius=1):
    width, height = img.size
    nearby_pixels = []

    for i in range(max(0, x - radius), min(width, x + radius + 1)):
        for j in range(max(0, y - radius), min(height, y + radius + 1)):
            pixel_color = img.getpixel((i, j))
            if pixel_color[0] < 128:
                nearby_pixels.append((i, j))

    return nearby_pixels

def generate_bezier_path(x, y, nearby_pixels):
    path_data = f"M{x},{y}"

    for pixel in nearby_pixels:
        path_data += f" C{(x + pixel[0]) / 2},{(y + pixel[1]) / 2} {(x + pixel[0]) / 2},{(y + pixel[1]) / 2} {pixel[0]},{pixel[1]}"

    return path_data

# Example usage
input_image_path = r"C:\Users\rytha\Desktop\New folder\input_image\WhatsApp Image 2023-11-27 at 3.52.34 PM.jpeg"
output_svg_path = r"C:\Users\rytha\Desktop\New folder\output_gcodes\output_curved232_lines.svg"
image_to_svg(input_image_path, output_svg_path)
print("DONE! CHECK THE SVG FILE.")
