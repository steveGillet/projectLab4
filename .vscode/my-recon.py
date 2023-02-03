import jetson.inference
import jetson.utils

import argparse


# parse the command line
parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str, help="filename of the image to process")
parser.add_argument("--network", type=str, default="googlenet", help="model to use, can be:  googlenet, resnet-18, ect.")
args = parser.parse_args()


#load the image
img = jetson.utils.loadImage(args.filename)

