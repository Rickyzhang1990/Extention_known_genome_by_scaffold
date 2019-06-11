Python中用来显示当前系统默认换行符的函数，例如，Windows使用’\r\n’，Linux使用’\n’而Mac使用’\r’。  
在perl语言中可以设置换行符，但是在python中不能设置系统默认换行符，当我将
```python 
import os 
os.linesep = ">"
```
时，读取时并不能按照">"为换行符进行读取，看来perl和python还是有很多不同的。 

