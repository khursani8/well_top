import pandas as pd
import numpy as np
from tqdm import tqdm

from fastai.tabular import *
from fastai.basic_data import * 
from fastai.metrics import accuracy

def binary_facies_geoscience(df, gr_cutoff=120):
    """
    Given df input w/ TVDSS index and has column 'GR',
    calculates sand/shale 
    Returns a pandas srs.
    """
    srs = df['GR'].copy()
    srs[df['GR'] > gr_cutoff] = 'Shale'
    srs[df['GR'] <= gr_cutoff] = 'Sand'
    srs[df['GR'].isnull()] = np.nan
    return srs
    
def binary_facies_datascience(df, model='strat_model'):
    """
    Given df input w/ TVDSS index and standardized column names,
    pass the data through a trained classifier to predict sand/shale.
    Returns a pandas srs of predicted 'sand'/'shale'.
    """
    # Not too sure on the loading part so we're running through all these steps instead
    ground_truths = pd.read_csv('../data/stratified_train.csv', index_col=0)
    all_features = ground_truths.columns.tolist()
    
    dep_var = 'lith'
    cat_names = ['well']
    cont_names = ['DENS', 'DTS', 'GR', 'PEF', 'RESD', 'RESM', 'RESS', 'NEUT', 'SP']
    procs = [FillMissing, Categorify, Normalize]
    test = TabularList.from_df(df, path='.', cat_names=cat_names, cont_names=cont_names)
    data = (TabularList.from_df(ground_truths, path='.', cat_names=cat_names, cont_names=cont_names, procs=procs)
                           .random_split_by_pct()
                           .label_from_df(cols=dep_var)
                           .add_test(test)
                           .databunch())
    learn = tabular_learner(data, layers=[200,100], metrics=[accuracy])
    learn.load(model)
    
    # Define classes
    classes = ground_truths['lith'].unique().tolist()
    
    # Generate predictions
    softmax, _ = learn.get_preds(ds_type=DatasetType.Test)
    
    # Make sure to calculate labels from softmax directly!
    # TODO: Check argmin or argmax!
    preds = np.argmin(softmax, axis=1)
    srs = pd.Series(data=[classes[i] for i in preds], index=df.index)
    
    # Example code:
#     stratified_data = pandas.read_csv('../data/stratified_train.csv')
#     preds = binary_facies_datascience(stratified_data)

#     from sklearn.metrics import f1_score, accuracy_score
#     from sklearn.preprocessing import OrdinalEncoder

#     oe = OrdinalEncoder()
#     y_true = oe.fit_transform(stratified_data['lith'].values.reshape(-1, 1))
#     y_pred = oe.transform(preds.values.reshape(-1, 1))

#     f1_score(y_true, y_pred) 
    return srs

def multiclass_sands_geoscience(df, sand_shale_srs):
    """
    Given df input w/ TVDSS index and standardized column names,
    and a pandas srs w/ same index that specifies 'sand'/'shale',
    associates the sands w/ facies types.
    Returns a pandas srs of predicted facies.
    """
    facies = []
    for i in tqdm(range(len(df))):
        facies.append(auto_detect_facies(gamma_ray=df['GR'].iloc[i], density=df['DENS'].iloc[i], acoustic=df['DTC'].iloc[i], PE=df['PEF'].iloc[i]))
    
    srs = pd.Series(index=df.index, data=facies)
    srs[sand_shale_srs != 'Sand'] = np.nan # filters Shale and also other messages that might arise
    return srs

def multiclass_sands_datascience():
    """
    Given df input w/ TVDSS index and standardized column names,
    and a pandas srs w/ same index that specifies 'sand'/'shale',
    uses a trained classifier to predict facies types of sands.
    Returns a pandas srs of predicted facies.
    """
    
    pass

def pipeline(df):
    # Somehow get the file imported
    
    # Generate the ground truth values
    df['true_lith'] = binary_facies_geoscience(data, gr_cutoff=90)

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