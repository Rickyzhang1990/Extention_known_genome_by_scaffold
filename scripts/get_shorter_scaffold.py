#!/usr/bin/env python 
#coding = utf-8

import os,sys

def get_seq(fasta):
	with open(fasta,'r') as f:
		s_c = 0 #s_c = seq condition for the start of file 
		for line in f:                               #逐行迭代读取文件（应对大文件）
			if line.startswith(">") and s_c == 0:    #文件开头读取第一个fasta
				seq_id = line.strip().split(" ")[0]
				s_c = 1
				seq_seq = ""
			elif not line.startswith(">") and s_c == 1: #读完第一行，读取第一个fasta的序列
				seq_seq += line.strip()
			elif  line.startswith(">") and s_c == 1:  #读到第二个fasta的ID
				seq = [seq_id,seq_seq]                #第一个fasta的id和seq 放到列表内
				yield seq                             #返回一个生成器
				seq_id = line.strip().split(" ")[0]   #第一个以后的fasta的ID
				seq_seq = ""                          #第一个以后的序列的序列文件

def get_len_cutoff(seq ,out, cutoff = 10000):         
	with open(out,'w') as outfile:
		for i in seq:
			if len(i[1]) <= cutoff:
				outfile.write(i[0]+'\n'+i[1]+'\n')
			else:	continue

if __name__ == "__main__":
	fasta_generator = get_seq(sys.argv[1])
	get_len_cutoff(fasta_generator ,sys.argv[2] , sys.argv[3])
