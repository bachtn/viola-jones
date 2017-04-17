#!/usr/bin/env python3

from classify import *
from predict import *

def main():
    #createData()
    predict('test.jpg', 'trained-classifier.pkl')

if __name__ == '__main__':
    main()
