# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os
import re
import pickle
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--inp_dr', default="/scratch/eff254/DL/project/data/gigaword_eng_5/data", type=str, help="Data Directory")
parser.add_argument('--out_dr', default="/scratch/eff254/DL/project/data/gigaword_eng_5_decompressed", type=str, help="Directory for out data")
parser.add_argument('--eval_dr', default="/scratch/eff254/DL/project/DLProject/Preprocess", type=str, help="Directory where tokenizer/normalizarion/BPE pearl script lives")
parser.add_argument('--source', default="apw_eng", type=str, help="One of ['cna_eng', 'wpb_eng', 'afp_eng', 'xin_eng', 'apw_eng', 'ltw_eng', 'nyt_eng']")
parser.add_argument('--do_tok', action='store_false', help="Apply normalization and tokenization to articles? (Default = True)")
parser.add_argument('--do_bpe', action='store_false', help="Learn and apply BPE to the articles? (Default = True)")
parser.add_argument('--per_train', default=70, type=int, help="Percentage in train set")
parser.add_argument('--per_valid', default=15, type=int, help="Percentage in validation set")
args = parser.parse_args()
print(args)

####### FUNCTIONS TO READ ####### 

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

    '''NOT USED'''
    
    indexes_ = np.random.choice(len(id_list_), n_pairs_)  
    
    id_list_ = [id_list_[x] for x in indexes_]
    txt_list_ = [txt_list_[x] for x in indexes_]
    tps_list_ = [tps_list_[x] for x in indexes_]
    hls_list_ = [hls_list_[x] for x in indexes_]
    
    return(id_list_, txt_list_, tps_list_, hls_list_)

####### FUNCTIONS TO NORMALIZE/TOKENIZE ####### 

def writeLinesO(list_, file_name_, dir_):
    
    outF = open(dir_ + "/" + file_name_, "w")
    for line in list_:
        outF.write(line)
        outF.write("\n")
    outF.close()
    
def readLinesO(file_name_, dir_):
    
    with open(dir_ + "/" + file_name_, "r") as inpF:
        content = inpF.readlines()
    
    return(content)

def runNorm(inp_list_, eval_dir_ = eval_dir, tempfile_name_ = "temp.txt"): 
    
    ''' Assumes the normalize-punctuation.perl is in eval_dir_'''
    
    writeLinesO(inp_list_, tempfile_name_, eval_dir_)
    
    # perl "$code_dir"/normalize-punctuation.perl -l "en" < "$data_dir"/tst2010.en > "$data_dir"/tst2010.en.norm
    cmd_ = "perl %s -l 'en' < %s > %s" % (eval_dir_ + "/normalize-punctuation.perl", \
                                         eval_dir_ + "/" + tempfile_name_, \
                                         eval_dir_ + "/" + tempfile_name_ + ".norm",)
    
    print("Runnig perl normalization script...")
    subprocess.call(cmd_, shell=True)
    
    normalized = readLinesO(tempfile_name_ + ".norm", eval_dir_)
    
    os.remove(eval_dir_ + "/" + tempfile_name_ + ".norm")
    os.remove(eval_dir_ + "/" + tempfile_name_)    
    
    return normalized

def runTok(inp_list_, eval_dir_ = eval_dir, tempfile_name_ = "temp.txt"): 
    
    ''' Assumes the tokenizer_apos.perl is in eval_dir_'''
    
    writeLinesO(inp_list_, tempfile_name_, eval_dir_)
    
    # perl "$code_dir"/tokenizer_apos.perl -threads 5 -l "en" < "$data_dir"/tst2010.en.norm > "$data_dir"/tst2010.en.tok 
    cmd_ = "perl %s -threads 5 -l 'en' < %s > %s" % (eval_dir_ + "/tokenizer_apos.perl", \
                                         eval_dir_ + "/" + tempfile_name_, \
                                         eval_dir_ + "/" + tempfile_name_ + ".tok",)
    
    print("Runnig perl tokenization script...")
    subprocess.call(cmd_, shell=True)
    
    tokenized = readLinesO(tempfile_name_ + ".tok", eval_dir_)
    
    os.remove(eval_dir_ + "/" + tempfile_name_ + ".tok")
    os.remove(eval_dir_ + "/" + tempfile_name_)
    
    return tokenized

