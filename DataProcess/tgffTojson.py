#Audiobeam_Mesh4x4_AIR1__ra1
#python temp.py -i test.tgff -o out.json -r 4

import csv
import numpy as np

import sys
import getopt

import json

import re
import os

def folderprocess(inputfolder):
    g = os.walk(inputfolder)
    for path,dir_list,file_list in g:
        for dir_item in dir_list:
            print(dir_item)
            dir1 = os.walk(os.path.join(path,dir_item))
            meshSize = int(dir_item.split('_')[1])
            appName = dir_item.split('_')[0]
            print(meshSize)
            row = 0
            if(meshSize==16):
                row = 4
            elif(meshSize == 64):
                row = 8
            elif(meshSize == 256):
                row = 16

            for path1,dir_list1,file_list1 in dir1:
                i = 1
                for file_item in file_list1:
                    inputfile = os.path.join(path1,file_item)
                    
                    outputpath = inputfolder+"_json"

                    ouputfile = outputpath +"/"+ appName+"conv1l"+str(i)+"_Mesh"+str(row)+"x"+str(row)+"_"+"AIR1_free.json"
                    i = i+1
                    command = "python g2json_single.py -i "+inputfile+" -o "+ouputfile+" -r "+str(row)
                    os.system(command)

def main(argv):
    inputfile = ''
    saveflag = ''
    try:
        opts, args = getopt.getopt(argv,"hi:s:",["ifile=","saveflag="])
    except getopt.GetoptError:
        print('Error TG2Timeline.py -i <inputfile> -s <saveflag>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('TG2Timeline.py -i <inputfile> -s <saveflag>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            print("read input file")
            inputfile = arg
        elif opt in ("-s", "--saveflag"):
            saveflag = arg

    print('inputfile: ', inputfile)
    folderprocess(inputfile)
    
    
if __name__ == "__main__":
    main(sys.argv[1:])
    