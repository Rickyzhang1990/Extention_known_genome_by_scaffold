import sys,os

sys.path.append('path')

import kaka_module as kaka 

def find_best(out):
	out_dic = kaka.fa_dic(out)
	a_r = {}
	for path in out_dic.keys():
		if path.endswith("-"):
			print path 
		relate = path.strip(">").split("->")
		if relate[0].startswith("FN"):
#			a_r[path[0]] = {'tail':path[1] + ":" + path[2]}
			a_r[relate[0]] = {}
			if 'tail' not in a_r[relate[0]]:
				a_r[relate[0]] = {'tail':path}
			else:
				len1 = len(out_dic[path])
				len2 = len(out_dic[a_r[relate[0]['tail']]])
				if len1 > len2:
					a_r[relate[0]] = {'tail':path}
				else:	continue
		else:
			a_r[relate[1]] = {}
			if 'head' not in a_r[relate[1]]:
				a_r[relate[1]] = {'head':path}
			else:
					len1 = len(out_dic[path])
					len2 = len(out_dic[a_r[relate[1]['head']]])
					if len1 > len2:
						a_r[relate[1]] = {'head':path}
					else:	continue
	return a_r

def get_fa(a_r, genome, tenx_fa, outfa):
	with open(outfa, 'w') as fa:
		ge_dic = kaka.fa_dic(genome)
		tenx = kaka.fa_dic(tenx_fa)
		for x,y in a_r.items():
			if len(y) == 2 :
				head_path = y['head'].strip(">")
				head_id = head_path.split('->')[0].split('(')[0]
				head_index = int(head_path.split('->')[0].split('(')[1].strip(')').split(':')[1])
				tail_path = y['tail'].strip(">")
				tail_id = tail_path.split('->')[1].split('(')[0]
				tail_index = int(tail_path.split('->')[1].split("(")[1].strip(":)"))
				final_path = head_path.split('->')[0] + head_path.split('->')[1] + tail_path.split('->')[1]
				final_seq = tenx[head_id][:head_index] + ge_dic[head_path.split('->')[1]] + tenx[tail_id][tail_index:]
				fa.write('>'+final_path + '\n' + final_seq + '\n')
			else:
				if 'head' in y:
					head_path = y['head'].strip(">")
					genome_id = head_path.split("->")[1]
					tenid = head_path.split("->")[0].split('(')[0]
					ten_index = int(head_path.split("->")[0].split('(')[1].strip(")").split(":")[1])
					final_seq = tenx[tenid][:ten_index] +  ge_dic[genome_id]
					fa.write(">"+ genome_id + '\n' + final_seq + '\n')
				else:
					tail_path = y['tail'].strip(">")
					genome_id = tail_path.split('->')[0]
					tenid = tail_path.split('->')[1].split("(")[0]
					ten_index = int(tail_path.split('->')[1].split("(")[1].split(":")[0])
					final_seq = ge_dic[genome_id] + tenx[tenid][ten_index:]
					fa.write(">" + genome_id + '\n' + final_seq + '\n')


if __name__ == "__main__":
	relate_dic = find_best(sys.argv[1])
	get_fa(relate_dic , sys.argv[2],sys.argv[3],sys.argv[4])
