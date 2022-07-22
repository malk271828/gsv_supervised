# gsv_supervised

# Install

## git clone 

Type git clone command with --recursive option in order to download submodules

```shell
git clone --recursive <URL>
```

## Prerequisite

```shell
ln -s geo_sampling/geo_sampling/geo_roads.py geo_roads
ln -s geo_sampling/geo_sampling/sample_roads.py sample_roads
```

# Usage

## Manual Data Acquisition

### sample GPS locatons

get a list of region names:

```shell
geo_road -c Japan -l 2
```

```shell
geo_road -c Japan -l 2 "Shizuoka+Shizuoka" -o artifacts/roads/Shizuoka.csv
```

### fetch images with Google Map API and visualize

```shell
python src/fetch_img.py --num 10 --input artifacts/roads/Shizuoka.csv
```

```shell
python src/visualize_grid.py 
```

## Automatic


# Frequently Encountered Errors

The following error is caused by that utm module is too new

```
pyproj.exceptions.CRSError: Invalid projection: +proj=utm +zone=53S +type=crs: (Internal Proj Error: proj_create: Error 1027 (Invalid value for an argument): utm: Invalid value for zone)
```
