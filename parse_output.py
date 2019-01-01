import os
import sys
import shutil
import xmltodict as xtd

OUTPUT_DIR_INDEX = 9

if __name__ == '__main__':
    print("===PARSE OUTPUT===")

    # set env
    # if os.environ.has_key("LD_LIBRARY_PATH"):
    #     os.environ["SANS_LD_LIBRARY_PATH"] = os.environ["LD_LIBRARY_PATH"]
    # os.environ["LD_LIBRARY_PATH"] = "/data/beta-proteomics2/tools/openms_2.4/openms-env/conda/lib"
    #
    # if os.environ.has_key("PATH"):
    #     os.environ["SANS_PATH"] = os.environ["PATH"]
    # os.environ["PATH"] = "/data/beta-proteomics2/tools/openms_2.4/openms-env/conda/bin:/data/beta-proteomics2/tools/openms_2.4/openms-env/openms-build/bin:$PATH"
    #
    # openms_data_path = '/data/beta-proteomics2/tools/openms_2.4/openms-env/share'
    # os.environ["OPENMS_DATA_PATH"] = os.path.abspath(openms_data_path)

    print('\ncurrent directory...')
    curr_dir = os.listdir('.')
    print(curr_dir)
    for dir in curr_dir:
        print(dir+":")
        print(os.listdir(dir))

    print('\nmoving directories into output dir...')
    output_dir = sys.argv[OUTPUT_DIR_INDEX]
    for input_dir in sys.argv[1:OUTPUT_DIR_INDEX]:
        print("move -- " + input_dir + " -> " + output_dir+"/"+input_dir)
        shutil.copytree(input_dir, output_dir+"/"+input_dir)
