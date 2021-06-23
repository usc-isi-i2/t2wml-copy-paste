# t2wml-copy-paste

## Requirements

* [Install Anaconda](https://docs.anaconda.com/anaconda/install/)

## Setup

* To create virtual env: `conda create --name sheet_annotator_venv python=3.8 -y`
* To activate: `conda activate sheet_annotator_venv`
* To install dependencies: `pip3 install -r requirements.txt`
* To lock/capture installed dependencies: `pip3 freeze > requirements.lock.txt`
* To deactivate: `conda deactivate`
* To remove: `conda remove --name sheet_annotator_venv --all -y`

## To run tests
    cd test 
    pytest

## Starting Jupyter notebook

`jupyter notebook --no-browser`

Follow the link in the console output to access the Jupyter notebook
