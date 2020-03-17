import pandas as pd
import ast
import numpy as np
from skimage import io
import re
import os

def remove_nans(df):
    for col in list(df.columns):
        df[col] = [np.NaN if i=='Unavailable' else i for i in df[col]]
    df = df.dropna()
    return df.reset_index(drop=True)

def remove_parens(df):
    pat = '\(.*\)'
    dts = list()
    for s in df.date:
        if len(re.findall(pat, s)) == 0:
            dts.append(s)
        else:
            dts.append(s.replace(re.findall(pat, s)[0], ' '))
    df['date'] = dts
    return df

def extract_date_range(df):
    start = list()
    end = list()
    for s in df.date:
        l = re.findall('[0-9]{4}', s)
        if len(l) == 1:
            start.append(int(l[0]))
            end.append(int(l[0]))
        else:
            start.append(int(l[0]))
            end.append(int(l[1]))
    df['start_date'] = start
    df['end_date'] = end
    return df.drop(['date'], axis=1)

def clean_category(df):
    df.category = ['painting' if 'painting' in i else i for i in df.category]
    df.category = ['drawing' if 'sketch' in i else i for i in df.category]
    return df

def extract_resolution(df):
    resos = list()
    for image in df['image_link']:
        arr = io.imread(image)
        res = arr.shape[0]*arr.shape[1]
        resos.append(res)
    df['resolution'] = resos
    return df

def high_res(df):
    thres = df.resolution.mean() - 2*df.resolution.std()
    return df[df.resolution > thres]

#----------------------------------------------------------------------------

def clean_data(indir=None, outdir=None):
    
    # Read in raw data
    if not indir:
        print('No directory')
        return
    dfl = list()
    filename = os.path.join(indir, 'paintings.txt')
    for l in open(filename):
        row = l[:-1]
        dfl.append(ast.literal_eval(row))
    paintings = pd.DataFrame(dfl)
    
    # Clean data
    paintings = remove_nans(paintings)
    paintings = remove_parens(paintings)
    paintings = paintings.drop_duplicates(subset='id')
    paintings = clean_category(paintings)
    
    # Extract basic features
    paintings = extract_date_range(paintings)
    paintings = extract_resolution(paintings)
    
    # Limit to paintings with high-enough resolution
    paintings = paintings[paintings.category == 'painting']
    paintings = high_res(paintings)
        
    paintings = paintings.reset_index(drop=True)
    
    # Write cleaned data
    if outdir:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        filename = os.path.join(outdir, 'paintings.csv')
        paintings.to_csv(filename)
        