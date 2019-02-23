import numpy as np

def auto_detect_facies(density, acoustic, PE):
    """
    Simple euclidean nearest neighbour to auto detect facies given logs.

    Parameters
    ----------

    density : float
      Density log response.
    acoustic : float
      Acoustic log response.
    PE : float
      PE log response.

    Return
    ------
    detected_facies : {'SS','LS','SH','DL','AN','SL'}

    """
  
    # wrap into coordinate
    coord = np.asarray([density, acoustic, PE])
    
    if np.isnan(coord).sum() != 0:
        return np.nan

    # facies dictionary
    facies_dict = {
      'SS' : [2.65, 53, 1.81],
      'LS' : [2.71, 47.5, 5.08],
      'SH' : [2.5, 100, 3],
      'DL' : [2.87, 43, 3.14],
      'AN' : [2.98, 50, 5.06],
      'SL' : [2.03, 67, 4.65],
    }

    distances = {}
    # calculate distance
    for facies in facies_dict:
        facies_coord = np.asarray(facies_dict[facies])
        distances[facies] = np.linalg.norm(coord - facies_coord)

    # return the facies
    return min(distances, key=distances.get)