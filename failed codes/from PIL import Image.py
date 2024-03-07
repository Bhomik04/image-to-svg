from PIL import Image
import numpy as np

def image_to_gcode(input_image_path, output_gcode_path, max_depth=10, feed_rate=100, z_safe=5):
    # Define A4 dimensions (in millimeters)
    a4_width = 210
    a4_height = 297

    # Open the image
    img = Image.open(input_image_path).convert("L")  # Convert to grayscale

    # Resize the image to fit within A4 dimensions
    img.thumbnail((a4_width, a4_height), Image.ANTIALIAS)

    # Get resized image dimensions
    width, height = img.size

    # Calculate the scaling factors for X and Y axes
    scale_x = a4_width / width
    scale_y = a4_height / height

    # Set up G-code header
    gcode = f"G21 ; Set units to millimeters\nG90 ; Absolute positioning\nG92 X0 Y0 Z0 ; Reset position\nG1 Z{z_safe} ; Move to safe Z height\n"

    # Loop through each pixel in the resized image and convert to G-code
    for y in range(height):
        for x in range(width):
            # Get pixel intensity (0-255)
            pixel_value = img.getpixel((x, y))

            # Convert pixel intensity to depth
            depth = max_depth - (pixel_value / 255) * max_depth

            # Scale coordinates to fit within A4 dimensions
            scaled_x = x * scale_x
            scaled_y = y * scale_y

            # Add G-code command for the current pixel
            gcode += f"G1 X{scaled_x:.2f} Y{scaled_y:.2f} Z-{depth:.2f} F{feed_rate}\n"

    # Set up G-code footer
    gcode += f"G1 Z{z_safe} ; Move back to safe Z height\nM2 ; End of program\n"

    # Save the generated G-code to a file
    with open(output_gcode_path, "w") as f:
        f.write(gcode)

if __name__ == "__main__":
    input_image_path = "input_image.png"
    output_gcode_path = "output_gcode.gcode"
    image_to_gcode(input_image_path, output_gcode_path)