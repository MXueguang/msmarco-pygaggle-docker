#!/bin/bash
wget https://git.uwaterloo.ca/jimmylin/anserini-indexes/raw/master/index-robust04-20191213.tar.gz
tar xvfz index-robust04-20191213.tar.gz -C pygaggle/indexes
rm index-robust04-20191213.tar.gz
