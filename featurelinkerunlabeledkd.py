import os
import shutil
import sys

def featurelinkerunlabeledkd2(adductdecharger_port, ini_file, out_port):
    print("\n==FEATURE LINKER UNLABELED KD==")

    command = "FeatureLinkerUnlabeledKD -ini " + ini_file + " -in "
    for file in os.listdir(adductdecharger_port):
        if 'log' not in file and 'featureXML' in file:
            command += adductdecharger_port+"/"+file + " "
    command += "-out " + out_port+"/featurelinker.consensusXML" + ' >> ' + out_port+'/logfile.txt'
    # command += " -out " + curr_port+"/tmp.consensusXML"

    print("COMMAND: " + command + "\n")
    os.system(command)

    # delete featureXML file
    # if os.path.exists(out_port+"/featurelinker-tmp.consensusXML"):
    #     os.remove(out_port+"/featurelinker-tmp.consensusXML")

'''
#5 module: feature linker unlabeled kd
'''
def featurelinkerunlabeledkd(adductdecharger_port, ini_file, out_port):
    adductdecharger = sorted([file for file in os.listdir(adductdecharger_port) if 'log' not in file and 'featureXML' in file])
    for i in range(1, len(adductdecharger)):
        file_1 = ""
        if i > 1:
            file_1 = out_port+"/featurelinker-"+str(format(i-2, "04"))+".consensusXML"
        else:
            file_1 = adductdecharger_port+"/"+adductdecharger[0]
        file_2 = adductdecharger_port+"/"+adductdecharger[i]


        print("\n==FEATURE LINKER UNLABELED KD==")

        command = "FeatureLinkerUnlabeledKD -ini " + ini_file + " -in "
        command += file_1 + " " + file_2
        command += " -out " + out_port+"/featurelinker-"+str(format(i-1, "04"))+".consensusXML" + ' >> ' + out_port+'/logfile.txt'
        # command += " -out " + curr_port+"/tmp.consensusXML"

        print("COMMAND: " + command + "\n")
        os.system(command)

    os.rename(out_port+"/featurelinker-"+str(format(len(adductdecharger)-1))+".consensusXML", out_port+"/featurelinker.consensusXML")

    # delete featureXML file
    # if os.path.exists(out_port+"/featurelinker-tmp.consensusXML"):
    #     os.remove(out_port+"/featurelinker-tmp.consensusXML")


if __name__ == '__main__':
    # set env
    if os.environ.has_key("LD_LIBRARY_PATH"):
        os.environ["SANS_LD_LIBRARY_PATH"] = os.environ["LD_LIBRARY_PATH"]
    os.environ["LD_LIBRARY_PATH"] = "/data/beta-proteomics2/tools/openms_2.4/openms-env/conda/lib"

    if os.environ.has_key("PATH"):
        os.environ["SANS_PATH"] = os.environ["PATH"]
    os.environ["PATH"] = "/data/beta-proteomics2/tools/openms_2.4/openms-env/conda/bin:/data/beta-proteomics2/tools/openms_2.4/openms-env/openms-build/bin:$PATH"

    openms_data_path = '/data/beta-proteomics2/tools/openms_2.4/openms-env/share'
    os.environ["OPENMS_DATA_PATH"] = os.path.abspath(openms_data_path)

    curr_dir = os.listdir('.')
    print(curr_dir)
    for dir in curr_dir:
        print(dir+":")
        print(os.listdir(dir))

    # ini file
    ini_file = 'iniFiles/'+os.listdir('iniFiles')[0]
    # shutil.copyfile(ini_file, sys.argv[2])

    # featurelinkerunlabeledkd(sys.argv[1], ini_file, sys.argv[3])
    featurelinkerunlabeledkd2(sys.argv[1], ini_file, sys.argv[3])
    # featurelinkerunlabeledkd(sys.argv[1], sys.argv[2], sys.argv[3])
