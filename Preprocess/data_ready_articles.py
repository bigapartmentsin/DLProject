# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os
import re
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--inp_dr', default="/scratch/eff254/DL/project/data/gigaword_eng_5/data", type=str, help="Data Directory")
parser.add_argument('--out_dr', default="/scratch/eff254/DL/project/data/gigaword_eng_5_decompressed", type=str, help="Directory for out data")
parser.add_argument('--source', default="apw_eng", type=str, help="One of ['cna_eng', 'wpb_eng', 'afp_eng', 'xin_eng', 'apw_eng', 'ltw_eng', 'nyt_eng']")
parser.add_argument('--is_toy', action='store_true', help="Whether to export all data (FALSE) or a toy example (TRUE)")
parser.add_argument('--size_toy', default=1000, type=int, help="Size of the toy example")
parser.add_argument('--do_bpe', action='store_true', help="Learn and apply BPE to the articles?")

args = parser.parse_args()
print(args)

def getFilesIDs(complete_dir):
    
    files = os.listdir(complete_dir)
    files = [x.split(".")[0] for x in files]
    files = list(set(files))
    
    return files

def importSingle(complete_filename, is_pickle = True): 
    
    if is_pickle:
        complete_filename = complete_filename + ".p"
        with open(complete_filename, 'rb') as f:
            file_content = pickle.load(f)        
        
    else:
        with open(complete_filename, 'r') as f:
            file_content = f.readlines()

    return file_content

def importByTerm(complete_dir, term, is_pickle = True): 
    
    possible_terms = ['hls', 'ids', 'tps', 'txt']
    if term not in possible_terms:
        raise ValueError("Termination or type of file not found. Accepted values: \n {}".format(possible_terms))
    
    files = getFilesIDs(complete_dir)
    
    list_files = []
    for file in files: 
        single = importSingle(complete_dir + "/" +  file + "." + term)
        list_files.extend(single)
        
    return list_files

def consistencyChecker(obj): 
    
    for i in range(0, len(obj)-1):
        
        if len(obj[i]) != len(obj[i+1]):
            
            raise AttributeError("Length of your lists are not the same")

def importBySource(inp_dir_, source_): 
    
    complete_dir = inp_dir_ + "/" + source_
    
    # Carefull here, order matters
    possible_terms = ['ids', 'txt', 'tps', 'hls']
    l1 = importByTerm(complete_dir, possible_terms[0], source_)
    l2 = importByTerm(complete_dir, possible_terms[1], source_)
    l3 = importByTerm(complete_dir, possible_terms[2], source_)
    l4 = importByTerm(complete_dir, possible_terms[3], source_)
    
    consistencyChecker([l1, l2, l3, l4])
    return l1, l2, l3, l4

def generalCleaner(id_list_, txt_list_, tps_list_, hls_list_):
    
    id_list_ = [id_list_[i] for i in range(0,len(id_list_)) if hls_list_[i]!='']
    txt_list_ = [txt_list_[i] for i in range(0,len(txt_list_)) if hls_list_[i]!='']
    tps_list_ = [tps_list_[i] for i in range(0,len(tps_list_)) if hls_list_[i]!='']
    hls_list_ = [hls_list_[i] for i in range(0,len(hls_list_)) if hls_list_[i]!='']
    
    id_list_ = [id_list_[i] for i in range(0,len(id_list_)) if tps_list_[i]=='story']
    hls_list_ = [hls_list_[i] for i in range(0,len(hls_list_)) if tps_list_[i]=='story']
    txt_list_ = [txt_list_[i] for i in range(0,len(txt_list_)) if tps_list_[i]=='story']
    tps_list_ = [tps_list_[i] for i in range(0,len(tps_list_)) if tps_list_[i]=='story']
    
    # Just to be sure
    consistencyChecker([tps_list_, txt_list_, hls_list_, id_list_])
    
    return id_list_, txt_list_, tps_list_, hls_list_

def toySubsetter(id_list_, txt_list_, tps_list_, hls_list_, n_pairs_):
    
    indexes_ = np.random.choice(len(id_list_), n_pairs_)  
    
    id_list_ = [id_list_[x] for x in indexes_]
    txt_list_ = [txt_list_[x] for x in indexes_]
    tps_list_ = [tps_list_[x] for x in indexes_]
    hls_list_ = [hls_list_[x] for x in indexes_]
    
    return(id_list_, txt_list_, tps_list_, hls_list_)


if __name__ == "__main__":

	current_ids, current_txt, current_tps, current_hls = importBySource(args.inp_dr, args.source)
    print("Original Length: {}".format(len(current_ids)))
    print("----")
    current_ids, current_txt, current_tps, current_hls = generalCleaner(current_ids, current_txt, current_tps, current_hls)
    print("Final Lenth: {}".format(len(current_ids)))

    if(args.is_toy == True):
    	current_ids, current_txt, current_tps, current_hls = toySubsetter(current_ids, current_txt, current_tps, current_hls, n_pairs_=args.size_toy)



