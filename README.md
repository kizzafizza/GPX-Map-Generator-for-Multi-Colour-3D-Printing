# GPX-Map-Generator-for-Multi-Colour-3D-Printing

## Overview

GPX Map Generator is a Python-based application that converts GPS activity data (GPX files) into multi-colour 3D printable map models. The project combines activity routes with OpenStreetMap data to automatically generate print-ready STL files for routes, roads, buildings, and map bases.

## Project Goals

* Automate the creation of custom 3D printable route maps
* Eliminate manual CAD editing and mesh repair workflows
* Generate clean, watertight STL files suitable for multi-colour printing
* Support scalable production of personalised map products
* Create a foundation for a future web-based map generation platform

## Features

* Import GPX files from Strava, Garmin, Coros, Polar, and other GPS platforms
* Generate printable route geometry from activity tracks
* Download roads and building footprints from OpenStreetMap
* Export separate STL files for:

  * Base
  * Roads
  * Buildings
  * Route
* Optimised for Bambu Studio and AMS-enabled multi-colour printing
* Configurable map size, route width, and scaling

## Tech Stack

### Core Libraries

* gpxpy
* shapely
* pyproj
* trimesh
* numpy

### Data Sources

* GPX Activity Files
* OpenStreetMap (OSM)
* Terrain Elevation Data (future)

## Project Structure

```text
gpx-map-generator/
│
├── input/
│   └── sample_route.gpx
│
├── output/
│   ├── route.stl
│   ├── roads.stl
│   ├── buildings.stl
│   └── base.stl
│
├── src/
│   ├── main.py
│   ├── config.py
│   │
│   ├── gpx/
│   │   └── parser.py
│   │
│   ├── geometry/
│   │   ├── coordinates.py
│   │   ├── route_builder.py
│   │   └── mesh_builder.py
│   │
│   ├── osm/
│   │   ├── roads.py
│   │   └── buildings.py
│   │
│   └── export/
│       └── stl_exporter.py
│
├── tests/
│
├── requirements.txt
└── README.md
```
