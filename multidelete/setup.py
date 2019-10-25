#-*-utf-8-*-


from setuptools import setup , find_packages

setup(name='multidelete',
      version='0.1',
      description='use multi cores delete a lot of files',
      author='kakazhang',
      author_email='fredzhang1990@163.com',
      packages=find_packages(), 
      requires=['multidelete',"multiprocessing"],
      scripts=["mude"],
      url = ""
)
