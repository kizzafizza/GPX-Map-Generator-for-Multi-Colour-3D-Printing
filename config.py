from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

INPUT_GPX = PROJECT_ROOT / "input" / "run.gpx"
OUTPUT_STL = PROJECT_ROOT / "output" / "route.stl"

MODEL_MAX_SIZE_MM = 150
ROUTE_WIDTH_MM = 3.0
ROUTE_HEIGHT_MM = 1.5
SIMPLIFY_TOLERANCE_MM = 0.4