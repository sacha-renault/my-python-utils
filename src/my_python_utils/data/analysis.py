from typing import Optional
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

@dataclass
class ArrayInfo:
    shape: tuple
    max: np.generic | npt.NDArray
    min: np.generic | npt.NDArray
    mean: np.generic | npt.NDArray
    var: np.generic | npt.NDArray

    def __format__(self, format_spec: str) -> str:
        if format_spec:
            return ("ArrayInfo("
                f"shape: {self.shape}, "
                f"max: {format(self.max, format_spec)}, "
                f"min: {format(self.min, format_spec)}, "
                f"mean: {format(self.mean, format_spec)}, "
                f"var: {format(self.var, format_spec)}"
                ")"
            )
        else:
            return repr(self)


def get_array_info(arr: npt.NDArray) -> None:
    # assert type
    if not isinstance(arr, np.ndarray):
        raise TypeError(f"arr was expecting {npt.NDArray}, got {type(arr)}")
    
    # get utils infos
    data_max = np.amax(arr)
    data_min = np.amin(arr)
    data_mean = np.mean(arr)
    data_var = np.var(arr)
    data_shape = np.shape(arr)

    # instanciate returned object 
    array_info = ArrayInfo(
        max = data_max,
        min = data_min,
        mean = data_mean,
        var = data_var,
        shape = data_shape)
    
    return array_info
    