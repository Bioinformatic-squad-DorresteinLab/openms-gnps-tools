import os
import shutil
import sys

def parse_folder(dir):
    if not os.path.exists(dir):
        yield None
    for file in sorted(os.listdir(dir)):
        if "log" not in file:
            yield (dir+"/"+file, os.path.splitext(file)[0].split('-')[1])


'''
#3 module: map aligner pose clustering
'''
def mapalignerposeclustering(input_port, ini_file, out_port):
    assert len(list(parse_folder(input_port))) > 0
    command = "MapAlignerPoseClustering "
    if ini_file is not None:
        command += "-ini " + ini_file + " "
    command += "-in "
    for input_file,file_count in list(parse_folder(input_port)):
        command += input_file + ' '

    command += '-out '
    for input_file,file_count in list(parse_folder(input_port)):
        command += out_port+"/"+out_port+"-"+file_count+".featureXML" + ' '
    command += ' > ' + out_port+'/logfile.txt'

    print("COMMAND: " + command + "\n")
    os.system(command)


if __name__ == '__main__':
    print("===MAP ALIGNER POSE CLUSTERING===")

    # set env
    os.environ["LD_LIBRARY_PATH"] = sys.argv[1]
    os.environ["PATH"] = sys.argv[2]
    os.environ["OPENMS_DATA_PATH"] = os.path.abspath(sys.argv[3])

    # ini file
    ini_file = None
    if os.path.exists('iniFiles'):
        ini_dir = list(parse_folder('iniFiles'))
        if len(ini_dir) > 0:
            ini_file = ini_dir[0][0]

    mapalignerposeclustering(sys.argv[4], ini_file, sys.argv[6])
    # mapalignerposeclustering(sys.argv[1], sys.argv[2], sys.argv[3])
