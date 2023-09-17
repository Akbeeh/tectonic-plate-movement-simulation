"""
This module is used to simulate the movement of tectonic plates using GeoPandas.
"""
import random
import time

import geopandas as gpd
import matplotlib.pyplot as plt
import shapely
from geojson_map import TectonicPlateGenerator
from shapely.affinity import translate

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
        self.init_plot()

    def init_plot(self) -> None:
        """
        This method initializes the plot.
        """
        plt.ion()  # Turn on interactive mode
        self.fig, self.ax = plt.subplots(figsize=(12, 6))

    def move_plate(
        self, plate, x_offset: int, y_offset: int
    ) -> shapely.geometry.polygon.Polygon:
        """This method moves a plate by x_offset and y_offset.

        Args:
            plate: The plate to move.
            x_offset (int): The x offset.
            y_offset (int): The y offset.

        Returns:
            shapely.geometry.polygon.Polygon: The moved plate.
        """
        new_geometry = translate(plate["geometry"], x_offset, y_offset)
        return new_geometry

    def run_simulation(self, num_steps: int = 100) -> None:
        for _ in range(num_steps):
            for i, plate in self.gdf.iterrows():
                x_offset = random.randint(-4, 4)  # Adjust the movement speed here
                y_offset = random.randint(-4, 4)
                self.gdf.at[i, "geometry"] = self.move_plate(plate, x_offset, y_offset)

            self.update_plot()
            time.sleep(2)  # Pause to control the animation speed (in seconds)

    def update_plot(self) -> None:
        self.ax.clear()
        self.ax.set(
            xlabel="Longitude",
            ylabel="Latitude",
            title="Dynamic Tectonic Plate Movement",
            xlim=(-180, 180),
            ylim=(-90, 90),
        )
        self.world_map.plot(ax=self.ax)

        # Different color for each plate
        unique_colors = [plt.cm.jet(i / len(self.gdf)) for i in range(len(self.gdf))]

        self.gdf.plot(
            ax=self.ax,
            color=unique_colors,
        )
        self.fig.canvas.flush_events()

    def close(self) -> None:
        plt.ioff()  # Turn off interactive mode
        plt.close()


if __name__ == "__main__":
    simulator = TectonicPlateSimulator("world_map.geojson")
    try:
        simulator.run_simulation()
    except KeyboardInterrupt:
        pass
    finally:
        simulator.close()
