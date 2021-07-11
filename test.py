from libs.JavaIO import JavaIO
from libs.JavaParse import JavaParse
import antlr4



jio = JavaIO()
jparse = JavaParse()

def visitor(object):
    if isinstance(object, antlr4.tree.Tree.TerminalNodeImpl):
        print(object.symbol.text)
    else:
        for item in object.children:
            if isinstance(item, antlr4.tree.Tree.TerminalNodeImpl):
                print(item.symbol.text)
            else:
                for sub_item in item.children:
                    visitor(sub_item)

def main():
    src = '/home/nimashiri/vsprojects/CFGsubgraph/sample_codes/test1.java'
    source = jio.getFileContent(src)
    tree = jparse.parse(source)
    visitor(tree)
    print(tree)


if __name__ == '__main__':
    main()
    