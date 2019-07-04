# python中的排列组合
在日常的工作学习中，我们肯定会遇到排列组合问题，比如，在5种颜色的球中，任意取3个，共有多少种组合方式，这也包括  
又放回和无放回抽样。
c5/3和a5/3的区别，在python中，自带的排列组合函数，都在python的指导工具包itertools中。  
product 笛卡尔积　　（有放回抽样排列）  
permutations 排列　　（不放回抽样排列）  
combinations 组合,没有重复　　（不放回抽样组合）  
combinations_with_replacement 组合,有重复　　（有放回抽样组合）  
```python 
>>> import itertools
>>> for i in itertools.product('ABCD', repeat = 2):
...     print(i)
... 
('A', 'A') ('A', 'B') ('A', 'C') ('A', 'D') ('B', 'A') ('B', 'B') ('B', 'C') ('B', 'D') ('C', 'A') ('C', 'B') ('C', 'C') ('C', 'D') ('D', 'A') ('D', 'B') ('D', 'C') ('D', 'D')
>>> for i in itertools.permutations('ABCD', 2):
...     print(i)
... 
('A', 'B') ('A', 'C') ('A', 'D') ('B', 'A') ('B', 'C') ('B', 'D') ('C', 'A') ('C', 'B') ('C', 'D') ('D', 'A') ('D', 'B') ('D', 'C')
>>> for i in itertools.combinations('ABCD', 2):
...     print(i)
... 
('A', 'B') ('A', 'C') ('A', 'D') ('B', 'C') ('B', 'D') ('C', 'D')
>>> for i in itertools.combinations_with_replacement('ABCD', 2):
...     print(i)
... 
('A', 'A') ('A', 'B') ('A', 'C') ('A', 'D') ('B', 'B') ('B', 'C') ('B', 'D') ('C', 'C') ('C', 'D') ('D', 'D')
```
python3中返回的为对象，可以通过迭代读取将值输出。  
`end`