import os
import sys
import yaml

from cli.parser import Parser

if __name__ == "__main__":

    parser = Parser()
    parser.init()

    args = sys.argv
    print(args)
    
    if len(args) > 1:
        absolute_path = os.path.abspath(args[1])
    else:
        absolute_path = os.path.abspath(".")
    
    print(absolute_path)
    filename = f"{absolute_path}/.projet-creator"

    if os.path.exists(filename):
        print("dir already created")
    else:
        os.makedirs(filename)
        os.system("attrib +h " + filename)

    with open(r'./config.yml') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        fruits_list = yaml.load(file, Loader=yaml.FullLoader)

        print(fruits_list)