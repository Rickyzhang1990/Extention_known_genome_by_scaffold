#!/usr/bin/env python
import os,sys
sys.path.append('path')
import kaka_module as kaka 

def  get_head_tail(fasta,out,per = 0.3):
    seq = kaka.read_fasta(fasta)
    with open(out,'w') as f:
        for x in seq:
            id = x[0].strip()
            if len(x[1]) >= 2000:
                head_seq = x[1][:200]
                tail_seq = x[1][-200:]
            else:
                head = int(len(x[1])*float(per))
                tail = int(len(x[1])*(1-float(per)))
                head_seq = x[1][:head]
                tail_seq = x[1][tail:len(x[1])]
            head_fa = id+"_head"+'\n'+head_seq+'\n'
            tail_fa = id+"_tail" + '\n' +tail_seq +'\n'
            f.write(head_fa+tail_fa)
if __name__ == "__main__":
    get_head_tail(sys.argv[1],sys.argv[2],sys.argv[3])
