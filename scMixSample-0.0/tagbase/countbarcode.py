#!/usr/bin/env python3 
#-*-utf-8-*-


import os,sys 
import configparser
import subprocess 


global configfile
configfile = sys.path[0]+ "/tagbase/config.ini"

def bar2tag(base:str , bar:str ,rpath:str ,sn:str , mis:int=0)->None:
    """
    Input:base and barcode seq 
    Output:None 
    """
    config = configparser.ConfigParser()
    config.read(configfile)
    bowtie = config.get("tool","bowtie")
    cmd = f"{bowtie} -f -a -v {mis} --al {rpath}/{sn}_map  --un {rpath}/{sn}_unmap  {base}   {bar}   {rpath}/{sn}_map.txt"
    path1 = os.path.abspath(base)
    suffix = [".1.ebwt",".2.ebwt",".3.ebwt" ,".4.ebwt",".rev.1.ebwt",".rev.2.ebwt"]
    boollist = []

    for x in suffix:
        indexfile = path1 + x 
        boollist.append(os.path.isfile(indexfile))
    if all(boollist):
        wait = subprocess.call(cmd ,shell = True)
        if wait == 0: pass 
        else:    raise("Error , map not completed")
    else:
        print("fa index not build ,please run \"bowtie-build {base} {base}\"first")
        exit(127)
