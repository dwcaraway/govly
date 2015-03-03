from setuptools import setup
import os

req_file = os.path.abspath(os.path.join(os.path.abspath(__file__), '../requirements.txt'))

with open(req_file) as f:
    required = [z for z in f.read().splitlines() if (z and z[0] != '#')]

print required

setup(name='Vitals',
      version='0.0.1',
      description='FogMine Department of Defense Procurement Market Research Tool',
      author='David Caraway',
      author_email='dave@fogmine.com',
      url='http://www.fogmine.com',
      packages = ['.', 'spiders'],
      entry_points={'scrapy':['settings=settings']},
      install_requires=required
     )
