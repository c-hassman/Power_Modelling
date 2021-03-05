
import configparser
from commonscripts import DotDict, joindir
import os
import sys

parser = configparser.ConfigParser()
import pandas as pd
#parser.read([
    # the minpower default set, from the minpower/configuration directory
   # joindir(os.path.split(__file__)[0], 'configuration/minpower.cfg'),
    # the user's global overrides, from the home directory
   # os.path.expanduser('~/minpower.cfg'),
  #  os.path.expanduser('~/.minpowerrc'),
#])

parser.read('configuration/minpower.cfg')
print(parser.sections())

data = pd.read_csv('uc/smallLoad.csv ')
print(data)
#uc/smallLoad.csv