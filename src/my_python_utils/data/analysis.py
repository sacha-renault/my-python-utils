from typing import Optional

import numpy as np
import numpy.typing as npt

def print_data_info(arr: npt.NDArray, *, axis: Optional[int] = None) -> None:
    # assert type
    if not isinstance(arr, np.ndarray):
        raise TypeError(f"arr was expecting {npt.NDArray}, got {type(arr)}")
    
    # get utils infos
    data_max = np.amax(arr, axis = axis)
    data_min = np.amin(arr, axis = axis)
    data_mean = np.mean(arr, axis = axis)
    data_var = np.var(arr, axis = axis)
    data_shape = np.shape(arr)

    # display 
    print("======= ARRAY INFO =======")
    print(f"shape : {data_shape}")
    print(f"  max : {data_max}")
    print(f"  min : {data_min}")
    print(f" mean : {data_mean}")
    print(f"  var : {data_var}")