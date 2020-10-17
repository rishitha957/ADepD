import os
import re
import ast
from pprint import pprint
from collections import deque
import astunparse
from visitors import ClassVisitor, DocStringVisitor, FuncVisitor
from get_all_api_calls import automatic_api_deprecation_detection as ADepD

path_list = ['./scikit-learn/sklearn/','./numpy/numpy/','./pandas/pandas/','./scipy/scipy/',
				'./matplotlib/','./seaborn/seaborn/']

file2 = open("output.txt","w")

for path in path_list:
	package = path.split("/")[-2]
	print(package)
	file1 = open(package+"_all_api_calls.txt","w")
	ADepD(file1,file2,path)
