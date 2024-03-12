import argparse
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import os
import json

def merge_images(image1_path, image2_path, output_path, item_area, alpha=0.6):
    lower_left_x, lower_left_y = item_area[0]
    upper_right_x, upper_right_y = item_area[1]
    w = upper_right_x - lower_left_x
    h = lower_left_y - upper_right_y
    box_coords = (lower_left_x, upper_right_y, upper_right_x, lower_left_y)
    print (image1_path, image2_path, output_path, box_coords)
    # Open the first image
    img1 = Image.open(image1_path).convert("RGBA")

    # Open the second image and resize it to match the first image's size
    img2 = Image.open(image2_path).convert("RGBA")
    img2 = img2.resize(img1.size)

    # Set the opacity of the second image to 60%
    img2.putalpha(int(255 * alpha))  # Alpha channel ranges from 0 to 255

    # Merge the two images
    combined = Image.alpha_composite(img1, img2)

    combined = combined.convert("RGB")
    #rect = plt.Rectangle((lower_left_x, lower_left_y), w, h, linestyle="-", edgecolor="red", linewidth=1)
    draw = ImageDraw.Draw(combined)
    draw.rectangle(box_coords, outline="red", width=5)

    # Save the merged image
    combined.save(output_path)

# Set up argument parsing
parser = argparse.ArgumentParser(description='Merge two images with the second image having 60% opacity.')
parser.add_argument('--source', help='Path to the source map')
parser.add_argument('--pred_dir', help='Directory to predictions')
parser.add_argument('--output_dir', help='Directory for the output images')

# Parse arguments
args = parser.parse_args()
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

files = os.listdir(args.pred_dir)
name = os.path.basename(args.source).split(".")[0]
print (name)
with open(args.source.replace(".tif", ".json"), "r") as f:
    info = json.load(f)
#print (info["shapes"])
output_dir = os.path.join(args.output_dir, name)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
area = {}
for shape in info["shapes"]:
    area[shape["label"]] = shape["points"]
for file in files:
    if not name in file: continue
    file_path = os.path.join(args.pred_dir, file)
    prefix = file.split("_poly_")[0]
    output_path = os.path.join(output_dir, prefix+".png")
    item_name = file[len(name)+1:-len("_predict.png")]
    print ("item:", item_name)
    item_area = area[item_name]
    # Call the function with the provided arguments
    merge_images(args.source, file_path, output_path, item_area)
