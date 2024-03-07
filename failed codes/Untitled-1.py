from __future__ import absolute_import, division, print_function, unicode_literals
import os
import cv2 as cv
import argparse
import copy
from PIL import Image

ignore_color = (255, 255, 255)  # white
color_threshold = 10  # +- this color to be registered - might be needed due to compression alg

class ImageToGcode:
    def __init__(self, img_path, spread, nozzles, area, feedrate, offsets):
        self.img = cv.imread(img_path)
        self.output = ""
        self.out_file = os.path.splitext(os.path.abspath(img_path))[0] + ".gcode"
        self.spread = spread
        self.nozzles = int(nozzles)
        self.increment = spread / nozzles
        self.print_area = area
        self.feedrate = feedrate
        # change colors to sauces here
        self.red = (0, 0, 255)
        self.orange = (0, 152, 255)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.offsets = offsets
        self.debug_to_terminal()
        self.make_gcode()

    def make_gcode(self):
        self.output = "M106\n"  # Start Fan
        nozzle_firings = [0 for _ in range(self.img.shape[1])]
        nozzle_firings = [copy.copy(nozzle_firings) for _ in range(4)]  # assuming 4 nozzles
        scan = range(self.img.shape[0])
        scan = reversed(scan)
        for y in scan:
            for x in range(self.img.shape[1]):
                color = tuple(self.img[y, x])

                if color == ignore_color:
                    pass
                elif color == self.red:
                    nozzle_firings[0][x] += 1 << y % self.nozzles
                elif color == self.orange:
                    nozzle_firings[1][x] += 1 << y % self.nozzles
                elif color == self.green:
                    nozzle_firings[2][x] += 1 << y % self.nozzles
                elif color == self.black:
                    nozzle_firings[3][x] += 1 << y % self.nozzles
                else:
                    pass

            if y % self.nozzles == 0 and y > 0:
                for head_number, head_vals in enumerate(nozzle_firings):
                    for column, firing_val in enumerate(head_vals):
                        if firing_val:
                            current_offset = self.offsets[head_number]
                            self.output += "G1 X" + str(
                                self.increment * column - current_offset[0]) + " Y" + str(
                                y / 12 * self.spread - current_offset[1]) + " F" + str(self.feedrate) + "\n"
                            self.output += "M400\n"
                            self.output += "M700 P" + str(head_number) + " S" + str(firing_val) + "\n"
                nozzle_firings = [0 for _ in range(self.img.shape[1])]
                nozzle_firings = [copy.copy(nozzle_firings) for _ in range(4)]

        with open(self.out_file, 'w') as f:
            f.write(self.output)

    def debug_to_terminal(self):
        print("Rows: " + str(self.img.shape[0]))
        print("Cols: " + str(self.img.shape[1]))
        print("Spread: " + str(self.spread) + "mm")
        print("Nozzles: " + str(self.nozzles))
        print("Print Area: " + str(self.print_area) + "mm")
        row_str = ""
        for y in range(self.img.shape[0]):
            row_str = ""
            for x in range(self.img.shape[1]):
                color = tuple(self.img[y, x])

                if color == self.red:
                    row_str += "\033[91m \033[0m"  # Red color in terminal
                elif color == self.green:
                    row_str += "\033[92m \033[0m"  # Green color in terminal
                elif color == self.white:
                    row_str += "\033[97m \033[0m"  # White color in terminal
                elif color == self.orange:
                    row_str += "\033[93m \033[0m"  # Yellow color in terminal
                elif color == self.black:
                    row_str += " "
                else:
                    print(color)
                    row_str += "\033[97m \033[0m"  # Default to white color in terminal
            print(row_str)


def process_images(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each image in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_output.gcode")
            image_processor = ImageToGcode(
                img_path=input_path,
                spread=3.175,  # Modify spread as needed
                nozzles=12,  # Modify nozzles as needed
                area=[200, 200],  # Modify area as needed
                feedrate=1000,  # Modify feedrate as needed
                offsets=[
                    [0, 0],  # Modify offsets as needed for each nozzle
                    [30.5, 0.1],
                    [0, 0],
                    [0, 0]
                ]
            )
            # Optional: Print debug info to terminal
            # image_processor.debug_to_terminal()


if __name__ == "__main__":
    input_folder_path = "C:\\Users\\rytha\\Desktop\\New folder\\input_images"
    output_folder_path ="C:\\Users\\rytha\\Desktop\\New folder\\output_gcodes"
    process_images(input_folder_path, output_folder_path)
