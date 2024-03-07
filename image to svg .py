import svgwrite
from PIL import Image

# To find near by pixel
    
def find_nearby_pixels(img, x, y, radius=1):
    width, height = img.size
    nearby_pixels = []

    for i in range(max(0, x - radius), min(width, x + radius + 1)):
        for j in range(max(0, y - radius), min(height, y + radius + 1)):
            pixel_color = img.getpixel((i, j))
            if pixel_color[0] < 128:
                nearby_pixels.append((i, j))

    return nearby_pixels

# To generate bezier (curve) path

def generate_bezier_path(x, y, nearby_pixels):
    path_data = f"M{x},{y}"

    for pixel in nearby_pixels:
        path_data += f" C{(x + pixel[0]) / 2},{(y + pixel[1]) / 2} {(x + pixel[0]) / 2},{(y + pixel[1]) / 2} {pixel[0]},{pixel[1]}"

    return path_data

# To convert image like jpeg ,png etc into svg or vactor file

def image_to_svg(input_image_path, output_svg_path, line_length=5):
    # Open the image
    img = Image.open(input_image_path)

    # A5 size in millimeters
    a4_width_mm = 210
    a4_height_mm = 297

    # Calculate DPI (dots per inch) for the A4 size
    dpi = 96  # Standard screen DPI
    a4_width = int((a4_width_mm / 25.4) * dpi)
    a4_height = int((a4_height_mm / 25.4) * dpi)

    # Create an SVG drawing with A4 size
    dwg = svgwrite.Drawing(output_svg_path, profile='tiny', size=(a4_width, a4_height))

    # Iterate over each pixel and create SVG curved lines
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            pixel_color = img.getpixel((x, y))
            if pixel_color[0] < 128:  # Adjust the condition based on your image
                # Find nearby pixels and connect with a curved line
                nearby_pixels = find_nearby_pixels(img, x, y)
                if nearby_pixels:
                    path_data = generate_bezier_path(x, y, nearby_pixels)
                    dwg.add(dwg.path(d=path_data, stroke='black', fill='none'))

    # Save SVG file
    dwg.save()


# import and export location
input_image_path = r"C:\Users\rytha\Desktop\image to svg\input_image\WhatsApp Image 2023-11-27 at 3.52.34 PM.jpeg" # import location
output_svg_path = r"C:\Users\rytha\Desktop\image to svg\output_gcodes\output_curved_lines_a4_1.svg" # export location
image_to_svg(input_image_path, output_svg_path)
print("DONE! CHECK THE SVG FILE.")

#