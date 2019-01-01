import os
import shutil
import sys
from subprocess import Popen


def parse_folder(dir):
    if not os.path.exists(dir):
        raise StopIteration
    for file in sorted(os.listdir(dir)):
        if "log" not in file and file[0] is not '.':
            # print(os.path.splitext(file)[0].split('-')[1])
            yield (dir+"/"+file, os.path.splitext(file)[0].split('-')[1])


def get_exec_cmd(input_file, file_count, ini_file, out_port):
    output = out_port+'/'+out_port+'-'+file_count+'.featureXML'

    command = 'FeatureFinderMetabo '
    if ini_file is not None:
        command += '-ini ' + ini_file + ' '
    command += '-in ' + input_file + ' -out ' + output + ' >> ' + out_port+'/logfile.txt'

    print("COMMAND: " + command + '\n')
    return command
    # os.system(command)


'''
#1 module: feature finder metabo
'''
def featurefindermetabo(input_port, ini_file, out_port):
    assert len(list(parse_folder(input_port))) > 0
    print(list(parse_folder(input_port)))

    commands = []
    for input_file,file_count in list(parse_folder(input_port)):
        cmd = get_exec_cmd(input_file,file_count,ini_file,out_port)
        commands.append(cmd)

    processes = [Popen(cmd, shell=True) for cmd in commands]

    for p in processes: p.wait()


if __name__ == '__main__':
    print("===FEATURE FINDER METABO===")

    print(sys.argv)

    # set env
    os.environ["LD_LIBRARY_PATH"] = sys.argv[1]
    # os.environ["LD_LIBRARY_PATH"] = "/data/beta-proteomics2/tools/openms_2.4/openms-env/conda/lib"
    os.environ["PATH"] = sys.argv[2]
    # os.environ["PATH"] = "/data/beta-proteomics2/tools/openms_2.4/openms-env/openms-build/bin:/data/beta-proteomics2/tools/openms_2.4/openms-env/conda/bin:$PATH"

    openms_data_path = sys.argv[3]
    # openms_data_path = '/data/beta-proteomics2/tools/openms_2.4/openms-env/share'
    os.environ["OPENMS_DATA_PATH"] = os.path.abspath(openms_data_path)

    # ini file
    ini_file = None
    if os.path.exists('iniFiles'):
        ini_dir = list(parse_folder('iniFiles'))
        if len(ini_dir) > 0:
            ini_file = ini_dir[0][0]

    featurefindermetabo(sys.argv[4], ini_file, sys.argv[6])
