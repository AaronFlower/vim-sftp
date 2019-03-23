from os.path import realpath, dirname

def printDir ():
    print (file_name)
    cur_dir = dirname(file_name)

    while cur_dir:
        print(cur_dir)
        if cur_dir == '/' :
            break
        cur_dir = dirname(cur_dir)
    return
