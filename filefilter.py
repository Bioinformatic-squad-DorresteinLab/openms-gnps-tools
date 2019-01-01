import os
import shutil
import sys
import xmltodict as xtd

def parse_folder(dir):
    if not os.path.exists(dir):
        yield None
    for file in os.listdir(dir):
        if "log" not in file:
            yield (dir+"/"+file, os.path.splitext(file)[0].split('-')[1])

'''
#6 module: gnps export
'''
def filefilter(input_port, out_port):
    assert len(list(parse_folder(input_port))) > 0
    for input_file,file_count in list(parse_folder(input_port)):
        # in_cm = in_port+'/'+get_port_outputs(in_port)[0]
        output = out_port+'/'+out_port+"-"+file_count+".consensusXML"

        command = "FileFilter -id:remove_unannotated_features -in " + input_file + " "
        command += "-out " + output + ' >> ' + out_port+'/logfile.txt'

        print("COMMAND: " + command + "\n")
        os.system(command)



if __name__ == '__main__':
    print("===FILE FILTER===")

    # set env
    os.environ["LD_LIBRARY_PATH"] = sys.argv[1]
    os.environ["PATH"] = sys.argv[2]
    os.environ["OPENMS_DATA_PATH"] = os.path.abspath(sys.argv[3])


    filefilter(sys.argv[4], sys.argv[5])
