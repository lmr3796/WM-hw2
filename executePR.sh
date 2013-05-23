#! /usr/bin/env bash

INPUT_FILE=$1
OUTPUT_FILE=`basename $1.pagerank.student`

./pagerank.py $INPUT_FILE > $OUTPUT_FILE
echo -e "\nResults is at $OUTPUT_FILE" 1>&2
