# **Paper**  
Batch effects in single-cell RNA -sequencing data are corrected by matching mutual nearest neighbors
# **Website**  

# **Funcition**  
we propose a new method for removal of discrepancies between biologically related batches according to the presence of MNNs between batches, which are considered to define the most similar
cells of the same type across batches.

# **Knowledge**   
The first step of our method involves global scaling of the data through a cosine normalization  
![cosine normalization](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/cosine_normalization.png)
The next step involves identification of mutual nearest neighbors.  
![MNN algorithm](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/MNN_algorithm.png)
For each MNN pair, a pair-specific batch-correction vector is computed as the vector difference between the expression profiles of the paired cells. 
Therefore, we can calculate the batch vectors for a different set of inquiry genes ,A cell-specific batch-correction vector is then calculated as a weighted average of these pair-specific vectors,  
 as computed with a Gaussian kernel. 
相关知识：  
欧氏距离：欧式距离源自N维欧氏空间中两点x1,x2x1​,x2​间的距离公式。  
![欧氏距离](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/euli_distane.png)  
余弦距离：余弦相似度，又称为余弦相似性，是通过计算两个向量的夹角余弦值来评估他们的相似度。余弦相似度将向量根据坐标值，绘制到向量空间中。  
![余弦相似度](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/cosine_distance.png)
高斯核函数：所谓径向基函数 (Radial Basis Function 简称 RBF), 就是某种沿径向对称的标量函数。 通常定义为空间中任一点x到某一中心xc之间欧氏距离的单调函数 , 可记作 k(||x-xc||), 其作用往往是局部的 , 即当x远离xc时函数取值很小。最常用的径向基函数是高斯核函数 ,形式为 k(||x-xc||)=exp{- ||x-xc||^2/(2*σ^2) } 其中xc为核函数中心,σ为函数的宽度参数 , 控制了函数的径向作用范围。
![Gaussian kernel](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/Gaussian_kernel.png)