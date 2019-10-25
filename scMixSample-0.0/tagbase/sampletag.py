#!/usr/bin/env python3 
#-*-utf-8-*-



"""
use sample tag as query.fa to map tag fastq ,get the sample tag sequence 
use the sampletag sequece as base ,cell barcode sequece as query ,find the sample barcode 
use the sample barcode find sequcene 
"""

import configparser
import os,sys 
import subprocess
import re 


global configfile 
configfile = sys.path[0] + "/tagbase/config.ini"



#def getpara(configfile):
#    """
#    Input:config file for this pipeline
#    Output:None
#    读取配置文件中软件配置信息，用于后续使用
#    """
#    config = configparser.ConfigParser()
#    config.read(configfile)
#    print(config.sections())
#    print(sys.path[0])
#    bowtie = config.get("tool","bowtie")
#    iTools = config.get("tool","iTools")
#    abfq   = config.get("tool","Abstract_fq")


def read_fa(fasta):
    with open(fasta,'r') as f:
        seq_id = ""

        for line in f:
            if line.startswith(">"):
                if seq_id:
                    yield seq_id ,seq_seq
                seq_id = line.strip().split(" ")[0].lstrip(">")
                seq_seq = ""
            else:
                seq_seq += line.strip()
        yield seq_id ,seq_seq



def rc_seq(seq):
    base_pair = {"A":"T","C":"G","T":"A","G":"C","N":"N","a":"t","c":"g","t":"a","g":"c"}
    rc = ''.join(base_pair[base] for base in seq[::-1])
    return rc


def _maptag(query:str , fa:str ,path:str ,name:str) -> None:
    """
    Input:query sequence ,fa sequence 
    Output:None
    使用正则表达式方式匹配每个样品对应的tagsequence
    """
    queryseq =  query.strip()
    queryrc  = rc_seq(queryseq)
    m1       = re.compile(queryseq)
    m2       = re.compile(queryrc)
    with open(path +"/" + name +"_abstract.fa",'w') as fa1:
        for sid ,seq in read_fa(fa):
            if any([m1.search(seq) ,m2.search(seq)]):
                fa1.write(">" + sid + "\n" + seq + "\n")
            else:
                continue 
    if os.path.isfile(path +"/" + name +".fa"):
        return True
    else:
        return False      

def maptag(query:str , fqpath:str ,name:str ,path:str = "./")-> None:
    """
    Input:sample tag fa ,fastq seq 
    Output:None 
    Function:
    use different sample tag map sample tag fq,first build sample tag base
    get different sample tag sequence
    """
#    getpara(configfile)
    config = configparser.ConfigParser()
    config.read(configfile)
    bowtie = config.get("tool","bowtie")
    iTools = config.get("tool","iTools")
    abfq   = config.get("tool","Abstract_fq")
    sn = name 
    fq1 ,fq2 = fqpath + "/" + name  + "_tag_1_R1.fq.gz",fqpath + "/"+ name  + "_tag_1_R2.fq.gz"
    if not os.path.exists(fqpath + sn + ".fa"):
        cmd = f"""\
{iTools}  Formtools Fq2Fa -InFq {fq1} -OutPut {fqpath}{sn}_r1.fa 
{iTools}  Formtools Fq2Fa -InFq {fq2} -OutPut {fqpath}{sn}_r2.fa
zcat {fqpath}{sn}_r1.fa {fqpath}{sn}_r2.fa >{fqpath}{sn}.fa 
    """
        with open(path + "/tagmap.sh",'w') as f:
            f.write(cmd)
        cmd1 = f"/bin/bash {path}/tagmap.sh 2>error.log" 
        fa2 = path + "/" + sn + ".fa"
        wait = subprocess.call(cmd1 ,shell = True)
        if wait == 0:
            if _maptag(query ,  fa2 , path , name):
                pass 
            else:
                raise("Error , not query map not complete")
        else:    
            raise("runError,sample tag not complete")
    else:
        fa2 = path + "/" + sn + ".fa"
        if _maptag(query ,  fa2 , path , name):
            pass
        else:
            raise("Error , not query map not complete")
    

