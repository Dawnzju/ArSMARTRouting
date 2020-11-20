import csv
import numpy as np

import sys
import getopt

import json

import re
import os


class transData:

    def __init__(self,filename,exe,trans):
        self.filename = filename
        self.exe = exe
        self.trans = trans

    def readJson(self,file_name):
        with open(file_name) as load_f:
            load_dict = json.load(load_f)
            return load_dict



    def dataProcess(self,taskGraph,file_name):
        outfolder = self.filename+"_result"
        outfile = outfolder+"/"+file_name
        for key,value in taskGraph.items():
            taskGraph[key]['exe_time'] = int(taskGraph[key]['exe_time']/self.exe)
            for i in range(0,len(taskGraph[key]['out_links'])):
                taskGraph[key]['out_links'][i][0][1] = int(taskGraph[key]['out_links'][i][0][1]/self.trans)
        for i in range(0,len(taskGraph)):
            sumSend1 = 0
            for outputLink in taskGraph[str(i)]['out_links']:
                sumSend1 = sumSend1 + outputLink[0][1]
            taskGraph[str(i)]['total_needSend'] = sumSend1
            sumSend = 0
            for outputLink in taskGraph[str(i)]['input_links']:
                sumSend = sumSend + outputLink[0][1]
            taskGraph[str(i)]['total_needReceive'] = sumSend
 

        with open(outfile,"w") as outfile:
            json.dump(taskGraph,outfile)


    def folderprocess(self):
        g = os.walk(self.filename)
        for path,dir_list,file_list in g:
            for file_name in file_list:
                mapfile = os.path.join(path,file_name)
                taskGraph = self.readJson(mapfile)
                self.dataProcess(taskGraph,file_name)



def main(argv):
    inputfile = ''
    exe = ''
    trans = ''

    try:
        opts, args = getopt.getopt(argv,"hi:e:t:",["ifile=","exe=","trans="])
    except getopt.GetoptError:
        print('Error exeandtrans.py -i <inputfile> -e <exe> -t <trans>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('TG2Timeline.py -i <inputfile> -e <saveflag>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            print("read input file")
            inputfile = arg
        elif opt in ("-e", "--exe"):
            exe = int(arg)
        elif opt in ("-t", "--trans"):
            trans = int(arg)

    #print('inputfile: ', inputfile)
    

    transdata = transData(inputfile,exe,trans)
    transdata.folderprocess()

    
if __name__ == "__main__":
    main(sys.argv[1:])
    