####### FUNCTIONS TO SPLIT / BPE ####### 


def validSplitter(id_list_, txt_list_, hls_list_,
                  per_train, per_valid, random_seed):
    
    if per_train < 0: 
        raise ValueError('per_train out of bound: Selected {} but need a number between 0 and 100'.format(per_train))
     
    if per_train > 100: 
        raise ValueError('per_train out of bound: Selected {} but need a number between 0 and 100'.format(per_train))
        
    if per_valid < 0: 
        raise ValueError('per_valid out of bound: Selected {} but need a number between 0 and 100'.format(per_valid))
        
    if per_valid  > 100: 
        raise ValueError('per_valid out of bound: Selected {} but need a number between 0 and 100'.format(per_valid))
        
    if per_train + per_valid > 100: 
        raise ValueError('per_valid and per_train add more than 100.')
        
    np.random.seed(random_seed)    
    random = np.random.randint(0, 100, len(id_list_))
    
    id_list_train = [x for i,x in enumerate(id_list_) if random[i] < per_train]
    id_list_valid = [x for i,x in enumerate(id_list_) if (random[i] >= (per_train)) & 
                                                         (random[i] < (per_train + per_valid))]    
    txt_list_train = [x for i,x in enumerate(txt_list_) if random[i] < per_train]
    txt_list_valid = [x for i,x in enumerate(txt_list_) if (random[i] >= (per_train)) & 
                                                           (random[i] < (per_train + per_valid))]
    hls_list_train = [x for i,x in enumerate(hls_list_) if random[i] < per_train]
    hls_list_valid = [x for i,x in enumerate(hls_list_) if (random[i] >= (per_train)) & 
                                                           (random[i] < (per_train + per_valid))]
    
    if (per_train + per_valid) < 100:
        
        id_list_test = [x for i,x in enumerate(id_list_) if random[i] >= per_train + per_valid]
        txt_list_test = [x for i,x in enumerate(txt_list_) if random[i] >= per_train + per_valid]
        hls_list_test = [x for i,x in enumerate(hls_list_) if random[i] >= per_train + per_valid]
        
        return id_list_train, txt_list_train, hls_list_train, \
               id_list_valid, txt_list_valid, hls_list_valid, \
               id_list_test, txt_list_test, hls_list_test
        
    else: 
        return id_list_train, txt_list_train, hls_list_train, \
               id_list_valid, txt_list_valid, hls_list_valid, \
               None, None, None

if __name__ == "__main__":

	current_ids, current_txt, current_tps, current_hls = importBySource(args.inp_dr, args.source)
    print("Original Length: {}".format(len(current_ids)))
    print("----")
    current_ids, current_txt, current_tps, current_hls = generalCleaner(current_ids, current_txt, current_tps, current_hls)
    print("Final Lenth: {}".format(len(current_ids)))

    if(args.do_tok == True):
    	current_txt = runNorm(current_txt, eval_dir_=opt.eval_dr)
        current_txt = runTok(current_txt, eval_dir_=opt.eval_dr)
        current_hls = runNorm(current_hls, eval_dir_=opt.eval_dr)
        current_hls = runTok(current_hls, eval_dir_=opt.eval_dr)

    ids_train, txt_train, tps_train, ids_valid, txt_valid, tps_valid, ids_test, txt_test, tps_test =  validSplitter(current_ids, current_txt, current_hls, opt.per_train, opt.per_valid, random_seed=1234)

    if(args.do_bpe == True):

        # BPE pipeline TODO




