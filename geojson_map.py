"""
This module is used to generate a GeoJSON file with a world map.
"""
import random

import geojson
from shapely.geometry import shape

# Help from https://geojson.readthedocs.io/en/latest/


class TectonicPlateGenerator:
    """
    This class is used to generate a GeoJSON file with a world map
    and a number of tectonic plates.

    By default, the number of tectonic plates is 5.

    The world map coordonates are between
    -180 and 180 for longitude and -90 and 90 for latitude.
    """

    def __init__(self, num_plates: int = random.randint(5, 8)):
        self.num_plates = num_plates
        self.tectonic_plates = geojson.FeatureCollection([])

        # We want no intersection between the plates at the beginning.
        for nb_plate in range(self.num_plates):
            new_plate = self.generate_random_plate(nb_plate + 1)
            self.tectonic_plates["features"].append(new_plate)

    def generate_random_plate(self, plate_number: int) -> geojson.Feature:
        """This method generates a random tectonic plate.

        Args:
            plate_number (int): The number of the plate.

        Returns:
            geojson.Feature: The generated plate.
        """
        while True:
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-60, 60)
            plate_geometry = geojson.utils.generate_random(
                featureType="Polygon",
                numberVertices=random.randint(5, 7),
                boundingBox=[-75, -25, 75, 25],
            )
            plate_geometry["coordinates"][0] = [
                [x + x_offset, y + y_offset]
                for x, y in plate_geometry["coordinates"][0]
            ]
            new_plate = geojson.Feature(
                properties={"name": f"plate{plate_number}"},
                geometry=plate_geometry,
            )

            # Check if the new_plate is valid (no self-intersection)
            if shape(new_plate["geometry"]).is_valid and not any(
                shape(existing_plate["geometry"]).intersects(
                    shape(new_plate["geometry"])
                )
                for existing_plate in self.tectonic_plates["features"]
            ):
                return new_plate

    def save_world_map(self) -> None:
        """
        Save the world map and the tectonic plates as a GeoJSON file
        """
        with open("world_map.geojson", "w", encoding="utf-8") as geo_data_file:
            geojson.dump(
                self.tectonic_plates,
                geo_data_file,
                indent=2,
            )
        # print("Tectonic plates data generated.")

    def load_world_map(self) -> geojson.FeatureCollection:
        """Load the world map and the tectonic plates from a GeoJSON file

        Returns:
            geojson.FeatureCollection: The world map and the tectonic plates
        """
        with open("world_map.geojson", "r", encoding="utf-8") as geo_data_file:
            return geojson.load(geo_data_file)
