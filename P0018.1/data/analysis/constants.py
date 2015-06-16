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
from exparser.DataMatrix import DataMatrix
from exparser.TangoPalette import *
from exparser.Cache import cachedDataMatrix, cachedArray
from exparser.PivotMatrix import PivotMatrix
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.CsvReader import CsvReader
from exparser import RBridge
from yamldoc import validate
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.stats import nanmedian
import pandas as pd
import statsmodels.formula.api as sm
import warnings
from matplotlib import colors
import matplotlib.cm as cmx
from scipy.stats import linregress

show = '--show' in sys.argv
smoothParams = {'windowLen' : 11}
traceLen = 1500
pxPerDeg = 34
frameDur = 1000./150
saccVelRange = 200, 600
matchColor = green[1]
nonMatchColor = red[1]
pupilRange = .84, 1.08
lookback = 300
winSize = 1
# Display center
xc = 512
yc = 384
maxN = None
startPositions = 'left', 'right', 'top', 'bottom'
saccadeDirections = 'right', 'left', 'down', 'up'

tilePlot = 4, 4
rectPlot = 8, 4
widePlot = 12, 4
mainPlot = 12, 6
highPlot = 12, 12

traceParams = {
	'signal'			: 'pupil',
	'lock'				: 'start',
	'phase'				: 'sacc',
	'baseline'			: 'sacc',
	'baselineLock'		: 'start',
	'baselineLen'		: 10,
	'baselineOffset'	: 195,
	'traceLen'			: traceLen,
	}

baselineParams = {
	'signal'			: 'pupil',
	'lock'				: 'end',
	'phase'				: 'baseline',
	'traceLen'			: 100,
	}

horizFilterParams = {
	'signal'			: 'x',
	'lock'				: 'start',
	'phase'				: 'sacc',
	'traceLen'			: traceLen,
	'smoothParams'		: {'windowLen' : 11},
	'transform'			: lambda x: x-xc,
	}
vertFilterParams = horizFilterParams.copy()
vertFilterParams['signal'] = 'y'
vertFilterParams['transform'] = lambda y: y-yc

horizParams = {
	'signal'			: 'x',
	'lock'				: 'start',
	'phase'				: 'sacc',
	'offset'			: 200,
	'traceLen'			: 400,
	'smoothParams'		: smoothParams,
	'transform'			: lambda x: x-xc,
	}

vertParams = horizParams.copy()
vertParams['signal'] = 'y'
vertParams['transform'] = lambda y: y-yc

horizVelParams = horizParams.copy()
horizVelParams['deriv'] = 1
horizVelParams['transform'] = lambda x: np.abs((x*1000.)/pxPerDeg)

vertVelParams = horizVelParams.copy()
vertVelParams['signal'] = 'y'
