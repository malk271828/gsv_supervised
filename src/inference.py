

import argparse
import os
import json
import subprocess

from rich import print
from base64 import b64encode, b64decode

import pandas as pd

from credentials import API_KEY
from settings import OUT_DIR, PYTHON_PATH

def parseArgs():
    argparser = argparse.ArgumentParser(description=__doc__)
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
    argparser.add_argument(
        "--cfg",
        default="yolov7/cfg/deploy/yolov7.yaml",
        type=str,
        help='cfg file path')
    argparser.add_argument(
        "--weight",
        default="yolov7/yolov7.pt",
        type=str,
        help='weight file')
    argparser.add_argument(
        "--data",
        default=OUT_DIR + "gsv.yaml",
        type=str,
        help='data file path')
    args = argparser.parse_args()
    return args

if __name__=="__main__":
    args = parseArgs()
    df = pd.read_csv(args.input)
    detect = True

    # generate data list
    datalist_path = OUT_DIR + "datalist.txt"
    img_path_list = []
    for i, row in df.iterrows():
        # get images by invoking Google Map APIs --------
        img_path = "./img/img_lat{0}_lon{1}_heading{2}.jpg".format(row.start_lat, row.start_long, args.heading)
        img_path_list.append(img_path + "\n")

    with open(datalist_path,  "w") as fd:
        fd.writelines(img_path_list)
        print("[green]output data list file to {0}[/green]".format(datalist_path))

    # # execute inference
    if detect:
        subprocess.run(["python", "yolov7/detect.py",
            "--source", OUT_DIR + "img/",
            "--weight", args.weight,
            "--save-txt",
            "--save-conf",
            "--nosave"
        ], shell=False)
    else:
        subprocess.run(["python", "yolov7/test.py",
            "--data", args.data,
            "--weight", args.weight,
        ], shell=False)

    # delete temporary files
    if os.path.exists(datalist_path):
        os.remove(datalist_path)
        print("[cyan]delete data list file to {0}[/cyan]".format(datalist_path))
