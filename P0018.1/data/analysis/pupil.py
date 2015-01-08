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
 
def pupilPlot(dm, suffix='', folder='pupil', model=None, standalone=True):

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
		standalone:
			desc:	Indicates whether the plot is standalone or a subplot.
			type:	bool
	"""

	dmMatch = dm.select('match == 1')
	dmNonMatch = dm.select('match == 0')
	if standalone:
		Plot.new(size=Plot.r)
		plt.title(suffix)
	ax = plt.gca()
	plt.axhline(1, linestyle='--', color='black')
	plt.xlim(0, traceParams['traceLen'])
	_dm = dm.selectColumns(['match', 'saccDir', 'subject_nr', '__trace_sacc__',
		'slopeX', 'slopeY'])
	tk.plotTraceContrast(_dm, 'match == 1', 'match == 0', label1='Match',
		label2='Non-match', model=model,
		winSize=winSize, cacheId='.lmerPupil'+suffix, **traceParams)
	plt.axvline(lookback, color='black', linestyle=':')	
	plt.legend(frameon=False, loc='lower right')
	if standalone:
		Plot.save('pupilPlot'+suffix, folder=folder, show=show)

def pupilPlotSubject(dm):

	"""
	desc:
		Creates by-subject pupil plots.

	arguments:
		dm:
			type:	DataMatrix
	"""

	Plot.new(size=Plot.l)
	for i, _dm in enumerate(dm.group('subject_nr')):
		plt.subplot(5, 2, i+1)
		subjectNr = _dm['subject_nr'][0]
		plt.title('Subject %d (N=%d)' % (subjectNr, len(_dm)))
		pupilPlot(_dm, standalone=False)
	Plot.save('pupilPlotSubject', show=show, folder='pupil')

def pupilPlotStartPos(dm):

	"""
	desc:
		Creates by-start-pos pupil plots.

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
		else:
			posParams = vertParams
		pupilPlot(_dm, standalone=False)
	Plot.save('pupilPlotStartPos', folder='pupil', show=show)
