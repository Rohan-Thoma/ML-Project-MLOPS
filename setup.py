from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = "-e ."


def get_requirements(file_path:str)-> List[str]:
    '''
    This function will return the list of packages 
    '''
    requirements=[]
    with open(file_path, 'r') as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
             requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
    name="mlproject3",
    version= '0.0.1',
    author='rohan',
    author_email='lolguy@abc.com',
    packages = find_packages(),
    #here this below code is for a few packages, but when we have many packages we have different code
    # install_requires=['pandas', 'numpy', 'seaborn']
    install_requires = get_requirements('requirements.txt') 
)