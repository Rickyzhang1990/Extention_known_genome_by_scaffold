#-*-utf-8-*-


from setuptools import setup , find_packages

setup(name='scMixSample',
      version='0.0',
      description='use multi cores delete a lot of files',
      author='kakazhang',
      author_email='chaozhang@capitalbiotech.com',
      packages=find_packages(), 
      requires=['click',"configparser","multiprocessing","gzip","re"],
      scripts=["scMixSample"],
      url = ""
)
