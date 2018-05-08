#!/bin/bash

#### CAREFEULL WITH DOUBLE QUOTATION IN SPACED DIRECTORY!!!
code_dir="/Users/eduardofierro/Google Drive/CuartoSemestre/DeepLearning/Project/DLProject/Preprocess"
data_dir="/Users/eduardofierro/Google Drive/CuartoSemestre/DeepLearning/Project/DLProject/splitting_validation_data"

echo "Applying BPEs to validation set..."
python "$code_dir"/apply_bpe.py -c "$code_dir"/train.article.bpe < "$data_dir"/validation.article.txt > "$data_dir"/validation.article.txt.bpe
python "$code_dir"/apply_bpe.py -c "$code_dir"/train.title.bpe < "$data_dir"/validation.title.txt > "$data_dir"/validation.title.txt.bpe

echo "Applying BPEs to test set..."
python "$code_dir"/apply_bpe.py -c "$code_dir"/train.article.bpe < "$data_dir"/test.article.txt > "$data_dir"/test.article.txt.bpe
python "$code_dir"/apply_bpe.py -c "$code_dir"/train.title.bpe < "$data_dir"/test.title.txt > "$data_dir"/test.title.txt.bpe

echo "END"
