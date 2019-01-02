import os
import shutil
import sys
from subprocess import Popen


def parse_folder(dir):
    if not os.path.exists(dir):
        yield None
    for file in sorted(os.listdir(dir)):
        if "log" not in file:
            yield (dir+"/"+file, os.path.splitext(file)[0].split('-')[1])


def get_exec_cmd(input_file, file_count, ini_file, idxml_path, input_port, out_port):
    command = 'IDMapper '
    if ini_file is not None:
        command += '-ini ' + ini_file + ' '
    command += '-in ' + input_file + ' -id ' + idxml_path + ' '
    command += '-spectra:in ' + input_port+'/'+input_port+'-'+file_count+".mzML"

    output = out_port+'/'+out_port+'-'+file_count+'.featureXML'
    command += ' -out ' + output + ' >> ' + out_port+'/logfile.txt'

    print("COMMAND: " + command + '\n')
    return command


'''
#2 module: id mapper
'''
def idmapper(input_port, ini_file, idxml_path, featurefinder_port, out_port):
    assert len(list(parse_folder(featurefinder_port))) > 0, \
      "ERROR: issue with featurefindermetabo step"

    commands = []
    for input_file,file_count in list(parse_folder(featurefinder_port)):
        cmd = get_exec_cmd(input_file,file_count,ini_file,idxml_path,\
          input_port,out_port)
        commands.append(cmd)

    mpl.run_parallel_shellcommands(commands,8)
    # processes = [Popen(cmd, shell=True) for cmd in commands]
    #
    # for p in processes: p.wait()


if __name__ == '__main__':
    print("===ID Mapper===")

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

    idmapper(sys.argv[4], ini_file, sys.argv[6], sys.argv[7], sys.argv[8])
    # idmapper(sys.argv[1], ini_file, sys.argv[3], sys.argv[4], sys.argv[5])
