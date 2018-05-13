# RNN for Text Summarization
Spring 2018 Deep Learning Project
Eduardo Fierro (eff254), Lisa Ren (tr1312), Caroline Roper (cer446)

---

### Files

You can download the RAW and pre-processed data used in this project from an NYU email (XXXX@nyu.edu) from the following link: https://bit.ly/2IEN7Ke

### Preporcess

To pre-process the data, we followed Rico Sennrich's subword-NMT scripts, available originally here: https://github.com/rsennrich/subword-nmt. All the files are available in the Preprocess folder inside this repository. Please refer to the README.md file inside that folder for instructions of replication. 

### Open-NMT

The model follows the specification publicly available by Guillaume Klein, Yoon Kim, Yuntian Dengm, Jean Senellart and Alexander M. Rush, available here: https://github.com/OpenNMT/OpenNMT-py. Due to recent changes for the implementation of pytorch 0.4, the codes were forked to this repository. For requirements, please refer to the README.md file of the repository. 

### Training models

Once the requirements are met, you can pre-process the data to generate the lazy dataloaders with the followin code: 

```shell
python preprocess.py -train_src DIRECTORY_TO_SOURCE_TRAIN/train.article.txt.bpe \
                     -train_tgt DIRECTORY_TO_TARGET_TRAIN/train.title.txt.bpe \
                     -valid_src DIRECTORY_TO_SOURCE_VALIDATION/valid.article.filter.txt.bpe \
                     -valid_tgt DIRECTORY_TO_TARGET_VALIDATION/valid.title.filter.txt.bpe \
                     -save_data OUTPUT_DIRECTORY/bpe \
                     -src_seq_length 10000 \
                     -dynamic_dict \
                     -share_vocab \
                     -max_shard_size 524288000                                               
```

After that, the model can be run using the following specificatio, where the directory ```INPUT_DIRECTORY```from below is the same as the ```OUTPUT_DIRECTORY``` from above: 

```shell
python train.py -data INPUT_DIRECTORY/bpe \
                -save_model SAVED_MODELS_DIRECTORY \
                -copy_attn \
                -reuse_copy_attn \
                -epochs 20 \
                -gpuid 0 \
                -bridge

```


