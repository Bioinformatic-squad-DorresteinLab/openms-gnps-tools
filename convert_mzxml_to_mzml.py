import os
import shutil
import sys
import multiprocessing as mp
from subprocess import Popen
import ming_parallel_library as mpl

def parse_folder(dir):
    if not os.path.exists(dir):
        raise StopIteration
    for file in sorted(os.listdir(dir)):
        if "log" not in file and file[0] is not '.':
            yield (dir+"/"+file, os.path.splitext(file)[0].split('-')[1])


def get_exec_cmd(input_file, file_count, out_port):
    output = out_port+'/'+out_port+'-'+file_count+'.mzML'

    command = 'FileConverter '
    command += '-in ' + input_file + ' -out ' + output + ' > ' + out_port+'/logfile-'+file_count+'.txt'

    print("COMMAND: " + command + '\n')
    return command


'''
#1 module: feature finder metabo
'''
def fileconverter(input_port, out_port):
    commands = []
    for input_file,file_count in list(parse_folder(input_port)):
        if '.mzml' not in input_file.lower():
            cmd = get_exec_cmd(input_file,file_count,out_port)
            commands.append(cmd)
        else:
            shutil.copyfile(input_file, out_port+"/"+out_port+"-"+file_count+".mzML")

    mpl.run_parallel_shellcommands(commands,8)


if __name__ == '__main__':
    print("===FEATURE FINDER METABO===")

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

    fileconverter(sys.argv[4], sys.argv[5])
