import os
import sys
import getopt

def processorFolder(path):
    fileList = os.listdir(path)
    outpath = path+"_result"
    if(os.path.exists(outpath)):
        print("outpath exists")
    else:
        os.system("mkdir "+outpath)
        print("make dir outpath")
    for file in fileList:
        namelist = file.split('_')
    
        newName = namelist[0:3]
        temp = namelist[1].split('x')
        size = temp[1]
        
        inputdir = path +"/" + file

        outputname = newName[0]+"_"+newName[1]+"_"+newName[2]+"_"+"xy.json"
        outputdir = outpath + "/" + outputname
        command = "python3 RoutingAlgorithmXY.py -i "+inputdir+" -o "+outputdir+" -r "+str(size)
        os.system(command)
        
        outputname = newName[0]+"_"+newName[1]+"_"+newName[2]+"_"+"ra1.json"
        outputdir = outpath + "/" + outputname
        command = "python3 RoutingAlgorithm1.py -i "+inputdir+" -o "+outputdir+" -r "+str(size)
        os.system(command)
        outputname = newName[0]+"_"+newName[1]+"_"+newName[2]+"_"+"ra2.json"
        outputdir = outpath + "/" + outputname
        command = "python3 RoutingAlgorithm2.py -i "+inputdir+" -o "+outputdir+" -r "+str(size)
        #print(command)
        os.system(command)
        #outputname = newName[0]+"_"+newName[1]+"_"+newName[2]+"_"+newName[3]
        #outputdir = outpath + "/" + outputname
        # command = "python3 OnlineCompute1.py -i "+inputdir+" -r "+str(size)
        # #print(command)
        # os.system(command)

        
         
        #os.system('ls')


def main(argv):
    inputfile = ''
    saveflag = 1
    unit = 1
    size = 8
    taskMax = 500

    try:
        opts, args = getopt.getopt(argv,"hi:u:s:",["ifile=","size=","unit="])
    except getopt.GetoptError:
        print('Error run_folder.py -i <inputfile> -s <size> -u <unit>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run_folder.py -i <folder> -s <size> -u <unit>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            print("read input file")
            inputfile = arg
        elif opt in ("-u", "--unit"):
            unit = int(arg)
        elif opt in ("-s", "--size"):
            size = int(arg)
        # elif opt in ("-u", "--unit"):
        #     unit = int(arg)


    print('inputfile: ', inputfile)
    print('saveflag: ', saveflag)
    print('unit: ',unit)
    print('size: ',size)
    processorFolder(inputfile)


if __name__ == "__main__":
    main(sys.argv[1:])