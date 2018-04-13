# -*- coding: utf-8 -*-

import numpy as np
import os
import gzip
import re
import argparse
# Check: https://github.com/kpu/preprocess

parser = argparse.ArgumentParser()
parser.add_argument('--inp_dr', default="/scratch/eff254/DL/project/data/gigaword_eng_5/data", type=str, help="Data Directory")
parser.add_argument('--out_dr', default="/scratch/eff254/DL/project/data/gigaword_eng_5_decompressed", type=str, help="Directory for out data")
parser.add_argument('--source', default="nyt_eng", type=str, help="One of ['cna_eng', 'wpb_eng', 'afp_eng', 'xin_eng', 'apw_eng', 'ltw_eng', 'nyt_eng']")
args = parser.parse_args()
print(args)

def importFile(source, file, dr = args.inp_dr): 
    
    '''
    Function to import file, fiven one of the sources
    
    Params:
    @source: string source form list below
    @file: string of filename
    @dr: data directory of data
    
    Returns:
    @file_content: list of bytes, where each element is a line
    '''
    
    list_sources = ['cna_eng', 'wpb_eng', 'afp_eng', 'xin_eng', 'apw_eng', 'ltw_eng', 'nyt_eng']
    if source not in list_sources:
        raise ValueError("Source not found")
        
    with gzip.open(dr + "/" + source + "/"  + file) as f:
        file_content = f.readlines()

    return file_content

def getContent(content, tag="HEADLINE"):
    
    '''
    Parses anything in between of tag with a file opened with importFile()
    
    Params:
    @content: file opened with importFile()
    
    Returns:
    @return_list: list of lines, with length = #of apperance of tag   
    '''
    docs_flags = [i for i, line in enumerate(file_content) if line.decode("UTF-8")=="</DOC>\n"]
    init_index = [i for i, line in enumerate(file_content) if line.decode("UTF-8")=="<" + tag + ">\n"]
    end_index = [i for i, line in enumerate(file_content) if line.decode("UTF-8")=="</" + tag + ">\n"]
    
    return_list = []
    tag_counter = 0
    for i, x in enumerate(docs_flags): 
        
        try:
            if init_index[tag_counter] < docs_flags[i] and init_index[tag_counter] < end_index[tag_counter] -1:
                content_intrest = content[init_index[tag_counter]+1:end_index[tag_counter]]
                return_list.append(content_intrest)
                tag_counter += 1  
            elif init_index[tag_counter] < docs_flags[i] and init_index[tag_counter] >= end_index[tag_counter] -1:
                return_list.append([b'\n'])
                tag_counter += 1 
            else: 
                return_list.append([b'\n'])
        except IndexError:
                return_list.append([b'\n'])
            
    return return_list

quoted = re.compile('"[^"*]*"')

def getDocID(content):
    
    lines_intrest = [line.decode("UTF-8") for i, line in enumerate(file_content) if line.decode("UTF-8")[0:4]=="<DOC"]
    quoted = re.compile('"[^"*]*"')
    list_ids = []
    list_types = []
    
    for i, x in enumerate(lines_intrest):
        list_ids.append(quoted.findall(x)[0].replace('"', ''))
        list_types.append(quoted.findall(x)[1].replace('"', ''))
    
    return list_ids, list_types 

def headlineCleaner(headline_list): 
    
    headline_list = [line[0].decode("UTF-8").replace('\n', '') for i, line in enumerate(headline_list)]
    
    return headline_list

def textCleaner(text_list):
    
    cleaned = []
    for i, text in enumerate(text_list):
        newtext = [x.decode('UTF-8').replace('\n', '') for i,x in enumerate(text) if x.decode('UTF-8') !='<P>\n']
        cleaned.append(" ".join(newtext))
        
    return cleaned

def exporter(list_, filename_, out_dir = args.out_dr):

    with open(out_dir + '/' +  filename_, 'w') as f:
        for i, line in enumerate(list_):
            f.write(line + "\n")

def consistencyChecker(obj): 
    
    for i in range(0, len(obj)-1):       
        if len(obj[i]) != len(obj[i+1]):           
            raise AttributeError("Length of your lists are not the same")

if __name__ == "__main__":
    
    new_out_dir = args.out_dr + "/" + args.source
    if not os.path.exists(new_out_dir):
        os.makedirs(new_out_dir)
    
    all_files = os.listdir(args.inp_dr + "/" + args.source)
    new_names = [name.replace(".gz", "") for name in all_files]
    for i, myfile in enumerate(all_files):
        file_content = importFile(args.source, myfile)
        headlines = getContent(file_content,"HEADLINE")
        headlines = headlineCleaner(headlines)
        text = getContent(file_content,"TEXT")
        text = textCleaner(text)
        id_list, types_id = getDocID(file_content)
        consistencyChecker([id_list, types_id, text, headlines])
        #exporter(headlines, new_names[i] + '.hls', new_out_dir)
        #exporter(text, new_names[i] + '.txt', new_out_dir)
        #exporter(id_list, new_names[i] + '.ids', new_out_dir)
        #exporter(types_id, new_names[i] + '.tps', new_out_dir)
        pickle.dump(headlines, open(new_out_dir + '/' + new_names[i] + '.hls.p', "wb" ) ) 
        pickle.dump(text, open(new_out_dir + '/' + new_names[i] + '.txt.p', "wb" ) ) 
        pickle.dump(id_list, open(new_out_dir + '/' + new_names[i] + '.ids.p', "wb" ) ) 
        pickle.dump(types_id, open(new_out_dir + '/' + new_names[i] + '.tps.p', "wb" ) ) 
        if i % 50==0:
        	print("Processing... {}/{}".format(i, len(all_files)))
