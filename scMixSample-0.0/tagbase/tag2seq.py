#!/usr/bin/env python3
#-*-utf-8-*-

import subprocess 
import os,sys 
from  multiprocessing import Pool 
import configparser
import gzip 



global configfile 
configfile = sys.path[0]+ "/tagbase/config.ini"

def buildindex(bowtie:str , base:str)->0:
    """
    建立基因组比对索引
    输入：bowtie比对工具，参考基因组
    输出：无输出
    """
    os.system(f"{bowtie}-build {base} {base}")
    pass 
def read_fq(fastq):
    """
    read iter read fq file
    """
    fq = gzip.open(fastq,'rb') if fastq.endswith('.gz') else open(fastq,'r')
    count = 0
    for line in fq:
        line = line.decode()
        count += 1
        if count % 4  is 1 :
            seq_id = line.strip()
            seq_seq = line
        elif count % 4 is 0 :
            seq_seq += line
            seq = (seq_id ,seq_seq)
            yield seq
        else:
            seq_seq += line
    yield seq_id ,seq_seq
    fq.close()

def cutread(fq:str ,path:str)->str:
    """
    Input:fq1 of candinate read
    Output:16th base of r1 read ,on behalf of barcode
    read1的前16bp代表10xgenomics的cell barcode序列,提取前16bp比对sampletag seq
    可以获得每个样品对应的reads序列
    """
    basename = os.path.basename(fq).split(".fq")[0]
    with open(path + "/" + basename + ".fa",'w') as fa1:
        for sid ,seq in read_fq(fq):
            sid = sid.lstrip("@")
            sequence = seq.split("\n")[1]
            barcodeseq = sequence[:16]
            fa1.write(">" + sid  + "\n" + barcodeseq  + "\n")

    return  path+"/"+ basename+".fa"



def map2tagseq(base:str , fafile:str ,fq:str ,path:str = "" , mis:int = 0)-> None:
    """
    use fisrt 16bp.fa map to sampletag seq ,get the sampletag reads name 
    Input:16bp.fa ,tagseq base 
    output:map status file 
    """
    config = configparser.ConfigParser()
    config.read(configfile)
    bowtie = config.get("tool","bowtie")
    iTools = config.get("tool","iTools")
    abfq   = config.get("tool","Abstract_fq")
    fq1 = fq[0] 
    fq2 = fq[1]
    sn = os.path.basename(fafile).split(".")[0]
    cmd = f"""\
{bowtie} -f -a -v {mis} --al {path}/{sn}_map  --un {path}/{sn}_unmap  {base}   {fafile}   {path}/{sn}_map.txt
{abfq} -InFq1 {fq1}  -adapter1 {path}/{sn}_map.txt -InFq2 {fq2} -adapter2 {path}/{sn}_map.txt -outdir {path}
"""
    with open(path + f"/fq2{sn}.sh",'w') as f1:
        f1.write(cmd)
    cmd1 = f"/bin/bash  {path}/fq2{sn}.sh  2>error.log"
    wait = subprocess.call(cmd1,shell = True)
    if wait == 0: pass
    else:    raise("runError,sample tag not complete")



def mulimap2seq(base:str , falist:list ,fqlist ,path:str = "" ,mis:int = 0) -> None:
    """
    multi version of map2tagseq function
    """
    pool = Pool(len(falist))
#    print(falist)    debug
#    print(fqlist)    debug 
#    exit()           debug
    config = configparser.ConfigParser()
    config.read(configfile)
    bowtie = config.get("tool","bowtie")
    buildindex(bowtie , base)
    assert len(falist) == len(fqlist)
    for i  in range(len(falist)):
        fa = falist[i]
        fq = fqlist[i]
        pool.apply_async(map2tagseq,(base ,fa ,fq , path ,mis))

    pool.close()
    pool.join()
    print("done")


