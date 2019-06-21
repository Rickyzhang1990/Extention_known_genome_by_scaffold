# Paper 
Integrated analysis of single cell transcriptomic data across conditions, technologies, and species  
# website  
http://www.satijalab.org/seurat   
# **Algorithm process**   
## 1、Identifying shared correlation structures across datasets    
CCA is robust to affine transformations in the original data, and is unaffected by linear shifts in gene expression (for example, due to different normalization strategies). 
**Step1** CCA analysis :CCA returns vectors whose gene-level projections are correlated between datasets, but not necessarily aligned,
CCA(canonical correlation analysis)：为了从总体上把握两组指标之间的相关关系，分别在两组变量中提取有代表性的两个综合变量U1和V1（分别为两个变量组中各变量的线性组合），  
利用这两个综合变量之间的相关关系来反映两组指标之间的整体相关性。为了研究两组变量量X= (X1, ...,Xn) 和Y= (Y1, ...,Ym) 之间的相关关系，采用类似于主成分分析的方法，   
在两组变量中，分别选取若干有代表性的变量组成有代表性的综合指标，通过研究这两组综合指标之间的相关关系，来代替这两组变量间的相关关系，这些综合指标称为典型变量。
DTW(dynamic time warping):动态时间规整，  

# Seurat  v3   
由于官方文档没有进行CCA分析的示例，在seurat官方github的issue中查找到一个讨论问题
https://github.com/satijalab/seurat/issues/1074  
根据该篇文档测试代码如下：
经过资料查找，发现这一版是旧的
```R   
c1.data <- Read10X("/lustre/work/chaozhang/test/test_Seurat3/owndata/C1")
c3.data <- Read10X("/lustre/work/chaozhang/test/test_Seurat3/owndata/C3")
c1 <- CreateSeuratObject(c1.data)
c1 <- NormalizeData(c1)
c1 <- ScaleData(c1)
c3 <- CreateSeuratObject(c3.data)
c3 <- NormalizeData(c3)
c3 <- ScaleData(c3)
c1 <-FindVariableFeatures(object = c1, selection.method = "vst", nfeatures = 1000)
c3 <-FindVariableFeatures(object = c3, selection.method = "vst", nfeatures = 1000)
g.1 <-head(rownames(HVFInfo(object = c1)), n = 1000)
g.2 <-head(rownames(HVFInfo(object = c3)), n = 1000)
genes.use <-unique(c(g.1,g.2))
genes.use <-intersect(genes.use, rownames(GetAssayData(object = c1, slot = "scale.data")))
genes.use <-intersect(genes.use, rownames(GetAssayData(object = c3, slot = "scale.data")))
c1$c3 <- "c1"
c3$c1 <- "c3"
result <- RunCCA(object1 = c1, object2 = c3, genes.use=genes.use, num.cc = 30, add.cell.id1='c1', add.cell.id2='c3')
```
**v3版**批次校正整合流程：参考如下(https://github.com/satijalab/seurat/issues/1617)  
参考二(https://satijalab.org/seurat/v3.0/immune_alignment.html)
```R 
library(Seurat)
c1.data <- Read10X("/lustre/work/chaozhang/test/test_Seurat3/owndata/C1" )
c3.data <- Read10X("/lustre/work/chaozhang/test/test_Seurat3/owndata/C3" )
c1 <- CreateSeuratObject(c1.data, project = "C1", min.cells = 5)
c1$c3 <- "C1"
c1 <- subset(c1, subset = nFeature_RNA > 500)
c1 <- NormalizeData(c1, verbose = FALSE)
c1 <- FindVariableFeatures(c1, selection.method = "vst", nfeatures = 2000)
c3 <- CreateSeuratObject(counts = c3.data , project = "C3", min.cells = 5)
c3$c1 <- "C3"
c3 <- subset(c3, subset = nFeature_RNA > 500)
c3 <- NormalizeData(c3, verbose = FALSE)
c3 <- FindVariableFeatures(c3, selection.method = "vst", nfeatures = 2000)
c1c3.anchors <- FindIntegrationAnchors(object.list = list(c1, c3), dims = 1:20)
c1c3_inter <- IntegrateData(anchorset = c1c3.anchors, new.assay.name = "integrated", dims = 1:20)

```
