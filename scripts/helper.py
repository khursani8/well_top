import numpy as np

def auto_detect_facies(gamma_ray, density, acoustic, PE):
    """
    Simple euclidean nearest neighbour to auto detect facies given logs.

    Parameters
    ----------
    gamma_ray: float
        Gamma ray response.
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
    coord = np.asarray([gamma_ray, density, acoustic, PE])
    
    if np.isnan(coord).sum() != 0:
        return 'NO FACIES'

    # facies dictionary
    facies_dict = {
      'SS' : [80, 2.65, 53, 1.81],
      'LS' : [80, 2.71, 47.5, 5.08],
      'SH' : [100, 2.5, 100, 3],
      'DL' : [80, 2.87, 43, 3.14],
      'AN' : [80, 2.98, 50, 5.06],
      'SL' : [90, 2.03, 67, 4.65],
    }

    distances = {}
    # calculate distance
    for facies in facies_dict:
        facies_coord = np.asarray(facies_dict[facies])
        distances[facies] = np.linalg.norm(coord - facies_coord)

    # return the facies
    return min(distances, key=distances.get)