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

def pupilPlot(dm, suffix='', folder='pupil', model=None, standalone=True,
	setYLim=True):

	"""
	desc:
		Creates a main pupil plot contrasting match and non-match trials.

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
		model:
			desc:	The statistical model to be used or `None` for no
					statistics.
			type:	[str, NoneType]
		standalone:
			desc:	Indicates whether the plot is standalone or a subplot.
			type:	bool
		setYLim:
			desc:	Indicates whether the Y limit should be fixed (True) or set
					automatically by pyplot (False).
			type:	bool
	"""

	if standalone:
		plt.title(suffix)
		Plot.new(rectPlot)
	plt.xlim(0, traceParams['traceLen'])
	cols = ['match', 'saccDir', 'subject_nr', '__trace_sacc__', 'slopeX',
		'slopeY', '_peakVel']
	if 'errVel' in dm.columns():
		cols += ['errVel', 'errVelPerc']
	if 'orthoVel' in dm.columns():
		cols += ['orthoVel']
	_dm = dm.selectColumns(cols)
	plt.axvline(lookback, color='black', linestyle=':')
	plt.axhline(1, color='black', linestyle=':')
	tk.plotTraceContrast(_dm, 'match == 1', 'match == 0', model=model,
		label1='Intrasaccadic Percept (N=%d)' % len(_dm.select('match == 1')),
		label2='No Percept (N=%d)' % len(_dm.select('match == 0')),
		winSize=winSize, cacheId='.lmerPupil'+suffix, **traceParams)
	plt.legend(frameon=False, loc='upper right')
	plt.xlim(0, traceParams['traceLen'])
	plt.xticks(range(100, traceParams['traceLen'], 200),
		range(100-lookback, traceParams['traceLen']-lookback, 200))
	if setYLim:
		plt.ylim(pupilRange)
	plt.ylabel('Pupil size (normalized)')
	plt.xlabel('Time relative to mid-saccade point (ms)')
	if standalone:
		Plot.save('pupilPlot'+suffix, folder=folder, show=show)

def mainPupilPlot(dm):

	"""
	desc:
		Provides the main results figure.

	arguments:
		dm:
			type:	DataMatrix
	"""

	model = 'match*saccDir + (1+match+saccDir|subject_nr)'
	pupilPlot(dm, suffix='.full', model=model)

def indDiffTracePlot(dm):

	"""
	desc:
		Plots individual results, with one pupil-size-difference trace per
		participant.

	arguments:
		dm:
			type:	DataMatrix
	"""
	Plot.new(rectPlot)
	for subject_nr, _dm in dm.walk('subject_nr'):
		print(subject_nr)
		x1, y1, err1 = tk.getTraceAvg(_dm.select('match == 1', verbose=False),
			**traceParams)
		x2, y2, err2 = tk.getTraceAvg(_dm.select('match == 0', verbose=False),
			**traceParams)
		d = y1 - y2
		plt.fill_between(x1, d, alpha=.25, color=blue[1], edgecolor=None)
		plt.plot(x1, d, color=blue[1])
	plt.xlim(0, traceLen)
	plt.xticks(range(100, traceParams['traceLen'], 200),
		range(100-lookback, traceParams['traceLen']-lookback, 200))
	plt.ylabel('Pupil-size difference (normalized)')
	plt.xlabel('Time relative to mid-saccade point (ms)')
	plt.axvline(lookback, color='black', linestyle=':')
	plt.axhline(0, color='black', linestyle=':')
	Plot.save('indDiffTracePlot', folder='pupil', show=show)
