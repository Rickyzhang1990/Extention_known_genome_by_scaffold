# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


description = \
"""
1-Description of psl ,the format of psl file:
2-matches - Number of bases that match that aren't repeats
3-misMatches - Number of bases that don't match
4-repMatches - Number of bases that match but are part of repeats
5-nCount - Number of 'N' bases
6-qNumInsert - Number of inserts in query
7-qBaseInsert - Number of bases inserted in query
8-tNumInsert - Number of inserts in target
9-tBaseInsert - Number of bases inserted in target
10-strand - '+' or '-' for query strand. For translated alignments, second '+'or '-' is for genomic strand
11-qName - Query sequence name
12-qSize - Query sequence size
13-qStart - Alignment start position in query
14-qEnd - Alignment end position in query
15-tName - Target sequence name
16-tSize - Target sequence size
17-tStart - Alignment start position in target
18-tEnd - Alignment end position in target
19-blockCount - Number of blocks in the alignment (a block contains no gaps)
20-blockSizes - Comma-separated list of sizes of each block
21-qStarts - Comma-separated list of starting positions of each block in query
22-tStarts - Comma-separated list of starting positions of each block in target
"""

import json 
import sys,os
def find_related(pslfile):
    with open(pslfile,'r') as m:
        related_set = {}
        for eachline in m:
            each = eachline.strip().split('\t')
            if each[13] in related_set: pass
            else:
                related_set[each[13]] = {}
            if (each[9].endswith('head') and each[11] == "0" and each[16] == each[14]):
                genome_candinite =  each[9].split("_")[0]+":"+str(each[11])
                tenxcandinite =  each[13] + ':' + str(each[15])
                strand = each[8].strip()
                if not 'head' in related_set[each[13]]:
                    related_set[each[13]]['head'] = [tenxcandinite  + '->' + genome_candinite + "->" + strand]
                else:
                    related_set[each[13]]['head'].append(tenxcandinite  + '->' + genome_candinite + "->" + strand)
            elif (each[9].endswith("tail") and each[12] == each[10] and each[15] == "0"):
                genome_candinite = each[9].split("_")[0] + ":" + str(each[12])
                tenxcandinite = each[13].strip() + ":" + str(each[16])
                stand = each[8].strip()
                if not 'tail'  in related_set[each[13]]:
                    related_set[each[13]]['tail']= [genome_candinite  + '->' + tenxcandinite + "->" + strand]
                else:
                    related_set[each[13]]['tail'].append(genome_candinite  + '->' + tenxcandinite + "->" + strand)
            else:
                del related_set[each[13]]
#        with open("related_set.json",'w') as json_file:
#            json.dumps(related_set , json_file)
    return related_set

if __name__ == "__main__":
	relate = find_related(sys.argv[1])
	with open('related_1.json','w') as json_file:
	    json.dump(relate,json_file)
