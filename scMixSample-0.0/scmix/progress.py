#!/usr/bin/env python 
#-*-utf-8-*- 


import click 
import os,sys 

@click.group()
def cli():
    pass


##样本sample tag比对到标签文库序列中，得到每个样品的sample tag序列
@click.command()
@click.option('--tag', help ='the query fa of sample tag ,formart "fa"' , required=True ,type = str)
@click.option("--fqpath",  help ="the sample tag fastq seq of the project", required = True ,type = str)
@click.option("--name",help = "the name of your sample ",required = True,type = str)
@click.option("--path", help = "the work derectory of your ",default = "./")

def tagmap(tag , fqpath ,name ,path):
    from tagbase  import sampletag
    sampletag.maptag(tag , fqpath ,name , path)


##通过第一步得到sampletag序列后，提取原始数据R1前16bp作为barocode 比对sampletag序列，得到每个样品的原始数据
@click.command()
@click.option("--base" ,  help = "the sample tag base to align",required = True )
@click.option("--fqpath", help = "the fastq path of your raw data",required = True)
@click.option("--workdir",help = "the work dir and output path for the project",default = os.path.abspath("./"))
@click.option("--name",   help = "the sample name of fastq ,for detection of fastq name" ,required = True)
@click.option("--mis",help = "the work dir and output path for the project",default =  0 ,type = int)


def abstractfq(base ,fqpath , workdir ,name):
    from tagbase  import tag2seq
    fqpath = fqpath if fqpath.endswith("/") else fqpath + "/"  
    fqlist = [(fqpath + name + "_" + str(i) + "_R1.fq.gz" ,fqpath + name + "_" + str(i) + "_R2.fq.gz") for i in range(1,5)]
    fafilelist  = []
    fq1list = [fqpath + name + "_" + str(i) + "_R1.fq.gz"   for i in range(1,5)]
    for fq1 in fq1list:
        fafile = tag2seq.cutread(fq1 ,workdir)
        if os.path.isfile(fafile):
            fafilelist.append(fafile)
        else:
            print("file not create properly ,break")
            exit(1)    
    tag2seq.mulimap2seq(base , fafilelist , fqlist , workdir ,mis)


## 预留功能，统计每个样品的barcode
@click.command()
@click.option("--base", help = "the sample tag base to align" ,required = True)
@click.option("--name",   help = "the sample name of fastq ,for detection of fastq name" ,required = True)
@click.option("--barcode", help = "10xgenomics barcode whitelist " ,required = True)
@click.option("--workdir",help = "the work dir and output path for the project",default = os.path.abspath("./"))
@click.option("--mis",help = "the work dir and output path for the project",default =  0 ,type = int)


def countbar(base , barcode , workdir , name ,mis):
    from tagbase import countbarcode 
    countbarcode.bar2tag(base , barcode , workdir , name ,mis)

cli.add_command(tagmap)
cli.add_command(abstractfq)
cli.add_command(countbar)


def main():
    cli()

if __name__ == "__main__":
    main()
