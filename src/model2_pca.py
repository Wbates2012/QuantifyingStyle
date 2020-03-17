import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
import os
import json

def linreg_pca(X, y, components=2):
    
    # Limit dimensions
    pca = PCA(n_components=components)
    pca_result = pca.fit_transform(X)
    newX = list()
    for j in range(len(y)):
        row = list()
        for i in range(components):
            row.append(pca_result[:,i][j])
        newX.append(row)
    
    return pd.DataFrame(newX, columns=['pca'+str(i) for i in range(components)])
    # Linear Regression
    results = regress(newX, y)
    return results

def regress(X, y):
    
    results = dict()
    reg = LinearRegression()
    reg.fit(X, y)
    
    results['R-Squared'] = reg.score(X,y)
    results['Coefficient'] = reg.coef_[0]
    results['Intercept'] = reg.intercept_
    
    return results

#---------------------------------------------------------------------------

def driver(indir=None, outdir=None):
    
    # Read in processed data
    if not indir:
        print('No directory')
        return
    filename = os.path.join(indir, 'painting_features.csv')
    painting_feats = pd.read_csv(filename, index_col=0)
    painting_feats = painting_feats.dropna()
    
    X1 = painting_feats[['mean_hue', 'mean_value', 'mean_saturation', 'resolution', 'edge_score']]
    X2 = painting_feats.drop(['start_date', 'end_date', 'id', 'image_link', 'category', 'title'], axis=1)
    y = painting_feats['start_date']
    
    basic_results = linreg_pca(X1, y)
    adv_results = linreg_pca(X2, y, 2)
    
    adv_results['image_link'] = painting_feats['image_link']
    adv_results['id'] = painting_feats['id']
    
    if outdir:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        filename = os.path.join(outdir, 'model2_features.csv')
        adv_results.to_csv(filename)
    return
    # Export results
    if outdir:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        filename = os.path.join(outdir, 'basic_pca_linreg.json')
        with open(filename, 'w') as f:
            json.dump(basic_results, f)
        filename = os.path.join(outdir, 'adv_pca_linreg.json')
        with open(filename, 'w') as f:
            json.dump(adv_results, f)
    
    
    
    
    
    