from pathlib import Path

import gpxpy
import numpy as np
import trimesh
from pyproj import CRS, Transformer
from shapely.geometry import LineString, Polygon, MultiPolygon
from shapely.ops import unary_union
from config import (INPUT_GPX, OUTPUT_STL, MODEL_MAX_SIZE_MM, ROUTE_WIDTH_MM, ROUTE_HEIGHT_MM, SIMPLIFY_TOLERANCE_MM)


def read_gpx_points(gpx_path: Path) -> list[tuple[float, float]]:
    with open(gpx_path, "r", encoding="utf-8") as file:
        gpx = gpxpy.parse(file)

    points = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append((point.longitude, point.latitude))

    if len(points) < 2:
        raise ValueError("GPX file does not contain enough route points.")

    return points


def get_utm_crs(lon: float, lat: float) -> CRS:
    zone = int((lon + 180) / 6) + 1
    hemisphere = "north" if lat >= 0 else "south"
    return CRS.from_dict({"proj": "utm", "zone": zone, "south": hemisphere == "south"})


def convert_gps_to_xy_mm(points: list[tuple[float, float]]) -> np.ndarray:
    lon_center = np.mean([p[0] for p in points])
    lat_center = np.mean([p[1] for p in points])

    transformer = Transformer.from_crs(
        "EPSG:4326",
        get_utm_crs(lon_center, lat_center),
        always_xy=True,
    )

    xy_m = np.array([transformer.transform(lon, lat) for lon, lat in points])

    # Centre around origin
    xy_m -= xy_m.mean(axis=0)

    # Convert metres to millimetres
    xy_mm = xy_m * 1000

    # Scale to fit desired model size
    max_dimension = max(
        xy_mm[:, 0].max() - xy_mm[:, 0].min(),
        xy_mm[:, 1].max() - xy_mm[:, 1].min(),
    )

    scale_factor = MODEL_MAX_SIZE_MM / max_dimension
    xy_mm *= scale_factor

    return xy_mm


def create_route_polygon(xy_mm: np.ndarray):
    line = LineString(xy_mm)

    # Simplify slightly to avoid excessive messy geometry
    line = line.simplify(SIMPLIFY_TOLERANCE_MM, preserve_topology=True)

    # Buffer creates the printable route width
    route_polygon = line.buffer(
        ROUTE_WIDTH_MM / 2,
        cap_style="round",
        join_style="round",
    )

    return route_polygon


def polygon_to_mesh(polygon):
    meshes = []

    if isinstance(polygon, Polygon):
        polygons = [polygon]
    elif isinstance(polygon, MultiPolygon):
        polygons = list(polygon.geoms)
    else:
        polygons = list(unary_union(polygon).geoms)

    for poly in polygons:
        if not poly.is_empty and poly.area > 0:
            mesh = trimesh.creation.extrude_polygon(poly, ROUTE_HEIGHT_MM)
            meshes.append(mesh)

    if not meshes:
        raise ValueError("No valid route mesh was created.")

    return trimesh.util.concatenate(meshes)


def main():
    OUTPUT_STL.parent.mkdir(parents=True, exist_ok=True)

    print("Reading GPX...")
    points = read_gpx_points(INPUT_GPX)

    print(f"Loaded {len(points)} GPS points.")

    print("Converting GPS coordinates to model coordinates...")
    xy_mm = convert_gps_to_xy_mm(points)

    print("Creating route geometry...")
    route_polygon = create_route_polygon(xy_mm)

    print("Creating STL mesh...")
    route_mesh = polygon_to_mesh(route_polygon)

    print("Exporting STL...")
    route_mesh.export(OUTPUT_STL)

    print(f"Done. STL saved to: {OUTPUT_STL}")


if __name__ == "__main__":
    main()