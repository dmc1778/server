import os
import subprocess
from subprocess import call, check_output, STDOUT
import shutil
from numpy import log
import requests
from flask import Flask, json, request, jsonify, redirect, render_template
from neo4j import GraphDatabase
import csv
import json
import pandas as pd
import shutil
from pathlib import Path
import codecs
from itertools import filterfalse

from requests.api import head

base_path = '/home/nimashiri/java_projects/test/'

class BinarySearch:
    def binarySearch(self, arr, x):
        l = 0
        r = len(arr)
        while (l <= r):
            m = l + ((r - l) // 2)
    
            res = (x == arr[m])
    
            # Check if x is present at mid
            if (res == 0):
                return m - 1
    
            # If x greater, ignore left half
            if (res > 0):
                l = m + 1
    
            # If x is smaller, ignore right half
            else:
                r = m - 1
    
        return -1

class FilterCPG():
    def __init__(self, jdk_source) -> None:
        self.relations = ['ARGUMENTS', 'EOG', 'DFG', 'CATCH_CLAUSE', 'TRY_BLOCK', 'INVOKES', 'THEN_STATEMENT', 'CONDITION']
        self.jdk_source = jdk_source
        self.bnObject = BinarySearch()

    def applyFilter(self, data, source_code):
        print('I am in filter function!')
        flag = False
        import_list = []
        new_data = []
        #jdk_list = list(self.jdk_source.keys())

        sdict = source_code[0]

        for key, value in sdict.items():
            if 'import ' in value and 'java' in value:
                value = value.replace('import ', '')
                import_list.append(value)
        print('Analyzing dependencies done!')
        import_counter = 0
        for item in import_list:
            sitem = item.split('.')
            if 'java' in sitem[0] or 'javax' in sitem[0] or 'omg' in sitem[1] or 'ietf' in sitem[1] or 'w3c' in sitem[1] or 'xml' in sitem[1]:
                import_counter += 1
        if import_counter > 0:
            flag = True
        print('JDK checking done and returning values!')
        for i, item in enumerate(data):
            if item['p'][1] in self.relations:
                new_data.append(item)
        return new_data, flag        

def loadJSON():
    with open('/home/nimashiri/cpg-master/cpg-neo4j/build/install/cpg-neo4j/bin/JDK_APIS/javadoc_dict_methods.json', 'r') as f:
        d = json.load(f)
    return d

def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def copyFiles(chunks):

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    for i in range(len(chunks)):
        cpg = 'cpg'
        if not os.path.exists(base_path+'/'+cpg+str(i)):
            os.makedirs(os.path.join(base_path, cpg+str(i)))

    _dirs = os.listdir('/home/nimashiri/java_projects/test')

    for i, p in enumerate(chunks):
        for _file in chunks[i]:
            _l = _file.split('/')
            if '.java' in _l[-1]:
                if os.path.getsize(_file) < 3500:
                    shutil.copy(_file, os.path.join(base_path, _dirs[i]))


def write_json(data, filename, addr):
    x = filename.split('.')
    if not os.path.exists(addr):
        os.makedirs(addr)
    file_ = os.path.join(addr, x[0]+'.json')
    with open(file_, 'w') as f:
        json.dump(data, f, indent=4)


def save_logs(log_path, data):
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    data = pd.DataFrame(data)
    _log_path = os.path.join(log_path, 'logs.csv')
    data.to_csv(_log_path, index=False)


def read_code_file(file_path):
    code_lines = {}
    file_path = Path(file_path)
    if file_path.exists:
        ret = False
        with open(file_path, 'r', encoding="ISO-8859-1") as fp:
            for ln, line in enumerate(fp):
                assert isinstance(line, str)
                line = line.strip()
                if '//' in line:
                    line = line[:line.index('//')]
                code_lines[ln + 1] = line
    else:
        ret = True
    return code_lines, ret

def writeCodefile(name, codefile):
    with codecs.open(name, 'w') as f_method:
        for line in codefile:
            f_method.write("%s\n" % codefile[line])
        f_method.close()

def main():

    jdk_source = loadJSON()

    filter = FilterCPG(jdk_source)

    log_holder = []
    log_holder.append(['Project name', 'filtered file'])

    log_path = './logs'
    counter = 0
    for root, dirs, files in os.walk('/media/nimashiri/DATA/java_projects/'):
        for project in dirs:
            current_project = os.path.join(root, project)
            listOfFiles = getListOfFiles(current_project)
            for _dirs in listOfFiles:
                #_dirs = '/media/nimashiri/DATA/java_projects/commons-math-MATH_3_6_1/src/main/java/org/apache/commons/math3/optimization/direct/BOBYQAOptimizer.java'
                _l = _dirs.split('/')
                r1 = _l.count('tests')
                r2 = _l.count('test')
                a = _l[-1].replace('.java', '.json')       
                if r1 == 0 and r2 == 0:
                    if '.java' in _l[-1]:
                        if not os.path.isfile(os.path.join('/media/nimashiri/DATA/CPGs', project, a)):
                            try:
                                source_code = read_code_file(_dirs)
                                #writeCodefile(_l[-1],filter1_code)
                                print('I am analyzing: {}'.format(_dirs))
                                strr = './cpg-neo4j --host=localhost --port=7687 --user=neo4j --password=nima1370' + \
                                    ' ' + _dirs + ' ' + '--save-depth=-1'
                                try:
                                    cmd_out = check_output(strr, stderr=STDOUT, shell=True).decode()
                                #a = call([strr], stderr=STDOUT, shell=True)
                                except Exception as e:
                                    if not 'OutOfMemoryError' in e.output.decode():
                                        print(e.output.decode())
                                        res_get = requests.get(
                                                    'http://127.0.0.1:5050/display')
                                        data = res_get.json()                                
                                        new_data, status = filter.applyFilter(data, source_code)
                                        if status:
                                            addr = os.path.join('/media/nimashiri/DATA/CPGs', project)

                                            write_json(new_data, _l[-1], addr)
                                            requests.post('http://127.0.0.1:5050/delete')
                                            counter += 1
                                            print('CPG Generation Done!', counter)
                                            print('################################')
                                        else:
                                            print('Couldnt find JDK API in this file!')
                                            print('################################')
                                            log_holder.append([project, _dirs, 'Couldnt find JDK API in this file!'])
                                            save_logs(log_path, log_holder)
                                    else:
                                        print("I have an OutOfMemoryError! and loging the details!")
                                        log_holder.append([project, _dirs, 'OutOfMemoryError'])
                                        save_logs(log_path, log_holder)
                            except Exception as e:
                                print(e)
                    else:
                        print('CPG file already exists!')


if __name__ == '__main__':
    main()
