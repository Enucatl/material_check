import click
import os
import numpy as np
from glob import glob
from tqdm import tqdm
import tifffile


@click.command()
@click.argument(
    "folder",
    type=click.Path(exists=True, file_okay=False))
def main(folder):
    input_files = sorted(glob(
        os.path.join(folder, "*.tif")))
    darks = input_files[1:30]
    flats = input_files[30:130]
    first_projection = input_files[130]
    print(darks[0], darks[-1])
    print(flats[0], flats[-1])
    print(first_projection)
    dark_array = np.dstack(
        tifffile.imread(filename)
        for filename in darks)
    flat_array = np.dstack(
        tifffile.imread(filename)
        for filename in flats)
    first_projection = tifffile.imread(first_projection)
    print(dark_array.shape)
    print(flat_array.shape)
    print(first_projection.shape)


if __name__ == "__main__":
    main()
