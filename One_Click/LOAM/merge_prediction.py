import argparse
import matplotlib.pyplot as plt
from PIL import Image
import os

def merge_images(image1_path, image2_path, output_path, alpha=0.6):
    print (image1_path, image2_path, output_path)
    # Open the first image
    img1 = Image.open(image1_path).convert("RGBA")

    # Open the second image and resize it to match the first image's size
    img2 = Image.open(image2_path).convert("RGBA")
    img2 = img2.resize(img1.size)

    # Set the opacity of the second image to 60%
    img2.putalpha(int(255 * alpha))  # Alpha channel ranges from 0 to 255

    # Merge the two images
    combined = Image.alpha_composite(img1, img2)

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
for file in files:
    file_path = os.path.join(args.pred_dir, file)
    prefix = file.split("_poly_")[0]
    output_path = os.path.join(args.output_dir, prefix+".png")
    # Call the function with the provided arguments
    merge_images(args.source, file_path, output_path)
