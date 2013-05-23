#! /usr/bin/env bash

INPUT_FILE=$1
OUTPUT_FILE=`basename $1.lexrank.student`
IDF_FILE=./idf
T=0.1

./lexrank.py $T $IDF_FILE $INPUT_FILE > $OUTPUT_FILE
echo -e "\nResults is at $OUTPUT_FILE" 1>&2
