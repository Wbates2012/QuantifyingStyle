import pandas as pd
import numpy as np
import json
import os
from sklearn.linear_model import LinearRegression

def get_complexity(df):
    
    # Normalize
    norm_edge_score = df.edge_score.apply(lambda x: x/np.max(df.edge_score))
    norm_color_score = df.color_score.apply(lambda x: x/np.max(df.color_score))
    norm_row_var_score = df.row_variance_score.apply(lambda x: x/np.max(df.row_variance_score))
    
    # Create complexity score
    complexity = (norm_edge_score + norm_color_score + norm_row_var_score)/3
    return complexity

def get_advanced_complexity(df):
    
    # Normalize
    norm_edge_score = df.edge_score.apply(lambda x: x/np.max(df.edge_score))
    norm_color_score = df.color_score.apply(lambda x: x/np.max(df.color_score))
    norm_row_var_score = df.row_variance_score.apply(lambda x: x/np.max(df.row_variance_score))
    norm_col_var_score = df.col_variance_score.apply(lambda x: x/np.max(df.col_variance_score))
    norm_sqr_var_score = df.square_variance_score.apply(lambda x: x/np.max(df.square_variance_score))
    
    # Average variance scores
    overall_var_score = (norm_row_var_score+norm_col_var_score+norm_sqr_var_score)/3
    overall_var_score = overall_var_score.apply(lambda x: x/np.max(overall_var_score))

    # Create advanced complexity score
    adv_complexity = (norm_edge_score + norm_color_score + overall_var_score)/3
    #adv_complexity = adv_complexity.apply(lambda x: x/np.max(adv_complexity))
    return adv_complexity



#----------------------------------------------------------------------

def driver(indir=None, outdir=None):
    
    # Read in processed data
    if not indir:
        print('No directory')
        return
    filename = os.path.join(indir, 'painting_features.csv')
    painting_feats = pd.read_csv(filename, index_col=0)
    painting_feats = painting_feats.dropna()
    
    # Obtain inputs
    painting_feats['complexity'] = get_complexity(painting_feats).values.reshape(-1,1)
    painting_feats['adv_complexity'] = get_advanced_complexity(painting_feats).values.reshape(-1,1)
    #y = painting_feats.start_date
    
    # Model
    #basic_results = regress(X1, y)
    #adv_results = regress(X2, y)
    
    # Export results
    if outdir:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        filename = os.path.join(outdir, 'model1_features.csv')
        painting_feats.to_csv(filename)
        return
        filename = os.path.join(outdir, 'basic_complexity_linreg.json')
        with open(filename, 'w') as f:
            json.dump(basic_results, f)
        filename = os.path.join(outdir, 'adv_complexity_linreg.json')
        with open(filename, 'w') as f:
            json.dump(adv_results, f)
    
    
    