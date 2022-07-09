import argparse

import shapefile
import folium

def parseArgs():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        "--shp",
        required=True,
        type=str,
        help='shapefile path')
    args = argparser.parse_args()
    return args

def Type2Color(Type):
    if Type=="primary":
        color = "red"
    elif Type=="secondary":
        color= "blue"
    else:
        color= None
    return color

if __name__=="__main__":
    args = parseArgs()
    shp = shapefile.Reader(args.shp, encoding='utf-8')

    # filtering data
    geojson = shp.__geo_interface__
    print(geojson["features"][0])

    m = folium.Map(
        location=[35.56, 139.65],
        zoom_start=14,
        width=800, 
        height=800,
        tiles='openstreetmap') # マップ作成

    folium.GeoJson(geojson, name='region_name',
                style_function = lambda x: {
                    'opacity': 1 if x["properties"]["type"]=="primary" or "secondary" else 0,
                    'color': Type2Color(x["properties"]["type"])
                }
                ).add_to(m)

    folium.LayerControl().add_to(m)
    m.save('svname.html')