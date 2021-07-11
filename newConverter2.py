import os
import csv, json
import numpy as np

class WordId:
    word_map = {}
    word_id_counter = 0
    def word_id(self, word):
        if word in self.word_map:
            return self.word_map[word]
        else:
            self.word_map[word] = self.word_id_counter
            self.word_id_counter += 1
            return self.word_map[word]

class WordIdGenerator:
    word_map = {}
    word_id_counter = 2
    def word_id(self, word):
        if word in self.word_map:
            return self.word_map[word]
        else:
            self.word_map[word] = self.word_id_counter
            self.word_id_counter += 1
            return self.word_map[word]

def writeDictAsCSV(mydict, filename):
    with open(filename+'.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in mydict.items():
            writer.writerow([key, value])

def readJSON(path_):
    with open(path_, 'r', encoding='utf-8-sig') as f:
        data = json.load(f, strict=False)
    return data

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

def write_stage_2(textfile, part1, part2, index):
    header = [['t', '#', str(index)]]
    #trailer = [['t', '#', '-1']]
    pack = [header, part1, part2, " "]
    for item in pack:
        for element in item:
            element = list(element)
            s = " ".join(map(str, element))
            textfile.write(s+'\n')

def get_values(data, gen, gen2):
    part1 = []
    part2 = []
    node_labels = []
    node_ids = []
    edge_labels = []
    for i in range(len(data)):
       edge_labels.append(data[i]['p'][1])

    edge_labels = [gen.word_id(w) for w in edge_labels]
    # writeDictAsCSV(gen.word_map, 'edges')

    for i in range(len(data)):
        node_labels.append(data[i]['p'][0]['name'])
        node_labels.append(data[i]['p'][2]['name'])

    node_labels = [gen.word_id(w) for w in node_labels] 

    for i in range(len(data)):
        node_ids.append(data[i]['p'][0]['name'])
        node_ids.append(data[i]['p'][2]['name'])   

    node_ids = [gen2.word_id(w) for w in node_ids]


    for i in range(len(data)):
        part1.append(['v', gen2.word_id(data[i]['p'][0]['name']), gen.word_id(data[i]['p'][0]['name'])])
        part1.append(['v', gen2.word_id(data[i]['p'][2]['name']), gen.word_id(data[i]['p'][2]['name'])])

    part1 = [list(x) for x in set(tuple(x) for x in part1)]
    part1 = [list(x) for x in sorted(tuple(x) for x in part1)]
    for i in range(len(data)):
        part2.append(['e', gen2.word_id(data[i]['p'][0]['name']), gen2.word_id(data[i]['p'][2]['name']), gen.word_id(data[i]['p'][1])])
    
    # writeDictAsCSV(gen.word_map, 'nodes')
    return part1, part2

def main():
    gen = WordIdGenerator()
    gen2 = WordId()
    
    #listofFiles = getListOfFiles('/media/nimashiri/DATA/CPGs')

    for root, dirs, files in os.walk('/media/nimashiri/DATA/CPGs'):
        for dir in dirs:
            index = 0
            current_dir = os.path.join(root, dir)
            file_path = '/media/nimashiri/DATA/databases/' + dir + '.txt'
            textfile = open(file_path, "w")
            for cpg in os.listdir(current_dir):
                current_file = os.path.join(current_dir, cpg)
                try:
                    data = readJSON(current_file)
                    part1, part2 = get_values(data, gen, gen2)
                    write_stage_2(textfile,part1, part2, index)
                    index += 1

                    print('I am writing to database!', index)
                except:
                    print('Cannot read the file!')
            textfile.close()
    writeDictAsCSV(gen.word_map, 'nodes_edges')
    

if __name__ == '__main__':
    main()