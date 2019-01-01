import os
import shutil
import sys
import xmltodict as xtd

if __name__ == '__main__':
    print("===CLEAN CONSENSUS===")

    # cli args
    consensus_file = sys.argv[1]
    output_dir  = sys.argv[2]

    with open(consensus_file, 'r') as cf:
        params = xtd.parse(cf.read())
        element_index = 0
        while params['consensusXML']['consensusElementList'] and element_index < len(params['consensusXML']['consensusElementList']):
            if !params['consensusXML']['consensusElementList'][element_index]['PeptideIdentification'] or len(params['consensusXML']['consensusElementList'][element_index]['PeptideIdentification']) == 0:
                del params['consensusXML']['consensusElementList'][element_index]
            else:
                element_index = element_index + 1

        filename = os.path.splitext(file)[0].split('-')[1]
        output = out_port + '/featurelinker-' + filename + '.consensusXML'
        params.unparse(params, output)
