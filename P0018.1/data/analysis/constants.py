#-*- coding:utf-8 -*-

"""
This file is part of P0014.1.

P0014.1 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

P0014.1 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with P0014.1.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import math
from exparser import TraceKit as tk
from exparser import Plot
from exparser.TangoPalette import *
from exparser.Cache import cachedDataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from yamldoc import validate
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.stats import nanmedian
import pandas as pd	
import statsmodels.formula.api as sm
import warnings

smoothParams = None #{'windowLen' : 21}
traceLen = 1500

def regressFunc(a, dm):
	
	return a[:,2] - a[:,0]*dm['slopeX'][0] - a[:,1]*dm['slopeY'][0]

traceParams = {
	'signal'			: 'pupil',
	'lock'				: 'start',
	'phase'				: 'sacc',
	'baseline'			: 'sacc',
	'baselineLock'		: 'start',
	'baselineLen'		: 10,
	'baselineOffset'	: 295,
	'traceLen'			: traceLen,
	'regress'			: regressFunc,
	}

baselineParams = {
	'signal'			: 'pupil',
	'lock'				: 'end',
	'phase'				: 'baseline',
	'traceLen'			: 100,
	}

horizParams = {
	'signal'			: 'x',
	'lock'				: 'start',
	'phase'				: 'sacc',
	'traceLen'			: traceLen,
	'deriv'				: 0,
	'smoothParams'		: smoothParams,
	}

vertParams = horizParams.copy()
vertParams['signal'] = 'y'


show = '--show' in sys.argv
matchColor = green[1]
nonMatchColor = red[1]
yLim = .8, 1.05
lookback = 300
# Display center
xc = 512
yc = 384
maxN = None