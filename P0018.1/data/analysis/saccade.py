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
from analysis import pupil

def saccadePlot(dm, posParams, suffix='', folder=None, standalone=True,
	avg=True, colorRange=saccVelRange, trials=False, vLine=True):

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
		folder:
			desc:	A folder name for the plot.
			type:	[str, NoneType]
		standalone:
			desc:	Indicates whether the plot is standalone or a subplot.
			type:	bool
		avg:
			desc:	Indicates whether the trace average should be plotted.
			type:	bool
		colorRange:
			desc:	The range of values to be used for color coding the traces.
			type:	tuple
	"""

	if standalone:
		Plot.new(size=Plot.r)
		plt.title(suffix)
	plt.xlim(0, posParams['traceLen'])
	plt.xticks(range(100, posParams['traceLen'], 100),
		range(100+posParams['offset']-lookback,
		posParams['traceLen']-lookback+posParams['offset'], 100))
	jet = plt.get_cmap('jet')
	cNorm  = colors.Normalize(*colorRange)
	scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
	for trialDm in dm:
		a = tk.getTrace(trialDm, **posParams)
		if 'deriv' in posParams and posParams['deriv'] > 0:
			pv = np.max(a)
		else:
			pv = trialDm['_peakVel'][0]
		color = scalarMap.to_rgba(pv)
		if trials:
			plt.plot(a, color=color, alpha=.05)
	if avg:
		x, y, err = tk.getTraceAvg(dm, **posParams)
		plt.plot(y, color='black')
	if vLine:
		plt.axvline(lookback-posParams['offset'], color='black', linestyle=':')
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
			plt.axhline(_dm['startX'][0], linestyle=':', color='black')
			plt.axhline(1024-_dm['startX'][0], linestyle=':', color='black')
			# plt.ylim(0, 1024)
		else:
			posParams = vertParams
			plt.axhline(_dm['startY'][0], linestyle=':', color='black')
			plt.axhline(768-_dm['startY'][0], linestyle=':', color='black')
			# plt.ylim(0, 768)
		saccadePlot(_dm, posParams, standalone=False)
	Plot.save('saccadeStartPos', folder='saccade', show=show)

def saccadeVelPlotStartPos(dm):

	"""
	desc:
		Creates by-start-pos saccade velocity plots.

	arguments:
		dm:
			type:	DataMatrix
	"""

	Plot.new(size=widePlot)
	plt.subplots_adjust(wspace=0)
	for i, startPos in enumerate(startPositions):
		plt.subplot(1, 4, i+1)
		plt.title(startPos)
		_dm = dm.select('startPos == "%s"' % startPos)
		if startPos in ['left', 'right']:
			posParams = vertVelParams
		else:
			posParams = horizVelParams
		saccadePlot(_dm, posParams, standalone=False, colorRange=(0, 150),
			trials=False)
		plt.ylim(0, 200)
		if i != 0:
			plt.gca().yaxis.set_ticklabels([])
		else:
			plt.ylabel('Saccade velocity (o/s)')
		plt.xlabel('Time (ms)')
	Plot.save('saccadeVelStartPos', folder='saccade', show=show)

def saccadeMetrics(dm):

	"""
	desc:
		Creates a latency distribution histogram.

	arguments:
		dm:
			type:	DataMatrix
	"""

	cm = dm.collapse(['startPos', 'subject_nr'], '_peakVel')
	cm.save('output/_peakVel.csv')
	print(cm)
	cm.ttest(['startPos'], 'std')._print(sign=5)
	cm.ttest(['startPos'], 'mean')._print(sign=5)
	Plot.new(size=Plot.r)
	plt.subplot(211)
	plt.hist(dm['saccLat'], bins=100)
	plt.subplot(212)
	colors = brightColors[:]
	stepSize = 50
	for _dm in dm.group('startPos'):
		color = colors.pop()
		startPos = _dm['startPos'][0]
		a = _dm['_peakVel']
		lx = []
		ly = []
		for edge in range(0, 1000, stepSize):
			y = np.sum((a > edge) & (a <= edge+stepSize))
			x = edge+.5*stepSize
			lx.append(x)
			ly.append(y)
		plt.plot(lx, ly, label=startPos, color=color)
		plt.axvline(a.mean(), color=color)
		print('M(%s) = %s (%s) N = %d' % (startPos, a.mean(), a.std(), len(a)))
	plt.legend(frameon=False)
	Plot.save('metrics', folder='saccade', show=show)

def peakVelCorr(dm):

	"""
	desc:
		Determines the correlation between the actual peak velocity, and that
		as predicted during peak velocity calibration.

	arguments:
		dm:
			type:	DataMatrix
	"""

	from scipy.stats import linregress, nanmean
	from exparser.DataMatrix import DataMatrix
	colors = allColors[:]
	l = [['subject_nr', 'startPos', 'sf', 'sv']]
	Plot.new()
	for _dm in dm.group('subject_nr'):
		color = colors.pop()
		symbols = ['x', 'o', 's', '.']
		for startPos in ['left', 'right', 'top', 'bottom']:
			symbol = symbols.pop()
			__dm = _dm.select('startPos == "%s"' % startPos)
			sf = .5/nanmean(__dm['sf_%s' % startPos])
			sv = nanmean(__dm['_peakVel'])
			plt.plot(sf, sv, symbol, color=color)
			l.append([__dm['subject_nr'][0], startPos, sf, sv])
	dm = DataMatrix(l)
	print(dm)
	s, i, r, p, se = linregress(dm['sf'], dm['sv'])
	print('s = %.5f, r = %.5f, p = %.5f' % (s, r, p))
	Plot.save('peakVelCorr', folder='saccade', show=show)

def curvature(dm):

	"""
	desc:
		Creates a saccade trajectory plot for each direction.

	arguments:
		dm:
			type:	DataMatrix
	"""

	Plot.new(size=widePlot)
	plt.subplots_adjust(wspace=0)
	for i, startPos in enumerate(['left', 'right', 'bottom', 'top']):
		plt.subplot(1, 4, i+1)
		plt.title(startPos)
		_dm = dm.select('startPos == "%s"' % startPos)
		jet = plt.get_cmap('jet')
		cNorm  = colors.Normalize(0, 150)
		scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
		for trialDm in _dm:
			if startPos in ('left', 'right'):
				v = tk.getTrace(trialDm, **vertVelParams)
			else:
				v = tk.getTrace(trialDm, **horizVelParams)
			color = scalarMap.to_rgba(np.max(v))
			x = tk.getTrace(trialDm, **horizParams)
			y = tk.getTrace(trialDm, **vertParams)
			plt.plot(x, y, color=color, alpha=.1)
		plt.xlim(-350, 350)
		plt.ylim(-350, 350)
	Plot.save('curvature', folder='saccade')

def orthoVelLme(dm):

	from scipy.stats import ttest_rel
	dm = dm.addField('peakOrthoVel', dtype=float)
	for i in dm.range():
		if dm['saccDir'][i] == 'vert':
			posParams = horizVelParams
		else:
			posParams = vertVelParams
		a = tk.getTrace(dm[i], **posParams)
		pv = np.max(a)
		dm['peakOrthoVel'][i] = pv
	cm = dm.collapse(['saccDir', 'subject_nr'], 'peakOrthoVel')
	cm.save('output/peakOrthoVel.saccDir.csv')
	g1 = cm['std'][10:]
	g2 = cm['std'][:10]
	print('M = %.4f, SD = %.4f' % (g1.mean(), g1.std()))
	print('M = %.4f, SD = %.4f' % (g2.mean(), g2.std()))
	t, p = ttest_rel(g1, g2)
	print t, p
