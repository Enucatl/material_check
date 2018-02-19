import click
import os
import numpy as np
from glob import glob
from tqdm import tqdm
import tifffile
import nist_lookup.xraydb_plugin as xdb


@click.command()
@click.argument(
    "folder",
    type=click.Path(exists=True, file_okay=False))
@click.option(
    "--height_map_left",
    type=click.Path(exists=True))
@click.option(
    "--height_map_right",
    type=click.Path(exists=True))
@click.argument(
    "output",
    type=click.Path())
def main(folder, height_map_left, height_map_right, output):
    input_files = sorted(glob(
        os.path.join(folder, "*.tif")))
    thickness = tifffile.imread(height_map_right) - tifffile.imread(height_map_left)
    darks = input_files[1:30]
    flats = input_files[30:130]
    first_projection = input_files[130]
    print(darks[0], darks[-1])
    dark = np.median(np.dstack(
        tifffile.imread(filename)
        for filename in darks), axis=-1)
    print(dark.shape)
    print(flats[0], flats[-1])
    print(first_projection)
    flat = np.median(np.dstack(
        tifffile.imread(filename)
        for filename in flats), axis=-1)
    first_projection = tifffile.imread(first_projection)
    print(flat.shape)
    print(first_projection.shape)
    a = (first_projection - dark) / (flat - dark)
    t = 3400
    d = 0.18
    pixel_size = 0.65e-6
    mu = -np.log(a[:, :thickness.shape[1]]) / (t * d * pixel_size)
    np.save(output, mu)
    _, _, atlen = xdb.xray_delta_beta("CH12", 2, 10e3)
    mu_theory = 1 / (atlen * 1e-2)
    print(np.median(mu), np.std(mu))
    print(mu_theory)




if __name__ == "__main__":
    main()
