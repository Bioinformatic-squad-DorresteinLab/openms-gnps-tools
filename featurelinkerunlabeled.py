import os
import shutil
import sys
import xmltodict as xtd

def parse_folder(dir):
    for file in sorted(os.listdir(dir)):
        if "log" not in file and 'featureXML' in file:
            yield (dir+"/"+file, os.path.splitext(file)[0].split('-')[1])


def parse_out_folder(dir):
    for file in os.listdir(dir):
        if "log" not in file in file:
            yield (dir+"/"+file, os.path.splitext(file)[0].split('-')[1])


'''
#5 module: feature linker unlabeled kd
'''
def featurelinkerunlabeledkd(input_port, ini_file, out_port):
    assert len(list(parse_folder(input_port))) > 0

    command = "FeatureLinkerUnlabeledKD "
    if ini_file is not None:
        command += "-ini " + ini_file + " "
    command += "-in "
    for input_file,file_count in list(parse_folder(input_port)):
        command += input_file + " "
    command += "-out " + out_port+"/"+out_port+"-0000.consensusXML" + ' >> ' + out_port+'/logfile.txt'
    # command += " -out " + curr_port+"/tmp.consensusXML"

    print("COMMAND: " + command + "\n")
    os.system(command)

    # delete featureXML file
    # if os.path.exists(out_port+"/featurelinker-tmp.consensusXML"):
    #     os.remove(out_port+"/featurelinker-tmp.consensusXML")


'''
#5 module: feature linker unlabeled qt
'''
def featurelinkerunlabeledqt(input_port, ini_file, out_port):
    command = "FeatureLinkerUnlabeledQT "
    if ini_file is not None:
        command += "-ini " + ini_file + " "
    command += "-in "
    for input_file,file_count in list(parse_folder(input_port)):
            command += input_file + " "
    command += "-out " + out_port+"/"+out_port+"-0000.consensusXML" + ' >> ' + out_port+'/logfile.txt'
    # command += " -out " + curr_port+"/tmp.consensusXML"

    print("COMMAND: " + command + "\n")
    os.system(command)


def fix_filenames(out_port, mapping_file):
    print("correcting filenames in featurelinker step...")

    files = dict()
    with open(mapping_file) as f:
        file_dict = xtd.parse(f.read())
        for map_line in file_dict['parameters']['parameter']:
            if "upload_file_mapping" in map_line['@name'] and "inputFiles" in map_line['#text']:
                map = map_line['#text'].split('|')
                raw_file_path = os.path.splitext(map[0])[0].split('-')[1]

                print("mapping",raw_file_path,"->",map[1])
                files[int(raw_file_path)] = map[1]

    print(list(parse_out_folder(out_port)))
    for input_file,file_count in list(parse_out_folder(out_port)):
        with open(input_file) as f:
            file_dict = xtd.parse(f.read())
    
        for map in file_dict['consensusXML']['mapList']['map']:
            print("\tid:", map['@id'], '\t', map['@name'], '\t-->\t', files[int(map['@id'])])
            map['@name'] = files[int(map['@id'])]

        # export file_dict
        out = xtd.unparse(file_dict, pretty=True)
        with open(out_port+"/featurelinkerunlabeled-0000.consensusXML", 'w') as file:
            file.write(out)

    print("out port dir:", os.listdir(out_port))


if __name__ == '__main__':
    print("\n==FEATURE LINKER UNLABELED QT==")

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

    # tool type
    linker_tool = "Feature Linker Unlabeled QT"
    with open(sys.argv[7], "r") as f:
        params = xtd.parse(f.read())
        for param in params['parameters']['parameter']:
            if param['@name'] == "featurelinkerunlabeled.tool_type":
                linker_tool = param['#text']

    if linker_tool == "Feature Linker Unlabeled QT":
        featurelinkerunlabeledqt(sys.argv[4], ini_file, sys.argv[6])
    else:
        featurelinkerunlabeledkd(sys.argv[4], ini_file, sys.argv[6])

    fix_filenames(sys.argv[6], sys.argv[7])
