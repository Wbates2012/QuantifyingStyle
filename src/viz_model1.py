import numpy as np
import pandas as pd
from PIL import Image
import os
import urllib

def visualize(indir=None, outdir=None):
    
    # Read in processed data
    if not indir:
        print('No directory')
        return
    filename = os.path.join(indir, 'model1_features.csv')
    painting_feats = pd.read_csv(filename, index_col=0)
    painting_feats = painting_feats.dropna()
    painting_feats = painting_feats.reset_index(drop=True)
    
    viz_feats = painting_feats[['id', 'start_date', 'adv_complexity', 'image_link']]
    
    GLOBAL_WIDTH = 75000
    GLOBAL_HEIGHT = 800
    bg_color = (222, 222, 222) # gray, you can choose your own
    
    
    x = [int(GLOBAL_WIDTH*(viz_feats.start_date[i]-np.min(viz_feats.start_date))/np.max(viz_feats.start_date))+100 for i in range(len(viz_feats))]
    y = [int(GLOBAL_HEIGHT*(viz_feats.adv_complexity[i]-np.min(viz_feats.adv_complexity))/np.max(viz_feats.adv_complexity))-100 for i in range(len(viz_feats))]
    y = [-i+np.max(y)+200 for i in y]
    
    coords = [(x[i], y[i]) for i in range(len(viz_feats))]
    
    figure = Image.new('RGB', (np.max(x)+50, np.max(y)+50), bg_color)
    
    if outdir:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        picdir = os.path.join(outdir, 'thumbnails')
        if not os.path.exists(picdir):
            os.makedirs(picdir)
    
    size = 64, 64
    for i in range(len(viz_feats.image_link)):
        link = viz_feats['image_link'][i]
        name = str(viz_feats['id'][i]) + '.jpg'
        url = 'viz/model1/thumbnails'
        out = os.path.join(url, name)
        urllib.request.urlretrieve(link, out)
        
        piece = Image.open(out)
        piece.thumbnail(size)
        figure.paste(piece, coords[i])
        
    filename = os.path.join(outdir, 'plot1.jpg')
    figure.save(filename)
    return

    
    