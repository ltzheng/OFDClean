# OFDClean

Pythpn implementation of Contextual Data Cleaning with Ontological Functional Dependencies.

## Datasets

Dataset, ofds, senses of clinical data of [Python code](https://github.com/ltzheng/OFDClean/Python/datasets) and [Java code](https://github.com/ltzheng/OFDClean/Java/data). 

## Source code

The source code is available [here](https://github.com/ltzheng/OFDClean). 

### Python code 

- Initial sense assignment
- Local sense refinement
- Provided by Longtao Zheng

#### Data path and format

Input data should align with the format in directory `datasets`

#### Run

Configure the path of data, OFDs, and senses in `main.py`, then run `python main.py`.

### Java code 

- Repair data by beam search
- Provided by Zheng Zheng
