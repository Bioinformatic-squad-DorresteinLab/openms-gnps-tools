import os
import sys
import shutil
import xmltodict as xtd

OUTPUT_DIR_INDEX = len(sys.argv) - 1

if __name__ == '__main__':
    print("===PARSE OUTPUT===")

    print('\ncurrent directory...')
    curr_dir = os.listdir('.')
    print(curr_dir)
    for dir in curr_dir:
        print(dir+":")
        print(os.listdir(dir))

    print('\nmoving directories into output dir...')
    output_dir = sys.argv[OUTPUT_DIR_INDEX]

    # copy output files
    for input_dir in sys.argv[1:OUTPUT_DIR_INDEX]:
        print("move -- " + input_dir + " -> " + output_dir+"/"+input_dir)
        shutil.copytree(input_dir, output_dir+"/"+input_dir)

    # copy iniFiles
    shutil.copytree("iniFiles", output_dir+"/iniFiles")

    # copy log files to log folder
    os.mkdir('logs')
    for input_dir in sys.argv[1:OUTPUT_DIR_INDEX]:
        for filepath in os.listdir(input_dir):
            input_file = input_dir+'/'+filepath
            if 'log' in filepath:
                shutil.copyfile(input_file, output_dir+"/"+input_file)
