import sys
import json
import shutil

sys.path.insert(0, 'src')
from clt import collect_data
from cln import clean_data
from fe import generate_features
import model1_complexity
import viz_model1
import model2_pca
import viz_model2

data_params = 'config/raw_params.json'
clean_params = 'config/clean_params.json'
feat_params = 'config/feat_params.json'
model1_params = 'config/model1_params.json'
model2_params = 'config/model2_params.json'
model1_viz_params = 'config/model1_viz_params.json'
model2_viz_params = 'config/model2_viz_params.json'

test_data_params = 'config/raw_test_params.json'
test_clean_params = 'config/clean_test_params.json'
test_feat_params = 'config/feat_test_params.json'
test_comp_params = 'config/model1_test_params.json'
test_pca_params = 'config/model2_test_params.json'
test_comp_viz_params = 'config/model1_test_viz_params.json'
test_pca_viz_params = 'config/model2_test_viz_params.json'

def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)
    return param

def main(targets):
    
    if 'erase' in targets:
        shutil.rmtree('data/raw', ignore_errors=True)
        shutil.rmtree('data/cleaned', ignore_errors=True)
        shutil.rmtree('data/feat', ignore_errors=True)
        shutil.rmtree('data/out', ignore_errors=True)
        
    if 'data' in targets:
        cfg = load_params(data_params)
        collect_data(**cfg)
        
    if 'clean' in targets:
        cfg = load_params(clean_params)
        clean_data(**cfg)
        
    if 'features' in targets:
        cfg = load_params(feat_params)
        generate_features(**cfg)
        
    if 'complexity' in targets:
        cfg = load_params(model1_params)
        model1_complexity.driver(**cfg)
        
    if 'model1viz' in targets:
        cfg = load_params(model1_viz_params)
        viz_model1.visualize(**cfg)
        
    if 'pca' in targets:
        cfg = load_params(model2_params)
        model2_pca.driver(**cfg)
        
    if 'model2viz' in targets:
        cfg = load_params(model2_viz_params)
        viz_model2.visualize(**cfg)    
        
    if 'test-project' in targets:
        cfg = load_params(test_data_params)
        collect_data(**cfg)
        
        cfg = load_params(test_clean_params)
        clean_data(**cfg)
        
        cfg = load_params(test_feat_params)
        generate_features(**cfg)
        
        cfg = load_params(test_comp_params)
        model1_complexity.driver(**cfg)
        
        cfg = load_params(test_comp_viz_params)
        viz_model1.visualize(**cfg)
        
        cfg = load_params(test_pca_params)
        model2_pca.driver(**cfg)     
        
        cfg = load_params(test_pca_viz_params)
        viz_model2.visualize(**cfg)
    
    return

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
    
    
    
    
