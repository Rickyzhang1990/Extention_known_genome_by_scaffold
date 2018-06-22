#!/usr/bin/env python 
#-*-coding:utf-8-*-

import os,sys 

'''
采用了新的思路，利用gene以及ncRNA的起始位置进行排序，同一scaffold上的按照位置进行排序
，最后得到排序后的列表后在一一写出，得到最终的排序后的结果。
'''

def getGene(gff3):
	gene_line = []
	with open(gff3,'r') as gff_file:
		for line in gff_file:
			line = line.strip()
			new_line = line.split("\t")
			if new_line[2] == "gene":
				if gene_line:
					yield  gene_line
					gene_line = []
					gene_line.append(line)
				else:
					gene_line.append(line)
			else:
				gene_line.append(line)
		yield gene_line
		



if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "Usage:\n python %s gene.gff3 ncRNA.gff3 out.gff3"%sys.argv[0]
		exit(1)



	gff = sys.argv[1].strip()
	nc = sys.argv[2].strip()
	out = sys.argv[3].strip()
	scaffold = {}	


	with open(nc,'r') as ncre:
		for each in ncre:
			each_new = each.strip().split("\t")
			nc_s ,s_id  = int(each_new[3]),each_new[0]
			if s_id not in scaffold:
				scaffold[s_id] = [(nc_s , each)]
			else:	
				scaffold[s_id].append((nc_s,each))
				
# 将基因信息也存入到scaffold的字典内
	for x in getGene(gff):
		line0 = x[0].split("\t")
		g_s ,s_id = int(line0[3]),line0[0]
		g_info = (g_s , x )
		if s_id in scaffold:
			scaffold[s_id].append(g_info)
		else:
			scaffold[s_id] = [g_info]
	
#操作字典，对字典按照第一个元素进行排序，并将排序后的第二个元素输出
	with open(out , 'w') as new_gff:
		for sid ,value in scaffold.iteritems():
			new_scaf = sorted(value , key = lambda x:x[0] , reverse=False)
			for x in new_scaf:
				if isinstance(x[1], str):
					new_gff.write(x[1])
				else:
					new_gff.write("\n".join(x[1]) + '\n')

print "ok"
