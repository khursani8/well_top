import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from sklearn.preprocessing import LabelEncoder

__all__ = ['discrete_cmap','plotter'] 


def discrete_cmap(N, base_cmap=None):
    """Extract discrete colors from cmap"""
    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)


def plotter(data, depth_col, num_col=None, cat_col=None, cat_classes=None, figsize=(8, 12), base_cmap='hsv'):
    """
    Plot log data.
    
    Parameters
    ----------
        data : pandas dataframe
            Well log data in pandas dataframe. Depth column is required.
        depth_col : single value integer in list
            Column index of depth in data.
        num_col : single or multiple integers in list
            Numeric log indices in data. Eg, GR, Resistivity, etc. Skip if do not
            intend to plot numeric data.
        cat_col : single or multiple integers in list
            Categorical log indices in data. Eg, Facies, Formation, etc. Skip if do not
            intend to plot numeric data.
        cat_classes : list of strings/discrete entity in list
            List of all classes according to cat_col order. Eg, if cat_col = [0, 1]
            referring to Facies and Formation respectively, where both have 2 and 3
            classes respectively:
                >> cat_classes = [['SS','SH'], ['Seligi','Raya','Serudon']]
        figsize : tuple
            Graph object figure size in tuple of (row, column) size in inches.
        base_cmap : matplotlib cmap string
            Colormap for categorical data.
          
    Return
    ------
        No return. Only will prompt matplotlib.pyplot graph object.
    """
    
    # set up plt chart
    num_C = len(num_col) if not num_col is None else 0
    cat_C = len(cat_col) if not cat_col is None else 0
    C = num_C + cat_C
    fig, ax = plt.subplots(nrows=1, ncols=C, figsize=figsize)
    
    # depth
    depth_header = data.columns[depth_col].tolist()
    data = data.sort_values(by=depth_header)
    depth_data = data[depth_header].values
    depth_trim = max(depth_data), min(depth_data)
    
    # numeric data
    if not num_col is None:
        num_header = data.iloc[:, num_col].columns.tolist()
        num_data = data.iloc[:, num_col].values
        for i in range(num_C):
            ax[i].plot(num_data[:, i], depth_data)
            ax[i].set_xlabel(num_header[i])
            ax[i].invert_yaxis()
            ax[i].set_ylim(depth_trim)
        
    # categorical data
    if not cat_col is None:
        cat_header = data.iloc[:, cat_col].columns.tolist()
        cat_data = data.iloc[:, cat_col].values
        for i in range(cat_C):
            j = i + num_C
            x = cat_data[:, i]
            le = LabelEncoder()
            le.fit(cat_classes[i])
            class_encoded = le.transform(cat_classes[i])
            x_encoded = le.transform(x)
            n_unq = len(np.unique(x))
            raster_array = np.repeat(np.expand_dims(x_encoded, 1), 100, 1).astype(float)
            cm_val = discrete_cmap(N=len(cat_classes[i]), base_cmap=base_cmap)
            cm_vmin, cm_vmax = min(class_encoded), max(class_encoded)
            im = ax[j].imshow(X=raster_array, interpolation=None, aspect='auto', cmap=cm_val, vmin=cm_vmin, vmax=cm_vmax)
            divider = make_axes_locatable(ax[j])
            cax = divider.append_axes('right', size='20%', pad=0.05)
            cbar = plt.colorbar(im, cax=cax)
            cbar.ax.get_yaxis().set_ticks([])
            # future fix to have class labels at the side of colorbar
            #for k,lab in enumerate([str(s) for s in cat_classes[i]]):
            #    cbar.ax.text(0, (2*k+1)/8, lab, ha='left', va='center')
            ax[j].set_xticklabels([])
            ax[j].set_xlabel(cat_header[i])
            ax[j].grid()
        
    # keep only first yaxis
    for i in range(len(num_col)+len(cat_col)-1):
        ax[i+1].set_yticklabels([])
    
    plt.show()
    
import numpy as np


def auto_detect_facies_2(density, acoustic, PE, normalized=True):
    
    # normalizer
    def normalizer(x, xmin, xmax, scale='cart'):
        # layer for logscale
        if scale == 'log':
            x, xmin, xmax = map(log10, [x, xmin, xmax])
        # normalization
        norm_val = (x - xmin) / (xmax - xmin)
        return norm_val
    
    if normalized:
        density = normalizer(density, 1.95, 2.95)
        acoustic = normalizer(acoustic, 40, 140)
        PE = normalizer(PE, 0, 10)
        coord1 = np.asarray([density, acoustic, PE])
        facies_dict = {
            'SS' : [normalizer(2.65, 1.95, 2.95), normalizer(53  , 40, 140), normalizer(1.81, 0, 10)],
            'LS' : [normalizer(2.71, 1.95, 2.95), normalizer(47.5, 40, 140), normalizer(5.08, 0, 10)],
        }
    else:
        coord1 = np.asarray([density, acoustic, PE])
        facies_dict = {
            'SS' : [2.65, 53  , 1.81],
            'LS' : [2.71, 47.5, 5.08],
        }
    
    # calculate distance
    dist = {}
    for key,val in facies_dict.items():
        coord2 = np.asarray(val)
        dist[key] = np.linalg.norm(coord1 - coord2)
        
    return min(dist, key=dist.get)