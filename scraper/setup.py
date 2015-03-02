from setuptools import setup, find_packages
import os
from pip.req import parse_requirements


# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements/scraper.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

print reqs

setup(name='Vitals',
      version='0.0.1',
      description='FogMine Department of Defense Procurement Market Research Tool',
      author='David Caraway',
      author_email='dave@fogmine.com',
      url='http://www.fogmine.com',
      packages = ['scraper', 'scraper.spiders','app'],
      entry_points={'scrapy':['settings=scraper.settings']},
      install_requires=reqs
     )
