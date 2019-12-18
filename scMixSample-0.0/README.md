本工具用于处理混样测序文库构建的样品reads拆分流程，可以用于拆分混样测序不同样本的reads

# 安装方法   
解压该工具包压缩文件，在包中存在setup.py，使用以下命令可以完成  
python  setup.py  install     
完成安装即可将该包安装到我们的python环境中

**使用该流程前需要完善位于tagbase目录下的config.ini文件，填写自己环境下可用相关软件**
# 分析流程
## step1   
得到每个样品的sampletag序列，将sampletag序列比对到测得的标签文库上，得到每个样品的sampletag sequence 
mixsample  tagmap  --tag AATTCGTACTAT   --fqpath /mnt/rorke/work/chaozhang/singlecell/testmixpipeline/tagseq   --name qinbobiaoqianwenku --path /mnt/rorke/work/chaozhang/singlecell/testmixpipeline  
tag:样本的tag标签序列，会使用该tag序列正向和反向互补序列进行tag匹配，获得匹配到该样品的tag sequence 
fqpath&name:样本标签文库存放的路径&文库文件的名字，要求样本存放形式如下
qinbobiaoqianwenku_tag_1_R1.fq.gz  
qinbobiaoqianwenku_tag_1_R2.fq.gz   
即{文库名字}_tag_1_R1.fq.gz   {文库名字}_tag_1_R2.fq.gz 

## step2   
得到样本的sampletag sequence后，可以直接提取R1前16bp作为barcode seq去比对，或者每个样本对应的readID ,根据fq文件的readid拆分不同样本的数据。  
`mixsample abstractfq --base /mnt/rorke/work/chaozhang/singlecell/testmixpipeline/qinbobiaoqianwenku_abstract.fa  --fqpath /mnt/rorke/work/chaozhang/singlecell/testmixpipeline/rawdata  --workdir /mnt/rorke/work/chaozhang/singlecell/testmixpipeline/result --name SH180274A_ZDSY_s1 --mis 0`   
base :每个样本对应的barcode序列或者sample tagsequence 序列，推荐直接使用sampletag进行比对，节省时间  
fqpath&name：原始数据存放目录，用来找到原始数据，命名规则如下  
{name}_[1,2,3,4]_R1.fq.gz  
{name}_[1,2,3,4]_R2.fq.gz  
程序会使用4个进程同时处理数据
workdir:数据输出目录  
mis：bowtie比对时选择mismatch的数目，最高为2，默认为0


## step3   
统计每个样品的barcode数目
`mixsample countbar  --base /mnt/rorke/work/chaozhang/singlecell/testmixpipeline/qinbobiaoqianwenku_abstract.fa   --name s1   --barcode /mnt/rorke/work/chaozhang/singlecell/testmixpipeline/barcodecount/barcodes.fa  --workdir /mnt/rorke/work/chaozhang/singlecell/testmixpipeline/barcodecount`

base:第一步得到的sample tag sequence 序列，需要使用bowtie-build 建立比对索引
name:比对是输出结果文件的名字
barcode：建立文库测序的单细胞cell barocde序列
workdir:结果输出目录
mis:bowtie比对时选择mismatch的数目，最高为2,默认为0


结果即比对结果文件，参见bowtie结果。
