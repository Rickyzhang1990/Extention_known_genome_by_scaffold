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

