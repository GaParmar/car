#!/usr/bin/env python
import pickle
import os
import sys
import pdb

with open("log1.pkl", "rb") as file:
    emp = pickle.load(file)
    pdb.set_trace()