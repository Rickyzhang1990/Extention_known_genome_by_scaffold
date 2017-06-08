#!/usr/bin/env python
#coding = utf-8

import os,sys
sys.path.append('/lustre/work/chaozhang/scripts/useful_tools')
import kaka_module as kaka
import json
from collections import defaultdict

#def find_related(pslfile):
#with open(pslfile,'r') as m:
##related_set = {}
##for eachline in m:
###each = eachline.strip().split('\t')
###if each[13] in related_set:
####continue 
###else:
####related_set[each[13]]= {}
###if (each[9].endswith('head') and  
###each[11] == "0" and 
###each[16] == each[14]):
####genome_candinite =  each[9].split("_")[0]+":"+str(each[12])
####tenxcandinite =  each[13] + ':' + str(each[16])
####strand = each[8].strip()
####if not 'head' in related_set[each[13]]:
#####related_set[each[13]]['head'] = [tenxcandinite  + '->' + genome_candinite + "->" + strand]
####else:
#####related_set[each[13]]['head'].append(tenxcandinite  + '->' + genome_candinite + "->" + strand)
###elif (each[9].endswith("tail") and 
###each[12] == each[10] and 
###each[15] == "0"):
####genome_candinite = each[9].split("_")[0] + ":" + str(each[12])
####tenxcandinite = each[13].strip() + ":" + str(each[16])
####stand = each[8].strip()
####if not 'tail'  in related_set[each[13]]:
#####related_set[each[13]]['tail']= [genome_candinite  + '->' + tenxcandinite + "->" + strand]
####else:
#####related_set[each[13]]['tail'].append(genome_candinite  + '->' + tenxcandinite + "->" + strand)
###with open("related_set.json",'w') as json_file:
####json.dumps(related_set , json_file)
#return related_set 

def connect_seq(genome,tenxseq,related_set,first_fa):
#	tenxsequence = kaka.read_fasta(tenxseq)
#	tenxdic = {}
#	for each in tenxsequence:
#		id = each[0].strip()
#		seq = each[1].strip()
#	genome_seq = kaka.read_fasta(genome)
#	genome_dic = {}
#	for eachseq in genome_seq:
#		g_id = eachseq[0].strip()
#		g_seq = eachseq[1].strip()
#		genome_dic[g_id] = g_seq
#	genome_dic = kaka.fa_dic(genome)
#	tenxdic = kaka.fa_dic(tenxseq)
	with open(first_fa,'w') as fa_file:
		for id,st in related_set.iteritems():
			if len(st) == 2:
				left_path = st['tail']  
				right_path = st['head'] #if st.has_key('head') else continue 
				all_path=[x +'->' + y for x in left_path for y in right_path]
				for paths in all_path:
					paths = paths.split('->')
					f_sc_id = paths[0].split(":")[0]    #former scaffold if 
#					f_sc_si = int(paths[0].split(":")[1]) #former scaffold sequence index 
					tenxid = paths[1].split(":")[0]       # 10x scaffold id 
					t_f_i = int(paths[1].split(":")[1])   # 10x former seq idex
					t_l_i = int(paths[3].split(":")[1])   # 10x latter seq index 
					l_sc_id = paths[4].split(':')[0]      #latter genome scaffold index 
#					l_sc_si = int(paths[4].split(":")[1])
					if paths[2] == "+" and paths[5] == "+":
						final_id = "->".join([f_sc_id,tenxid +"("+ str(t_f_i) +":"+ str(t_l_i) + ")"  ,l_sc_id,"+:+"])
#						final_seq = genome_dic[f_sc_id] + tenxdic[tenxid][t_f_i:t_l_i] + genome_dic[l_sc_id]
					elif paths[2] == "-" and paths[5] == "-":
						final_id = "->".join([f_sc_id,tenxid + "("+ str(t_f_i) + ":" + str(t_l_i) +")" ,l_sc_id,"-:-"])
