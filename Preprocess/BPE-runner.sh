#!/bin/bash

#### CAREFEULL WITH DOUBLE QUOTATION IN SPACED DIRECTORY!!!
code_dir="/Users/eduardofierro/Google Drive/CuartoSemestre/DeepLearning/Project/DLProject/Preprocess"
data_dir="/Users/eduardofierro/Google Drive/CuartoSemestre/DeepLearning/Project/Data/sumdata/train"

#### BPE RUNNER.

echo "Learning BPEs from train set..."

# If file doesn't exist, then...
if [ ! -f "$data_dir"/train.article.bpe ]; then
    echo "Processing Article BPEs..."
    python "$code_dir"/learn_bpe.py -s 20000 < "$data_dir"/train.article.txt > "$data_dir"/train.article.bpe
fi
if [ ! -f "$data_dir"/train.title.bpe ]; then
    echo "Processing Title BPEs..."
    python "$code_dir"/learn_bpe.py -s 20000 < "$data_dir"/train.title.txt > "$data_dir"/train.title.bpe
fi

echo "Applying BPEs to train set..."
python "$code_dir"/apply_bpe.py -c "$data_dir"/train.article.bpe < "$data_dir"/train.article.txt > "$data_dir"/train.article.txt.bpe
python "$code_dir"/apply_bpe.py -c "$data_dir"/train.title.bpe < "$data_dir"/train.title.txt > "$data_dir"/train.title.txt.bpe

echo "Applying BPEs to valid set..."
python "$code_dir"/apply_bpe.py -c "$data_dir"/train.article.bpe < "$data_dir"/valid.article.filter.txt > "$data_dir"/valid.article.filter.txt.bpe
python "$code_dir"/apply_bpe.py -c "$data_dir"/train.title.bpe< "$data_dir"/valid.title.filter.txt > "$data_dir"/valid.title.filter.txt.bpe