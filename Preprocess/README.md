# RNN for Text Summarization - Preprocess
Spring 2018 Deep Learning Project
Eduardo Fierro (eff254), Lisa Ren (tr1312), Caroline Roper (cer446)

---

This folder assues that the data comes in pairs: each source and target comes in two different text files, identified by line beraks. For example, source of line 9 in one text file corresponds to the same line in the target file. 

If the data is not yet tokenize, you can simple run the tokenizer perl code. On the particular case of the data used in this project, tokenization was performed beforehand. 

To run the BPE's, you can simple run 
```bash
$ bash BPE-runner.sh
```

This file learns and applies BPE's with ```learn_bpe.py``` and ```apply_bpe.py``` to the train set. Note that inside this file, you need to change ```code_dir```and ```data_dir``` according to the file paths where your data and code are located in your local computer. 

To apply the BPE's to validation and train set, run: 

```bash
$ bash BPE-runner-train-valid.sh
````

Again, change ```code_dir```and ```data_dir``` according to the file paths on your local computer.  
