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

Once the requirements are met, you can pre-process the data to generate the lazy dataloaders with the following code: 

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

After that, the model can be run using the following specification, where the directory ```INPUT_DIRECTORY```from below is the same as the ```OUTPUT_DIRECTORY``` from above: 

```shell
python train.py -data INPUT_DIRECTORY/bpe \
                -save_model SAVED_MODELS_DIRECTORY \
                -copy_attn \
                -reuse_copy_attn \
                -epochs 20 \
                -gpuid 0 \
                -bridge

```
You can also specify the ```share_embeddings``` option or none. For comparison purposes, run the model using BPE data and data that have not converted into Byte Pairs. 

### Evaluation

To generate the translation, you can run the following: 

```shell
python translate.py -gpu 0 \
                    -batch_size 20 \
                    -beam_size 5 \
                    -model SAVED_MODELS_DIRECTORY \
                    -src PREDICTION DATA \
                    -output OUTPUT_DIRECTORY \
                    -min_length 9 \
                    -verbose \
                    -stepwise_penalty \
                    -coverage_penalty summary \
                    -beta 5 \
                    -length_penalty wu \
                    -alpha 0.9 \
                    -verbose \
                    -block_ngram_repeat 3 \
                    -ignore_when_blocking "." "</t>" "<t>"
```

In the example above, the translations are generated with alpha = 0.9 and minimum 9 words. 
