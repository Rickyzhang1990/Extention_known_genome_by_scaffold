#!/usr/bin/env python 
#coding = utf-8

import gzip 
import os,sys
import subprocess

def Bam2Fq(bamfile ,path ,sample ,method = '1', count = 10):
    sample_name = os.path.basename(bam)[:-4]
    if bam.endswith(".bam"):
        smd = os.popen('which samtools').read().strip()
        cmd = smd + " view  " + bam +" > "+sample_name +".sam"
        x = subprocess.call(cmd ,
                            shell = True,
                            stdin=None, stdout=None, stderr=None)
        if x == 0:  pass
#    sample_name = os.path.basename(bam)[:-4]
    m_dic = {'1':'assemble','2':'fragscaff' }
    samfile = open(sample_name+".sam",'r')
    read1 = gzip.open(path + '/%s_S1_L001_R1_000.fastq.gz'%sample,'wb')
    read2 = gzip.open(path + '/%s_S1_L001_R2_000.fastq.gz'%sample,'wb')
    b_list = open(path + '/%s_barcode_list.txt'%sample,'w')
    try:
        barcode_read1 = {}
        barcode_read2 = {}
        select_barcode = []
        for line in samfile: 
            line = line.strip().split("\t")
            index = 'GCGATGTG'
            if line[14].startswith("RX:"):  continue
            elif line[16].startswith("BX:"):
                barcode = line[16].split(":")[-1].split("-")[0]
                if method is '1':
                    id = line[0].strip() +' 1:N:0:%s'%index
                    seq = line[16].split(":")[-1].split("-")[0] + line[14].split(":")[-1] + line[9].strip()
                    q = line[17].split(":")[-1].split("-")[0] + line[15].split(":")[-1] + line[10].strip() 
                else :
                    id = line[0].strip() + "#%s"%barcode
                    seq = line[9].strip()
                    q = line[10].strip()
                symbol = "+"
                seq = '\n'.join([id,seq,symbol,q])
                if barcode in barcode_read1:
                    barcode_read1[barcode].append(seq) 
                else:
                    if  barcode_read1:
                        for x ,y  in barcode_read1.items():
                            if 2*len(y) >= count:
                                select_barcode.append(x)
                                read1.write('\n'.join(y) + '\n')
                        barcode_read1.clear()
                        barcode_read1[barcode] = [seq]
                    else:
                        barcode_read1[barcode] = [seq]
            elif line[14].startswith("BX:"):
                barcode = line[14].split(":")[-1].split("-")[0]
                seq = line[9].strip()
                q = line[10].strip()
                if method is "1":
                    id =  line[0].strip() +' 2:N:0:%s'%index
                else:
                    id = line[0].strip() + "#%s"%barcode
                symbol = "+"
                seq = '\n'.join([id,seq,symbol,q])
                if barcode in barcode_read2:
                    barcode_read2[barcode].append(seq)
                else:
                    if barcode_read2:
                        for x2 in barcode_read2.values():
                            if 2*len(x2) >= count:
                                read2.write('\n'.join(x2) + '\n') 
                        barcode_read2.clear()
                        barcode_read2[barcode] = [seq]
                    else:
                        barcode_read2[barcode] = [seq]

    finally:
        b_list.write('\n'.join(select_barcode) + '\n')
        samfile.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = 'the option get programe',add_help = True )
    parser.add_argument('--bam', help = " the bam file to be deal,usually the longranger basic output file",required = True)
    parser.add_argument('--path', help = "the output path ,default = './",default = "./")
    parser.add_argument('--method',help = 'the use of output fastq,assemble or align,1 for 10x ,2 for fragscaff',choices = ['1','2'],required = True)
    parser.add_argument('--count', help = "the minus count of barcode count" ,default = 20)
    parser.add_argument('--sample',help = "the samplme name of your fastq",required = True)
    argv = vars(parser.parse_args())
    bam = argv['bam'].strip()
    path = argv['path'].strip()
    method = argv['method'].strip()
    assert  method in ['1','2']
    count = int(argv['count']) 
    sample = argv['sample'].strip()
    Bam2Fq(bam,path,sample,method,count)
