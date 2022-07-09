import argparse
import requests
import os

from rich import print
from base64 import b64encode, b64decode

import pandas as pd

from credentials import API_KEY

def gsv_image(lat, lon, heading=0, pitch=0, size='640x640'):
    data = {'key': API_KEY,
                'location':  '{0:f},{1:f}'.format(lat, lon),
                'heading': '{0:d}'.format(heading),
                'pitch': '{0:d}'.format(pitch),
                'size': size}
    r = requests.get('https://maps.googleapis.com/maps/api/streetview', params=data)
    if r.status_code == 200:
        return b64encode(r.content)
    else:
        print(r.status_code)
        print(r.text)
        print("WARN: No image data for {0:f},{1:f}".format(lat, lon))
        return None

def gsv_metadata(lat, lon):
    data = {'key': API_KEY,
            'location':  '{0:f},{1:f}'.format(lat, lon)}
    r = requests.get('https://maps.googleapis.com/maps/api/streetview/metadata', params=data)
    if r.status_code == 200:
        return r.json()
    else:
        print("WARN: No metadata for {0:f},{1:f}".format(lat, lon))
        return None

def export_image_to_file(data, file_path):
    url = '{0:s}'.format(file_path)
    with open(url, 'wb') as f:
        raw = b64decode(data)
        f.write(raw)
    return url

def parseArgs():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        "--num",
        required=True,
        type=int,
        help='maximum number of locations to fetch')
    argparser.add_argument(
        "--input",
        required=True,
        type=str,
        help='input csv file acquired by geo_sampling')
    argparser.add_argument(
        "--out",
        default="artifacts/",
        type=str,
        help='output dir')
    args = argparser.parse_args()
    return args

if __name__=="__main__":
    args = parseArgs()
    df = pd.read_csv(args.input)
    total = len(df)
    df = df[:args.num]

    # get metadata --------------
    # df['gsv_metadata'] = df[['start_lat', 'start_long']].apply(lambda r: gsv_metadata(r.start_lat, r.start_long), axis=1)
    # print(df["gsv_metadata"])

    for i, row in df.iterrows():
        file_path = args.out + "img_lat{0}_lon{1}.jpg".format(row.start_lat, row.start_long)
        if not os.path.exists(file_path):
            img = gsv_image(row.start_lat, row.start_long, 0, 0)
            export_image_to_file(img, file_path=file_path)
            print("[cyan] save: {0} [/cyan]".format(file_path))
        else:
            print("[green] skipped: {0} [/green]".format(file_path))

    print("{0}/{1} images".format(args.num, total))
