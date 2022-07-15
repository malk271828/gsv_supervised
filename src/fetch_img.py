import argparse
import requests
import os
import json

from rich import print
from base64 import b64encode, b64decode

import pandas as pd

from credentials import API_KEY
from settings import OUT_DIR

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

def export_image_to_file(data, img_path):
    url = '{0:s}'.format(img_path)
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
    df = df[:args.num]

    for i, row in df.iterrows():
        # get metadata ----------------------------------
        meta_path = args.out + "meta/meta_lat{0}_lon{1}_heading{2}.json".format(row.start_lat, row.start_long, args.heading)
        if not os.path.exists(meta_path):
            if detailMeta:
                gsv_meta = gsv_metadata(row.start_lat, row.start_long)
                meta = pd.concat([row, pd.Series(gsv_meta)], axis=0)
            else:
                meta = row
            with open(meta_path, mode='w', encoding='utf-8') as fd:
                json_str = meta.to_json(orient='index')
                parsed = json.loads(json_str)
                json.dump(parsed, fd, ensure_ascii=False, indent=4)
            print("[cyan] save: {0} [/cyan]".format(meta_path))
        else:
            print("[green] skipped: {0} [/green]".format(meta_path))

        # get images by invoking Google Map APIs --------
        img_path = args.out + "img/img_lat{0}_lon{1}_heading{2}.jpg".format(row.start_lat, row.start_long, args.heading)
        if not os.path.exists(img_path):
            img = gsv_image(row.start_lat, row.start_long, args.heading, 0)
            export_image_to_file(img, img_path=img_path)
            print("[cyan] save: {0} [/cyan]".format(img_path))
        else:
            print("[green] skipped: {0} [/green]".format(img_path))

    print("{0}/{1} images".format(args.num, total))
