#!/usr/bin/python

__author__ = 'Mitul Patel'
__copyright__ = "Copyright 2016-17"
__license__ = "GPL"
__version__ = "v1.0"
__maintainer__ = "Mitul Patel"
__email__ = "mitul428@gmail.com"
__status__ = "Production"

# Imports

bExitForImportFailed=0
try:
    import sys
    from time import strftime
    import argparse
    from optparse import OptionParser, OptionGroup
    import copy
    import subprocess
    import os
    import shutil
    import time
    import fnmatch
    import platform
    import urllib
    from shutil import copyfile
    import zipfile
    import glob
    import csv
    from collections import OrderedDict
except Exception, e:
    print 'Basic imports failed!'
    print e
    bExitForImportFailed=1

################################################################################
# Color messages

class Highlighter:
    def __init__(self):
        self._msgTypes={'INF':'\033[0m',
                'IMP':'\033[1;32m',
                'DEV':'\033[1;34m',
                'ERR':'\033[1;31m',
                'WRN':'\033[1;33m'}
        self._reset='\033[0m'
        self._default='INF'
    def ColorMsg(self,msg,msgLevel='INF'):
        try:
            s=self._msgTypes[msgLevel]+msg+self._reset
        except:s=s=self._msgTypes[self._default]+msg+self._reset
        return s

def ColorOutput(msg,msgLevel='INF'):
    o=Highlighter()
    return o.ColorMsg(msg,msgLevel)

################################################################################
# Options

def getOptions():
    '''Retrieve the options passed from the command line'''

    usage = "usage: python metaPAGAP.py"
    version="demo "+__version__
    description=("metagenomics Pan Genome Analysis pipeline (demo) tool for generating core genome from multiple bacterial strains."+
                 "For bug reports, suggestions or questions mail to Mitul Patel: mitul428@gmail.com")
    parser = OptionParser(usage,version=version,description=description)
        # Parse the options
    return parser.parse_args()

def CheckRequirements():
    #debug
    sys.stdout.write(strftime("%H:%M:%S")+
                    ' Checking software requirements\n')
    sys.stdout.flush()

    # Check for BioPython
    try:import Bio
    except:
        sys.stderr.write(strftime("%H:%M:%S")+
                    ColorOutput(' ERROR: BioPython is missing!\n','ERR'))
        sys.stdout.flush()
        return 1
   # Check for Prokka, get_homologues, Mafft, AMAS, RaXML
    '''
    lex=['prokka', 'mafft', 'raxmlHPC', 'nw_display']
    for ex in lex:
        p = subprocess.Popen('which '+str(ex),shell=(sys.platform!="win32"),
                    stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
        out=p.communicate()

        if out[0]=='':
            sys.stderr.write(strftime("%H:%M:%S")+
                  ColorOutput(' ERROR: '+ex+' executable is missing or not reachable from this location!\n','ERR'))
            return 1
    '''
    return 0

def getdemopath():
    current_path = os.path.abspath(sys.argv[0])
    current_path = os.path.abspath(os.path.join(current_path, ".."))
    tmp_path = current_path
    demo_path = current_path
    last_tmp_path = tmp_path
    it_count = 0
    while len(tmp_path) > 1 and it_count < 20:
        it_count += 1
        current_dir = os.path.basename(tmp_path)
        current_path = os.path.abspath(os.path.join(tmp_path, ".."))
        sys.stdout.flush()
        
        if current_dir.startswith("demo"):
            demo_path = tmp_path + "/"
            break
        elif os.path.exists(current_path + "/demo/"):
            demo_path = current_path + "/demo/"
            break
        else:
            tmp_path = current_path
        if last_tmp_path == tmp_path or it_count == 20:
            print("Cannot determine demo path")
            exit()
    return demo_path;

def fetchDATA():
    step = 1
    file_path=os.path.abspath(os.curdir)

    # Message
    sys.stdout.write(strftime("%Y-%m-%d %H:%M:%S")+
        ColorOutput(' Downloading input files .....\n','IMP'))
    sys.stdout.flush()

    t0_time = time.time()
    if len(os.listdir(file_path)) > 0:
        unzip("master.zip", file_path)
        #print "already exist"https://github.com/mitul-patel/test/archive/master.zip
        pass
        #if (urllib.urlretrieve("https://github.com/mitul-patel/data/archive/master.zip", "master.zip")):
    elif (urllib.urlretrieve("https://github.com/mitul-patel/data/archive/master.zip", "master.zip")): 
        unzip("master.zip", file_path)
       #urllib.urlretrieve('https://jjcloud.app.box.com/s/rw0v7r6thtv6efsfs2ekp8gontaw7quf', 'test-contigs.zip')
    t1_time = time.time()
    print(t1_time - t0_time, "Download..........DONE")
    #urllib.urlretrieve("https://github.com/marekborowiec/AMAS/archive/master.zip", "master.zip")
    return step

def unzip(zipFilePath, destDir):

    # Message
    sys.stdout.write(strftime("%Y-%m-%d %H:%M:%S")+
        ColorOutput(' Extracting files for zip folder .....\n','IMP'))
    sys.stdout.flush()

    zfile = zipfile.ZipFile(zipFilePath)
    for name in zfile.namelist():
        (dirName, fileName) = os.path.split(name)
        # Check if the directory exisits
        newDir = destDir + '/' + dirName
        if not os.path.exists(newDir):
            os.mkdir(newDir)
        if not fileName == '':
            # file
            fd = open(destDir + '/' + name, 'wb')
            fd.write(zfile.read(name))
            fd.close()
    zfile.close()

def bbstats():
    step = 3

    # Message
    sys.stdout.write(strftime("%Y-%m-%d %H:%M:%S")+
        ColorOutput(' Assembly statistics .....\n','IMP'))
    sys.stdout.flush()

    bbmap_path=os.path.abspath("/demo/bbmap/")
    data_path=os.path.abspath("/demo")
    out_path=os.path.abspath("/demo")
    files = os.listdir(data_path)
        
    t0_time = time.time()

    if len(os.listdir(out_path)) == len(files):
        pass
    else:     
        for i in files:
            if file.endswith('.fna'):
                sample = i.split('-')[0]
                cmd = '/demo/bbmap/stats.sh %s/%s > %s/%s.stat' % (data_path, i, data_path, sample)
                if os.system(cmd):exit()

    t1_time = time.time()
    print(t1_time - t0_time, "Assembly stats..........DONE")

    return step


run_path = os.path.abspath(os.curdir)
demo_path = getdemopath()
os.chdir(demo_path)

def main():
    os.chdir(run_path)
    #plat=platform.system()
    #step = 1
    
    # Message
    sys.stdout.write(strftime("%Y-%m-%d %H:%M:%S")+
            ColorOutput(' Starting Demo\n','IMP'))
    sys.stdout.flush()

    if bExitForImportFailed:
        pass
    elif CheckRequirements():
        PrintRequirements()
        sys.stdout.write(strftime("%Y-%m-%d %H:%M:%S")+
                            ColorOutput(' Stopping Demo\n','WRN'))
        sys.stdout.flush()
        sys.exit(1)
    else:
        for step in range(1,3):
            if step == 1:
                stepCOM=fetchDATA()
            elif step == 2:
                stepCOM=bbstats()      
            
    # Message
    sys.stdout.write(strftime("%Y-%m-%d %H:%M:%S")+
        ColorOutput(' Finished Demo\n','IMP'))
    sys.stdout.flush()
    sys.exit(1)

if __name__ == '__main__':
    main()
