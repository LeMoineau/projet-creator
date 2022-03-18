import os
import sys

if __name__ == "__main__":
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