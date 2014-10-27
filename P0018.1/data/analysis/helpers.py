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
from yamldoc import validate
from matplotlib import pyplot as plt
import warnings

traceParams = {
	'signal'			: 'pupil',
	'lock'				: 'start',
	'phase'				: 'sacc',
	'baseline'			: 'cue',
	'baselineLock'		: 'end',
	'baselineLen'		: 10,
	'traceLen'			: 2500
	}

show = '--show' in sys.argv
matchColor = green[1]
nonMatchColor = red[1]

def pupilPlot(dm, suffix=''):

	dmMatch = dm.select('match == 1')
	dmNonMatch = dm.select('match == 0')

	Plot.new(size=Plot.r)
	ax = plt.gca()
	plt.title(suffix)
	tk.plotTraceAvg(ax, dmMatch, lineColor=matchColor, label='Match',
		**traceParams)
	tk.plotTraceAvg(ax, dmNonMatch, lineColor=nonMatchColor, label='Non-match',
		**traceParams)
	plt.legend()
	Plot.save('pupilPlot'+suffix, show=True)

def pupilPlotStartPos(dm):

	pupilPlot(dm.select('startPos == "left"'), suffix='left')
	pupilPlot(dm.select('startPos == "right"'), suffix='right')
	pupilPlot(dm.select('startPos == "bottom"'), suffix='bottom')
	pupilPlot(dm.select('startPos == "top"'), suffix='top')

