import numpy as np

def to_list(vec):
    """Convert any vector format to Python list"""
    if vec is None:
        return []
    if isinstance(vec, np.ndarray):
        return vec.tolist()
    if isinstance(vec, list):
        return vec
    try:
        return list(vec)
    except:
        return []
