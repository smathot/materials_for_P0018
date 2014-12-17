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

from analysis.constants import *

def saccadePlot(dm, posParams, suffix='', folder=None, standalone=True):

	"""
	desc:
		Creates a saccade plot.

	arguments:
		dm:
			type:	DataMatrix

	keywords:
		suffix:
			desc:	A filename suffix for the plot.
			type:	str
		folder:
			desc:	A folder name for the plot.
			type:	[str, NoneType]
		standalone:
			desc:	Indicates whether the plot is standalone or a subplot.
			type:	bool
	"""

	if standalone:
		Plot.new(size=Plot.r)
		plt.title(suffix)
	ax = plt.gca()
	plt.xlim(0, traceParams['traceLen'])
	for trialDm in dm:
		a = tk.getTrace(trialDm, **posParams)
		if trialDm['saccVel'] < 10:
			color = 'red'
		else:
			color = 'black'
		plt.plot(a, color=color, alpha=.05)
	if posParams['deriv'] > 0:
		xPeak, yPeak, xErr, yErr = tk.getTracePeakAvg(dm, **posParams)
		print xPeak, yPeak, xErr, yErr
		plt.axvspan(xPeak-xErr, xPeak+xErr, alpha=.01)
		plt.axvline(xPeak, color='black', linestyle=':')
		plt.axhspan(yPeak-yErr, yPeak+yErr, alpha=.01)
		plt.axhline(yPeak, color='black', linestyle=':')	
	if standalone:
		Plot.save('saccadePlot'+suffix, folder=folder, show=show)

def saccadePlotStartPos(dm):

	"""
	desc:
		Creates by-start-pos saccade plots.

	arguments:
		dm:
			type:	DataMatrix
	"""

	Plot.new(size=Plot.l)
	for i, startPos in enumerate(['left', 'right', 'bottom', 'top']):
		plt.subplot(2, 2, i+1)		
		plt.title(startPos)		
		_dm = dm.select('startPos == "%s"' % startPos)
		if startPos in ['left', 'right']:
			posParams = horizParams
			plt.ylim(0, 1024)
		else:
			posParams = vertParams
			plt.ylim(0, 768)
		saccadePlot(_dm, posParams, standalone=False)
	Plot.save('saccadeStartPos', folder='saccade', show=show)

def saccadeMetrics(dm):
	
	"""
	desc:
		Creates a latency distribution histogram.
		
	arguments:
		dm:
			type:	DataMatrix
	"""
	
	Plot.new(size=Plot.r)
	plt.subplot(211)
	plt.hist(dm['saccLat'], bins=100)
	plt.subplot(212)
	plt.hist(dm['saccVel'], bins=100)
	Plot.save('metrics', folder='saccade', show=show)
