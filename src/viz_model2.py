import pandas as pd
from PIL import Image
import os
import urllib

def visualize(indir=None, outdir=None):
    
    # Read in processed data
    if not indir:
        print('No directory')
        return
    filename = os.path.join(indir, 'model2_features.csv')
    painting_feats = pd.read_csv(filename, index_col=0)
    painting_feats = painting_feats.dropna()
    painting_feats = painting_feats.reset_index(drop=True)
    
    GLOBAL_WIDTH = 4000
    bg_color = (222, 222, 222)
    figure = Image.new('RGB', (GLOBAL_WIDTH, GLOBAL_WIDTH), bg_color)
    
    coords = [(int(100+painting_feats['pca0'][i]*.001)*20, (int(100+painting_feats['pca1'][i]*.001)*20)-400) for i in range(len(painting_feats))]
    
    if outdir:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        picdir = os.path.join(outdir, 'thumbnails')
        if not os.path.exists(picdir):
            os.makedirs(picdir)
    
    size = 64, 64
    for i in range(len(painting_feats.image_link)):
        link = painting_feats['image_link'][i]
        name = str(painting_feats['id'][i]) + '.jpg'
        out = os.path.join(picdir, name)
        urllib.request.urlretrieve(link, out)
        
        piece = Image.open(out)
        piece.thumbnail(size)
        figure.paste(piece, coords[i])
        
    filename = os.path.join(outdir, 'plot2.jpg')
    figure.save(filename)
    return
