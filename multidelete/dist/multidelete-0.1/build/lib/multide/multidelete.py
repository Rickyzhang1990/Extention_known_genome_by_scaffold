#!/usr/bin/env python 
#coding=utf-8

import os,sys 
import time 
from multiprocessing import cpu_count,Pool 
import time 

def getallfile(path):
    """
    利用递归遍历文件夹内所有的文件
    Input:待筛除的文件夹
    Return:所有文件夹的列表
    """
    path = os.path.abspath(path)
    allfilelist=os.listdir(path)
    allfile = [path + "/" + x for x in allfilelist]
#    for files in allfilelist:
#        filepath=os.path.join(path,files)
#        #判断是不是文件夹
#        if os.path.isdir(filepath):
#            getallfile(filepath)
#        allfile.append(filepath)
    return allfile


def delete(files):
    """
    Input:file
    return：None
    """
    os.system("rm -r %s"%files)


#@click.command()
#@click.option('--fold',help = "the fold to be delete ",type=str)
def main():

    start = time.time()
    fold = sys.argv[1]
    alllist = getallfile(fold)
    if len(alllist) > 4*cpu_count():
        cpun = cpu_count() -5 
    elif  cpu_count() <= len(alllist) < 2*cpu_count():
        cpun = int(cpu_count()/2)
    else:
        cpun = 3 
    pool = Pool(cpun)
    for files in alllist:
        pool.apply_async(delete,(files,)) 

    pool.close() 
    pool.join()
    end = time.time()
    print("Total time : %s s"%( end - start))
    print("done")


#if __name__ == "__main__":
#    main()
