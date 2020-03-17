import pandas as pd
import numpy as np
from skimage import io
import os
from scipy import ndimage
from skimage.color import rgb2hsv


def rgb_and_hsv(df):
    rgb_imgs = list()
    hsv_imgs = list()
    for url in df['image_link']: 
        print('1')
        p = io.imread(url)
        rgb_imgs.append(p)
        if len(p.shape) != 3:
            hsv_imgs.append(np.NaN)
            continue
        hsv_img = rgb2hsv(p)
        hsv_imgs.append(hsv_img)
    df['rgb'] = rgb_imgs
    df['hsv'] = hsv_imgs
    return df

def hsv_features(df):
    mean_hues = list()
    var_hues = list()
    mean_values = list()
    var_values = list()
    mean_sats = list()
    var_sats = list()
    edge_scores = list()
    row_var_scores = list()
    col_var_scores = list()
    sqvar_scores = list()
    
    for hsv_img in df.hsv:
        print('2')
        if type(hsv_img) == float:
            mean_hues.append(np.NaN)
            var_hues.append(np.NaN)
            mean_values.append(np.NaN)
            var_values.append(np.NaN)
            mean_sats.append(np.NaN)
            var_sats.append(np.NaN)
            edge_scores.append(np.NaN)
            row_var_scores.append(np.NaN)
            col_var_scores.append(np.NaN)
            sqvar_scores.append(np.NaN)
            continue
        
        hue_img = hsv_img[:, :, 0]
        mean_hue = np.mean(hue_img, axis=(0,1))
        var_hue = np.var(hue_img, axis=(0,1))
        mean_hues.append(mean_hue)
        var_hues.append(var_hue)
        
        value_img = hsv_img[:, :, 2]
        mean_value = np.mean(value_img, axis=(0,1))
        var_value = np.var(value_img, axis=(0,1))
        mean_values.append(mean_value) 
        var_values.append(var_value)
        
        sat_img = hsv_img[:, :, 1]
        mean_sat = np.mean(sat_img, axis=(0,1))
        var_sat = np.var(sat_img, axis=(0,1))
        mean_sats.append(mean_sat)
        var_sats.append(var_sat)
        
        sobel_x = ndimage.sobel(value_img, axis=0, mode='constant')
        sobel_y = ndimage.sobel(value_img, axis=1, mode='constant')
        edge_image = np.hypot(sobel_x, sobel_y)
        edge_score = np.sum(edge_image)
        edge_scores.append(edge_score)
    
        if len(hsv_img) == 2:
            row_var_scores.append(np.NaN)
            col_var_scores.append(np.NaN)
            sqvar_scores.append(np.NaN)
        else:
            row_vars = list()
            for row in value_img:
                var = np.var(row)
                row_vars.append(var)
            row_var_scores.append(np.mean(row_vars))
            
            col_vars = list()
            for j in range(len(value_img[0])):
                col = [value_img[i][j] for i in range(len(value_img))]
                col_vars.append(np.var(col))
            col_var_scores.append(np.mean(col_vars))
            
            sqvars = list()
            for j in range(len(value_img)-2):
                for i in range(len(value_img[j])-2):
                    square = list()
                    for q in range(2):
                        for r in range(2):
                            pix = value_img[j+r][i+q]
                            square.append(pix)
                    var = np.var(square)
                    sqvars.append(var)
            sqvar_scores.append(np.mean(sqvars))
            
    df['mean_hue'] = mean_hues
    df['var_hue'] = var_hues
    df['mean_value'] = mean_values
    df['var_value'] = var_values
    df['mean_saturation'] = mean_sats
    df['var_sats'] = var_sats
    df['edge_score'] = edge_scores
    df['row_variance_score'] = row_var_scores
    df['col_variance_score'] = col_var_scores
    # Read report for info on square variance -- not same as variance^2
    df['square_variance_score'] = sqvar_scores
    
    return df

def color_scored(df):
    n_colors = list()
    for i in df.rgb:
        print('3')
        if type(i) == float or len(i.shape) == 2:
            n_colors.append(np.NaN)
            continue            
        colors = list()
        for row in i:
            for c in row:
                colors.append(c)
        colors = pd.Series(colors).apply(lambda a: list(a))
        n = len(np.unique(colors))
        n_colors.append(n)
    df['color_score'] = n_colors
    
    return df

#----------------------------------------------------------------------------

def generate_features(indir=None, outdir=None):
    
    # Read in data
    if not indir:
        print('No directory')
        return
    filename = os.path.join(indir, 'paintings.csv')
    paintings = pd.read_csv(filename, index_col=0)
    
    # Transform into pixel arrays
    paintings = rgb_and_hsv(paintings)
    
    print('ONE THIRD')
    
    # Generate HSV features
    paintings = hsv_features(paintings)
    
    print('TWO THIRDS')
    # Generate color score
    paintings = color_scored(paintings)
    
    # Export image and feature dfs
    images = paintings[['id', 'rgb', 'hsv']]
    feats = paintings.drop(['rgb', 'hsv'], axis=1)
    if outdir:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        filename = os.path.join(outdir, 'images.csv')
        images.to_csv(filename)
        filename = os.path.join(outdir, 'painting_features.csv')
        feats.to_csv(filename)
        
        
    
    
    
    
    
    
    