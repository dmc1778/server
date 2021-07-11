import json
import os

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

def readJSON(path_):
    with open(path_, 'r') as f:
        data = json.load(f, strict=False)
    return data

def get_node_info(value):
    part1 = []
    for item in value:
        part1.append(['v', item['id'], item['label']])
    return part1

def get_edge_info(value):
    part2 = []
    for item in value:
        if not bool(item["label"]):
            item['label'] = 'Empty'
        part2.append(['e', item['source'], item['target'], item['label']])
    return part2

def get_values(data):
    part1 = get_node_info(data['nodes'])
    part2 = get_edge_info(data['edges'])
    return part1, part2

def load_temp(filename, superlist, gen):
    #f = open(filename, 'r')
    #data = f.readlines()
    str_list = []
    data = superlist
    for i in range(1, len(data)-1):
        #data[i] = data[i].replace('\n', '')
        #temp = data[i].split(' ')
        temp = data[i]
        if temp[0] == 'v':
            if len(temp[2:]) > 1:
                a = "".join(temp[2:])
                str_list.append(a)
            else:
                str_list.append(temp[2])
        else:
            str_list.append(temp[3])
    final = [gen.word_id(w) for w in str_list]
    
    list1 = []
    for i in range(1, len(data)-1):
        #data[i] = data[i].replace('\n', '')
        #temp = data[i].split(' ')
        temp = data[i]
        if temp[0] == 'v':
            if len(temp[2:]) > 1:
                new_temp = temp[0],temp[1],final[i-1]
                list1.append(new_temp)
            else:
                new_temp = temp[0],temp[1], final[i-1]
                list1.append(new_temp)
        else:
            temp[-1] = final[i-1]
            list1.append(temp)
    return list1


def writeValues(part1, part2, textfile, index):
    header = [['t', '#', str(index)]]
    trailer = [['t', '#', '-1']]
    a_list = [header,part1, part2,trailer]
    super_list = []
    for part in a_list:
        for element in part:
            # element[-1] = element[-1].replace(" ", "")
            #s = " ".join(map(str, element))
            #textfile.write(s+'\n')
            super_list.append(element)
    #textfile.close()
    return super_list

def write_stage_2(textfile,newList, index):
    header = [['t', '#', str(index)]]
    trailer = [['t', '#', '-1']]
    pack = [header, newList, trailer]
    for item in pack:
        for element in item:
            element = list(element)
            s = " ".join(map(str, element))
            textfile.write(s+'\n')

def main():
    gen = WordIdGenerator()
    file_path = '/home/nimashiri/gSpan-master/graphdata/sample.txt'
    textfile = open(file_path, "w")
    index = 0
    for root, _, files in os.walk('json_folder'):
        for _file in files:
            current_file = os.path.join(root, _file)
            try:
                data = readJSON(current_file)
                part1, part2 = get_values(data)
                super_list = writeValues(part1, part2, textfile, index)
                newList = load_temp(file_path, super_list, gen)
                write_stage_2(textfile, newList, index)
                index += 1
            except:
                print('Cannot read the file!')
    textfile.close()
    


    

if __name__ == '__main__':
    main()
    
