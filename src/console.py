import rlcompleter, readline
readline.parse_and_bind('tab:complete')

import sys
import os
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(path, '..', 'src'))

import pandas as pd
import collate
