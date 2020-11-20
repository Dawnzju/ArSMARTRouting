import csv
import numpy as np

import sys
import getopt

import json

import re
import os


class transData:

    def __init__(self,filename):
        self.filename = filename
        self.resultfolder = "./taskresult"
        self.mapfolder = "./taskmap"

    def findFirstIndex(self,line):
        i=0
        for item in line:
            if(item != '\t'):
                return i
            i=i+1
        return i

    def readcsv(self,fileMain):
        with open(fileMain) as f:
            reader = csv.reader(f)
            fieldnames = next(reader)
            csv_reader = csv.DictReader(f,fieldnames=fieldnames)

            allData = []

            for row in csv_reader:
                d={}
                for k,v in row.items():
                    d[k]=v
                allData.append(d)
                
            return allData

    def readmfile(self,fileMain):
        file_object = open(fileMain,'r+')

        resultAll=[]
        z=0
        result={}
        for line in file_object:
            t = self.findFirstIndex(line)
            if((t+2)<len(line)):
                if(line[t]=='L' and line[t+1]=='a'):
                    result['name'] = line.split(' ')[1]
                    #print(result['name'])
                elif(line[t]=='T' and line[t+1]=='y'):
                    result['type'] = line.split(' ')[1]
                    #print(result['type'])
                elif(line[t]=='S' and line[t+1]=='t'):
                    result['stride'] = line.split('{')[1]
                    #print(result['stride'])
                elif(line[t]=='D' and line[t+1]=='i'):
                    dimen={}
                    # print("line: ",line)
                    # for item in line.split('{')[1].split(','):
                    #     print(item)
                    #     try:
                    #         a = item.split(':')
                    #         t= a[1]
                    #         dimen[a[0][1]] = int(re.findall(r"\d+\.?\d*",t)[0])
                    #     except IndexError:
                    #         a = item.split(' ')
                    #         if(a[0]==''):
                    #             t = a[2]
                    #             z = a[1]
                    #         else:
                    #             t = a[1]
                    #             z = a[0]
                    #         dimen[z] = int(re.findall(r"\d+\.?\d*",t)[0])
                        
                    result['dimen'] = dimen
                    #print(result['dimen'])
                elif(line[t]=='D' and line[t+1]=='a' and z==0):
                    z=1
                    #print("start")

                    result['dataflow']=[]
                elif(z==1 and line[t]!='}'):
                    #print("append")

                    a = ''.join(re.findall(r'[A-Za-z]',line))
                    if(a[0]!='C'):
                        continue
                    else:
                        print()
                        t = ''.join(re.findall(r'[0-9]',line))
                        size = int(t)

                        result['dataflow'] = size
            elif(z==1 and line[t]=='}'):
                z=0
                #print(result['dataflow'])
                resultAll.append(result)
                result={}
        nameMap = {}
        print(resultAll)
        for item in resultAll:
            nameMap[item['name']]= item['dataflow']

        return nameMap

    def dataProcess(self,fileMain,mapfile,taskfile):
        layerinfor = self.readcsv(taskfile)

        nameMap = self.readmfile(mapfile)
        # print(layerinfor)
        print(nameMap)
        
        for onelayer in layerinfor:
            numPE = int(layerinfor[0][' NumPEs'])
            taskList = []
            linkList = []
            taskid = 0
            linkid = 0
            typeCount = 0
            typeList = []
            outdir = self.filename + "_"+layerinfor[0][' NumPEs']

            if(not os.path.exists(outdir)):
                os.makedirs(outdir)
            
            count = 0
            taskBegin = 0
            count = count +1
            # print(onelayer)
            taskinfo = {'taskname':"t0_"+str(taskid),"type":str(typeCount)}
            memoryid = taskid
            
            taskList.append(taskinfo)
            taskid=taskid+1

            taskNow = []

            for i in range(1,numPE):
                taskinfo = {'taskname':"t0_"+str(taskid),"type":typeCount}
                taskList.append(taskinfo)
                taskNow.append(taskid)
                taskid=taskid+1

            typeList.append([typeCount,onelayer[' Runtime (Cycles)']])
            compType = typeCount
            typeCount = typeCount+1

            for i in range(0,len(taskNow)):
                linkinfo = {'linkname':"a0_"+str(linkid),"src":memoryid,"dst":taskNow[i],"type": typeCount}
                linkList.append(linkinfo)
                linkid = linkid + 1
            
            inputTotal =  int(onelayer[" input l2 read"]) + int(onelayer[" filter l2 read"]) + int(onelayer[" output l2 read"])
            needsend = int(inputTotal/numPE)
            typeList.append([typeCount,needsend])
            typeCount = typeCount+1

            clusterSize = int(nameMap[onelayer[" Layer Number"]])
            clusterNumber = int(numPE/clusterSize)

            outputTotal = int(onelayer[" input l2 write"]) + int(onelayer[" filter l2 write"]) + int(onelayer[" output l2 write"])
            needwrite = int(outputTotal/numPE)
            for j in range(0,clusterNumber):
                taskinfo = {'taskname':"t0_"+str(taskid),"type":compType}

                for i in range(1,clusterSize):
                    linkinfo = {'linkname':"a0_"+str(linkid),"src":j*clusterSize+i+taskBegin,"dst":taskid,"type": typeCount}
                    linkList.append(linkinfo)
                    linkid = linkid + 1

                taskList.append(taskinfo)
                taskid=taskid+1


          
            taskinfo = {'taskname':"t0_"+str(taskid),"type":compType}
            taskList.append(taskinfo)    

            for i in range(0,clusterNumber):
                linkinfo = {'linkname':"a0_"+str(linkid),"src":taskid-i-1,"dst":taskid,"type": typeCount}
                linkList.append(linkinfo)
                linkid = linkid + 1

            taskid=taskid+1    
            taskBegin = taskid
            typeList.append([typeCount,needwrite])
            typeCount = typeCount+1

            # linkinfo = {'linkname':"a0_"+str(linkid),"src":taskid-1,"dst":taskid,"type": typeCount}
            # linkList.append(linkinfo)
            # linkid = linkid + 1
            
            
        #     if(count==2):
        #         break
        #     # break
        # taskinfo = {'taskname':"t0_"+str(taskid),"type":typeCount}
        # taskList.append(taskinfo)
        # typeList.append([typeCount,1])


        # print("tasklist",taskList)
        # print("linkList",linkList)
        # print("typeList",typeList)

            resultFile = outdir+"/" + self.filename + onelayer[" Layer Number"] + '.tgff'
            file_object1 = open(resultFile,'w')

            file_object1.write("@HYPERPERIOD 9207\n\n")

            file_object1.write("@TASK_GRAPH 0 {\n")
            file_object1.write("    PERIOD 9207\n\n")

            for oneTask in taskList:
                a = "   TASK "+str(oneTask["taskname"])+"   "+"TYPE "+str(oneTask["type"])+"\n"
                file_object1.write(a)

            file_object1.write('\n')

            for onelink in linkList:
                a = "   ARC a0_" +str(onelink["linkname"])+"    FROM  t0_"+str(onelink["src"])+"  TO  t0_"+str(onelink["dst"])+" TYPE "+str(onelink["type"])+"\n"
                file_object1.write(a)

            file_object1.write("}\n")
            file_object1.write(str(len(layerinfor)))
            file_object1.write("#------------------------------------------------------------------------------\n")
            file_object1.write("# type  exec_time\n")
            for typeitem in typeList:
                a = "    "+str(typeitem[0])+"    "+str(typeitem[1])+"\n"
                file_object1.write(a)


    def folderprocess(self):
        g = os.walk(self.mapfolder)
        for path,dir_list,file_list in g:
            for file_name in file_list:
                self.filename = file_name.split(".")[0]
                fileMain = self.filename
                sizeList = ["_16","_64","_256"]
                mapfile = os.path.join(path,file_name)
                for item in sizeList:
                    taskfile = self.resultfolder+"/"+fileMain+item+".csv"
                    print(fileMain,mapfile,taskfile)
                    self.dataProcess(fileMain,mapfile,taskfile)




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

    #print('inputfile: ', inputfile)
    

    transdata = transData(inputfile)
    transdata.folderprocess()

    
if __name__ == "__main__":
    main(sys.argv[1:])
    