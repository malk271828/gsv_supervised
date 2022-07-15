import argparse
import pandas
from glob import glob
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import torchvision
import torchvision.transforms.functional as F
from torchvision.utils import make_grid
from torchvision.io import read_image

from settings import OUT_DIR

def show(imgs):
    if not isinstance(imgs, list):
        imgs = [imgs]
    fig, axs = plt.subplots(ncols=len(imgs), squeeze=False)
    for i, img in enumerate(imgs):
        img = img.detach()
        img = F.to_pil_image(img)
        axs[0, i].imshow(np.asarray(img))
        axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])

def parseArgs():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        "--num",
        default=8,
        type=int,
        help='maximum number of images')
    argparser.add_argument(
        "--input",
        required=True,
        type=str,
        help='input csv file acquired by geo_sampling')
    argparser.add_argument(
        "--heading",
        default=45,
        type=int,
        help='heading direction')
    argparser.add_argument(
        "--out",
        default=OUT_DIR,
        type=str,
        help='output dir')
    args = argparser.parse_args()
    return args

if __name__=="__main__":
    args = parseArgs()
    df = pd.read_csv(args.input)
    total = len(df)
    detailMeta = False

    # sampling
    df_list = random.sample(df.values.tolist(), args.num)

    img_list = []
    for row in df_list:
        # get images by invoking Google Map APIs --------
        img_path = args.out + "img/img_lat{0}_lon{1}_heading{2}.jpg".format(row[4], row[5], args.heading)
        img = read_image(img_path)
        img_list.append(img)

    grid = make_grid(img_list, nrow=4)
    img = torchvision.transforms.ToPILImage()(grid)
    img.show()
