# **Paper**  
Batch effects in single-cell RNA -sequencing data are corrected by matching mutual nearest neighbors
# **Website**  
https://github.com/MarioniLab/MNN2017/  
# **Funcition**  
we propose a new method for removal of discrepancies between biologically related batches according to the presence of MNNs between batches, which are considered to define the most similar cells of the same type across batches.  
# **Knowledge**   
**The first step** of our method involves global scaling of the data through a cosine normalization  
**cosine_normalization**       ![cosine normalization](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/cosine_normalization.png)  
**The next step** involves identification of mutual nearest neighbors.  
           ![MNN algorithm](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/MNN_algorithm.png)  
**step three** For each MNN pair, a pair-specific batch-correction vector is computed as the vector difference between the expression profiles of the paired cells.   
**Therefore**, we can calculate the batch vectors for a different set of inquiry genes ,A cell-specific batch-correction vector is then calculated as a weighted average of these pair-specific vectors,as computed with a Gaussian kernel.     
# **parameters and notice**   
```R
mnnCorrect(..., k=20, sigma=0.1, cos.norm.in=TRUE, cos.norm.out=TRUE,
         svd.dim=0L, var.adj=TRUE, compute.angle=FALSE, subset.row=NULL, 
         order=NULL, pc.approx=FALSE, irlba.args=list(),
         BPPARAM=SerialParam())  
```   
  ...: Two or more expression matrices where genes correspond to
     rows and cells correspond to columns. Each matrix should
     contain cells from the same batch; multiple matrices
     represent separate batches of cells. Each matrix should
     contain the same number of rows, corresponding to the same
     genes (in the same order).  
    k: An integer scalar specifying the number of nearest neighbors
     to consider when identifying mutual nearest neighbors.  
sigma: A numeric scalar specifying the bandwidth of the Gaussian
       smoothing kernel used to compute the correction vector for
       each cell.  
**输出结果**  
Value:

     A named list containing two components:

     ‘corrected’: A list of length equal to the number of batches,
          containing matrices of corrected expression values for each
          cell in each batch. The order of batches is the same as
          supplied in ‘...’, and the order of cells in each matrix is
          also unchanged.

     ‘pairs’: A named list of length equal to the number of batches,
          containing DataFrames specifying the MNN pairs used for
          correction. Each row of the DataFrame defines a pair based on
          the cell in the current batch and another cell in an earlier
          batch. The identity of the other cell and batch are stored as
          run-length encodings to save space.
**示例**
```R 
Examples:

     B1 <- matrix(rnorm(10000), ncol=50) # Batch 1 
     B2 <- matrix(rnorm(10000), ncol=50) # Batch 2
     out <- mnnCorrect(B1, B2) # corrected values
    corrected <- out$correcred 
	pairs <-  out$pairs
```
**必填参数**为第一个，需要数据2个或者2个以上的表达矩阵，每个矩阵应当行数相同即基因相同且基因顺序也一致。    
**Expected type of input data**:    
The input expression values should generally be log-transformed,e.g., log-counts, see ‘normalize’ for details. They should also be normalized within each data set to remove cell-specific biases in capture efficiency and sequencing depth. By default, a further cosine normalization step is performed on the supplied expression data to eliminate gross scaling differences between data sets.     
Normalization methods:Pooling across cells to normalize single-cell RNA sequencing data with many zero counts
# MNN local test  
使用C1,C3数据进行批次校正，首先使用magic软件对数据进行填充和标准化，使用自写脚本提取二者相同的基因。使用`scran`包中的`mnnCorrect`对得到的两个matrix进行批次校正，代码如下：  
```R 
library(scran)
c1 <- read.table("/lustre/work/chaozhang/test/test_MNN/normarlization/temp/C1_filter_matrix.csv_imputed_intersect",sep = "\t" ,header = T) 
c3 <- read.table("/lustre/work/chaozhang/test/test_MNN/normarlization/temp/C3_filter_matrix.csv_imputed_intersect",sep = "\t" ,header = T)
c1_rowname = c1[,1] 
c1_matrix <- c1[,-1]
c3_rowname <-  c3[,1]
c3_matrix <- c3[,-1]
c1_matrix <- data.matrix(c1_matrix)
c3_matrix <- data.matrix(c3_matrix)
result <- mnnCorrect(c1_matrix ,c3_matrxi ,k=20)
c1_correct <- result$corrected[[1]]
c1_result <- cbind(c1_rowname , data.frame(result$corrected[[1]]))
c3_result <- cbind(c3_rowname , data.frame(result$corrected[[2]]))
write.table(c1_result , sep = "\t" ,quote = F ,col.names = F ,row.names = T ,file = "c1_correct.csv")
write.table(c3_result , sep = "\t" ,quote = F ,col.names = F ,row.names = T ,file = "C3_correct.csv")
```   

# 相关知识：  
欧氏距离：欧式距离源自N维欧氏空间中两点x1,x2x1​,x2​间的距离公式。   
              ![欧氏距离](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/euli_distance.png)    
余弦距离：余弦相似度，又称为余弦相似性，是通过计算两个向量的夹角余弦值来评估他们的相似度。余弦相似度将向量根据坐标值，绘制到向量空间中。  
              ![余弦相似度](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/cosine_distance.png)  
高斯核函数：所谓径向基函数 (Radial Basis Function 简称 RBF), 就是某种沿径向对称的标量函数。 通常定义为空间中任一点x到某一中心xc之间欧氏距离的单调函数 , 可记作 k(||x-xc||), 其作用往往是局部的 , 即当x远离xc时函数取值很小。最常用的径向基函数是高斯核函数 ,形式为 k(||x-xc||)=exp{- ||x-xc||^2/(2*σ^2) } 其中xc为核函数中心,σ为函数的宽度参数 , 控制了函数的径向作用范围。  
              ![Gaussian kernel](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/Gaussian_kernel.png)