#						final_seq = genome_dic[f_sc_id] + kaka_c_seq(tenxdic[tenxid][t_f_i:t_l_i]) + genome_dic[l_sc_id]
					elif paths[2] == "+" and paths[5] == "-":
						final_id = "->".join([f_sc_id,tenxid + "(" + str(t_f_i) + ":" + str(t_l_i) + ")",l_sc_id,"+:-"])
#						final_seq = genome_dic[f_sc_id][:f_sc_si] + tenxdic[tenxid][t_f_i:t_l_i] + kaka.c_seq(genome_dic[l_sc_id])
					elif paths[2] == "-" and paths[5] == "+":
						final_id = "->".join([f_sc_id,tenxid + "(" + str(t_f_i) + ":" + str(t_l_i) + ")",l_sc_id,"-:+"])
#						final_seq = genome_dic[f_sc_id][:f_sc_si] + kaka.c_seq(tenxdic[tenxid][t_f_i:t_l_i]) + kaka.c_seq(genome_dic[l_sc_id])
					fa_file.write(">"+final_id + '\n' )#+ final_seq +'\n')
#					del genome_dic[f_sc_id],genome_dic[l_sc_id]
			else:
				if st.has_key('head'):
					for path in st['head']:
						path = path.strip().split('->')
						tenid = path[0].split(":")[0]
						l_sc_id = path[1].split(":")[0]
						tenindex = path[0].split(":")[1]
						if path[2] == "+":
							final_id = "->".join([tenid +"(0:"+ str(tenindex) + ")",l_sc_id,":+"])
#							final_seq = tenxdic[tenid][:int(tenindex)] + genome_dic[l_sc_id]
						else:
							final_id = "->".join([tenid + "(0:" + str(tenindex) + ")",l_sc_id,":-"])
#							final_seq = kaka.c_seq(tenxdic[tenid][:int(tenindex)]) + genome_dic[l_sc_id]
						fa_file.write(">" + final_id +'\n')# + final_seq +'\n')
#						del genome_dic[l_sc_id]
				elif st.has_key('tail'):
					for path in st['tail']:
						path = path.strip().split('->')
						tenid = path[1].split(":")[0]
						tenindex = path[1].split(":")[1]
						f_sc_id = path[0].split(":")[0]
						if path[2] == "+":
							final_id = "->".join([f_sc_id,tenid + "(" + str(tenindex) + ":)",":+"])
#							final_seq = genome_dic[f_sc_id] + tenxdic[tenid][int(tenindex):]
						else:
							final_id = "->".join([f_sc_id,tenid + "(" + str(tenindex) + ":)",":-"])
#							final_seq = genome_dic[f_sc_id] + kaka.c_seq(tenxdic[tenid][int(tenindex):])
#						del genome_dic[f_sc_id]
					fa_file.write(">" + final_id + '\n')#+ final_seq +'\n'))
#	with open('dealed_genome.fa','w') as genome:
#		for i,j in genome_dic.iteritems():
#			genome.write(">" + i +'\n' + j + '\n')
#	for id , seq in genome_dic.iteritems():
#		with open("remove.genome.fa",'w') as genome:
#			genome.write(">"+id +'\n' + seq +'\n/)

def remove_scaffold(genome , outfa):
	fa_dic = kaka.fa_dic(genome)
	out_dic = kaka.fa_dic(outfa)
	genome_list = []
	for id in out_dic.keys():
		id = id.split("->")
		for x in id:
			if x.startswith("FN"):
				genome_list.append(x.split(":")[0])
#	for y in set(genome_list):
#		if y in fa_dic:
#			del fa_dic[y]
	leftover = set(fa_dic.keys()) - set(genome_list)

	with open("remove.fa",'w') as genome:
		for lid in leftover:
			genome.write(">" + lid +'\n' + fa_dic[lid] +'\n')







#def evalute_seq(fa_seq):
if __name__ == "__main__":
	import find_relate_less as fr
	relate_set = fr.find_related(sys.argv[1])
	with open("related_set.json",'w') as json_file:
		json.dump(relate_set , json_file)
	connect_seq(sys.argv[2],sys.argv[3],relate_set,sys.argv[4])
#	remove_scaffold(sys.argv[2],sys.argv[4])


