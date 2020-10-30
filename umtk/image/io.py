from pathlib import Path
from typing import Union
import SimpleITK
import numpy as np


def read_itk(
    file_path: Union[str, Path],
    read_header: bool = False,
    reorient: bool = False
):
    """ Read an image.

    Args:
        file_path (str or Path): itk image file path.
        read_header (bool): whether to return the dicom header
            together with the image array
        reorient (bool): whether to standardize image orientation
    Returns:
        (numpy.ndarray): loaded image array.
        (dict): dicom header dict containing 'spacing', 'orientation', 'origin'.
    """
    image_itk = SimpleITK.ReadImage(file_path)
    image = SimpleITK.GetArrayFromImage(image_itk)

    if reorient:
        directions = np.asarray(image_itk.GetDirection())
        image = np.flip(image, np.where(directions[[0, 4, 8]][::-1] < 0)[0])

    if read_header:
        if reorient:
            direction = np.array([1.0, 1.0, 1.0])
        else:
            d = image_itk.GetDirection()
            direction = np.round(np.array([d[8], d[4], d[0]]))
        header = {
            "spacing": np.asarray(image_itk.GetSpacing())[::-1],
            "direction": direction,
            "origin": np.asarray(image_itk.GetOrigin())[::-1],
        }
        return image, header
    else:
        return image