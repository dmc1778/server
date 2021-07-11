
from subprocess import call
import os

def read_file(database_name):
    with open(database_name) as f:
        lines = f.readlines()
        lines = [line.replace('\n', '') for line in lines]
    return lines

class SUMMARY:
    def __init__(self) -> None:
        self.TOTAL_PATTERNS = 0
        self.TOTAL_VERTICES = 0
        self.TOTAL_EDGES = 0

    def get_statustics(self, lines):
        clustered = []
        temp = []
        for line in lines:
            if line == '':
                self.TOTAL_PATTERNS += 1
            if 'v' in line:
                self.TOTAL_VERTICES += 1
            if 'e' in line:
                self.TOTAL_EDGES += 1
        

def main():
    sm = SUMMARY()
    # for i in range(2, 5):
    #     for j in range(100, 1000, 100):
    #         name_str = 'edge' + str(i) + 'k' + str(j)
    #         strr = 'java -jar spmf.jar run TKG sample.txt /home/nimashiri/vsprojects/CFGsubgraph/databases/' + name_str + '.txt' + ' ' + str(j) + ' ' + str(i) + ' ' + 'true false true'
    #         call([strr], shell=True)

    for root, dirs, files in os.walk('databases'):
        for file in sorted(files):
            current_database = os.path.join(root, file)
            lines = read_file(current_database)
            sm.get_statustics(lines)
            print("Summary for database {}".format(file))
            print("===========================================================")
            print("The total number of vertices {}".format(sm.TOTAL_PATTERNS))
            print("The total number of edges {}".format(sm.TOTAL_EDGES))
            print("The total number of patterns {}".format(sm.TOTAL_VERTICES))
            print("===========================================================")


if __name__ == '__main__':
    main()
    