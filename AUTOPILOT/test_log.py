#!/usr/bin/env python
import pickle
import os
import sys
import pdb

with open("default/log1.pkl", "rb") as file:
    emp = pickle.load(file)
    pdb.set_trace()