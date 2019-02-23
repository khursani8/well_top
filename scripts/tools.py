import pandas as pd
import numpy as np

def binary_facies_geoscience(df, gr_cutoff=90):
    """
    Given df input w/ TVDSS index and has column 'GR',
    calculates sand/shale 
    Returns a pandas srs.
    """
    srs = df['GR'].copy()
    srs[df['GR'] > gr_cutoff] = 'shale'
    srs[df['GR'] <= gr_cutoff] = 'sand'
    srs[df['GR'].isnan()] = np.nan
    return srs
    
def binary_facies_datascience(df):
    """
    Given df input w/ TVDSS index and standardized column names,
    pass the data through a trained classifier to predict sand/shale.
    Returns a pandas srs of predicted 'sand'/'shale'.
    """
    
    pass

def multiclass_sands_geoscience(df, sand_shale_srs):
    """
    Given df input w/ TVDSS index and standardized column names,
    and a pandas srs w/ same index that specifies 'sand'/'shale',
    associates the sands w/ facies types.
    Returns a pandas srs of predicted facies.
    """
    
    pass

def multiclass_sands_datascience():
    """
    Given df input w/ TVDSS index and standardized column names,
    and a pandas srs w/ same index that specifies 'sand'/'shale',
    uses a trained classifier to predict facies types of sands.
    Returns a pandas srs of predicted facies.
    """
    
    pass