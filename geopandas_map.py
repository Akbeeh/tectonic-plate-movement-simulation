"""
This module is used to simulate the movement of tectonic plates using GeoPandas.
"""
import random
import time
from typing import List

import geopandas as gpd
import matplotlib.pyplot as plt
import shapely
from geojson_map import TectonicPlateGenerator
from shapely.affinity import translate
from shapely.geometry import shape

# Help from https://geopandas.org/en/stable/docs.html


class TectonicPlateSimulator:
    """
    This class is used to simulate the movement of tectonic plates.
    At the beginning, the tectonic plates are randomly generated.
    """

    def __init__(self, geojson_file):
        TectonicPlateGenerator().save_world_map()
        self.world_map = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        self.gdf = gpd.read_file(geojson_file)
        self.gdf["color"] = [
            plt.cm.jet(i / len(self.gdf)) for i in range(len(self.gdf))
        ]
        self.init_plot()

    def init_plot(self) -> None:
        """
        This method initializes the plot.
        """
        plt.ion()  # Turn on interactive mode
        self.fig, self.axis = plt.subplots(figsize=(12, 6))

    def move_plate(
        self, plate, x_offset: int, y_offset: int
    ) -> shapely.geometry.polygon.Polygon:
        """This method moves a plate by x_offset and y_offset.
        It also handles boundary crossings.

        Args:
            plate: The plate to move.
            x_offset (int): The x offset.
            y_offset (int): The y offset.

        Returns:
            shapely.geometry.polygon.Polygon: The moved plate.
        """
        new_geometry = translate(plate["geometry"], x_offset, y_offset)

        # Handle boundary crossings
        plate_shape = shape(new_geometry)
        x_boundary = 180  # Longitude limits (-180 to 180)
        y_boundary = 90  # Latitude limits (-90 to 90)

        # Check if the plate crosses the x boundaries
        if plate_shape.bounds[0] > x_boundary:
            new_geometry = translate(new_geometry, -2 * x_boundary, 0)
        elif plate_shape.bounds[2] < -x_boundary:
            new_geometry = translate(new_geometry, 2 * x_boundary, 0)

        # Check if the plate crosses the y boundaries
        if plate_shape.bounds[1] > y_boundary:
            new_geometry = translate(new_geometry, 0, -2 * y_boundary)
        elif plate_shape.bounds[3] < -y_boundary:
            new_geometry = translate(new_geometry, 0, 2 * y_boundary)

        return new_geometry

    def check_for_collision(self, i_plate: int, plate) -> List[int]:
        """This method checks for collisions between plates.

        Args:
            i_plate (int): The index of the plate.
            plate: The plate to check for collisions.

        Returns:
            List[int]: The x and y offsets.
        """
        x_offset = random.randint(-4, 4)  # Adjust the movement speed here
        y_offset = random.randint(-4, 4)
        # Check for collisions
        for j, other_plate in self.gdf.iterrows():
            if i_plate != j and self.gdf.at[i_plate, "geometry"].intersects(
                other_plate["geometry"]
            ):
                # Move the plate away from the other plate
                x_offset *= -1
                y_offset *= -1
                # print(f"Collisions between {plate['name']} and {other_plate['name']}!")
                break

        return x_offset, y_offset

    def run_simulation(self, n_steps: int = 100) -> None:
        """This method runs the simulation.
        It moves the plates and updates the plot.
        It checks for collisions between plates and handles boundary crossings.

        Args:
            n_steps (int, optional): The number of steps to run the simulation for. Defaults to 100.
        """
        for _ in range(n_steps):
            for i, plate in self.gdf.iterrows():
                x_offset, y_offset = self.check_for_collision(i, plate)
                self.gdf.at[i, "geometry"] = self.move_plate(plate, x_offset, y_offset)

            self.update_plot()
            time.sleep(0.25)  # Pause to control the animation speed (in seconds)

    def update_plot(self) -> None:
        """
        This method updates the plot.
        """
        self.axis.clear()
        self.axis.set(
            xlabel="Longitude",
            ylabel="Latitude",
            title="Dynamic Tectonic Plate Movement",
        )
        self.axis.set_xlim([-180, 180])
        self.axis.set_ylim([-90, 90])
        self.fig.set_size_inches(12, 6)

        self.world_map.plot(ax=self.axis)

        for _, plate in self.gdf.iterrows():
            # Access the plate and centroid for annotation
            centroid = plate["geometry"].centroid
            name = plate["name"]
            x_coord, y_coord = centroid.x, centroid.y

            # Annotate the plate
            self.axis.annotate(
                name,
                xy=(x_coord, y_coord),
                color="w",
                fontsize=8,
                ha="center",
                va="center",
            )

        self.gdf.plot(
            ax=self.axis,
            color=self.gdf["color"],
        )
        self.fig.canvas.flush_events()

    def close(self) -> None:
        """
        This method closes the plot.
        """
        plt.ioff()  # Turn off interactive mode
        plt.close()


if __name__ == "__main__":
    simulator = TectonicPlateSimulator("world_map.geojson")
    try:
        simulator.run_simulation(500)
    except KeyboardInterrupt:
        pass
    finally:
        simulator.close()
