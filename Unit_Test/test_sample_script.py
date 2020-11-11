#pytest

#import lib
import os.path
import sys
from sample_script import *
import pytest

#test
def test_summation1():
    int=5
    
    assert int==summation(1,4)

def test_summation2():
    int=5

    assert int==error_summation(1,4)

