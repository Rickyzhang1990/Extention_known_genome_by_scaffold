# scanpy vs Seurat 
## HVG gene
<font color=#0099ff size=12 face="黑体">Scanpy</font>  
![Scanpy](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/Scanpy_HVG.png)  
<font color=#0099ff size=12 face="黑体">Seurat</font>
![SeuRat](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/Seurat_HVG.png)  

## PCA 
<font color=#0099ff size=12 face="黑体">Scanpy</font> 
![Scanpy](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/Scanpy_PCA.png)   
<font color=#0099ff size=12 face="黑体">Seurat</font>
![seurat](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/Seurat_PCA.png)  

## u-map
<font color=#0099ff size=12 face="黑体">Scanpy</font> 
![Scanpy](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/Scanpy_umap.png)   
<font color=#0099ff size=12 face="黑体">Seurat</font>
![seurat](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/Seurat_umap.png)

## violin plot 
<font color=#0099ff size=12 face="黑体">Scanpy</font>  
![Scanpy](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/Scanpy_violin.png)  
<font color=#0099ff size=12 face="黑体">Seurat</font> 
![seurat](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/Seurat_violin.png)

## Dot plot  
<font color=#0099ff size=12 face="黑体">Scanpy</font>  
![Scanpy](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/Scanpy_dotplot.png)   

##  trajectory inference   
等同于拟时间分析分析，轨迹推断/伪时间分析则构建了一个细胞发育和分化的模型。  
**Scanpy**  
![ PAGA](https://github.com/Rickyzhang1990/during_work/blob/master/paper_and_Algorithm/image/Scanpy_paga.png)  

总结：从结果来看，seurat包做出的图形就美观性看来要优于scanpy包的输出结果，但是scanpy包集合了当前单细胞数据大多数的分析内容，包括数据预处理，   
数据可视化，聚类，拟时间分析，差异表达分析等。就功能完整性上来看要优于Seurat包（seurat包拟时间分析需要monocle包)。此外使用scanpy包还可以进  
以有其他的图形，[详细可见以下]（https://scanpy-tutorials.readthedocs.io/en/latest/visualizing-marker-genes.html）。
总体来说，scanpy是一个功能全面，且可以实现多种分析的单细胞分析包。