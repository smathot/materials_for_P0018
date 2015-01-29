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

from matplotlib import pyplot as plt
from analysis.constants import *
from analysis import pupil, saccade

@cachedDataMatrix
def _filter(dm):

	"""
	desc:
		Filtering and integraty checks of data.

	arguments:
		dm:
			type:	DataMatrix

	returns:
		dm:
			type:	DataMatrix
	"""

	# Extract subject numbers from the filenames
	print('Checking subject numbers ...')
	for fname in dm.unique('file'):
		i = int(fname[2:4])
		_dm = dm.select('file == "%s"' % fname, verbose=False)
		assert(_dm.count('subject_nr') == 1)
		print('%s -> %d -> %d' % (fname, i, _dm['subject_nr'][0]))
		assert(_dm['subject_nr'][0] == i)
	# Filter outliers
	dm = dm.select('saccVel > 0')
	dm = dm.select('saccLat > 0')
	dm = dm.select('saccLat < 2000')
	print dm.collapse(['subject_nr'], 'subject_nr')
	print dm.collapse(['startPos'], 'subject_nr')
	# Fix miscoding of bottom/ top
	iBottom = np.where(dm['startPos'] == 'bottom')
	iTop = np.where(dm['startPos'] == 'top')
	dm['startPos'][iBottom] = 'top'
	dm['startPos'][iTop] = 'bottom'
	# Filter trials with fixation errors
	dm = dm.addField('fixErr', dtype=float)
	dm = dm.addField('saccErr', dtype=float)
	for i in dm.range():
		if dm[i]['startPos'] in ['left', 'right']:
			_traceParams = horizParams
			ref = dm[i]['startX']
		else:
			_traceParams = vertParams
			ref = dm[i]['startY']
		a = tk.getTrace(dm[i], **_traceParams)
		fixErr = np.abs(a[:200]-ref).max()
		saccErr = np.abs(a[lookback+100:]+ref).max()
		dm['fixErr'][i] = fixErr
		dm['saccErr'][i] = saccErr
	dm = dm.select('fixErr < 100')
	dm = dm.select('saccErr < 100')
	# Add regression parameters
	dm = dm.addField('pupilIntercept', dtype=float, default=0)
	dm = dm.addField('slopeX', dtype=float, default=0)
	dm = dm.addField('slopeY', dtype=float, default=0)
	dm = dm.addField('saccDir', dtype=str)
	dm['saccDir'][dm.where('startPos == "left"')] = 'horiz'
	dm['saccDir'][dm.where('startPos == "right"')] = 'horiz'
	dm['saccDir'][dm.where('startPos == "top"')] = 'vert'
	dm['saccDir'][dm.where('startPos == "bottom"')] = 'vert'
	for _dm in dm.group(['subject_nr']):
		subject_nr = _dm['subject_nr'][0]
		l = []
		for trialDm in _dm:
			x = trialDm['startX'][0]
			y = trialDm['startY'][0]
			ps = tk.getTrace(trialDm, **baselineParams).mean()
			l.append( [x, y, ps] )
		a = np.array(l)
		df = pd.DataFrame(a, columns=['x', 'y', 'ps'])
		model = sm.ols('ps ~ x + y', data=df)
		results = model.fit()
		print('ps(%d) = %.2f + %.4f*x + %.4f*y' % (subject_nr,
			results.params[0], results.params[1], results.params[2]))
		i = dm.where('subject_nr == %d' % subject_nr)
		assert(len(i) == len(_dm))
		dm['pupilIntercept'][i] = results.params[0]
		dm['slopeX'][i] = results.params[1]
		dm['slopeY'][i] = results.params[2]
	# Add peak velocity estimation
	dm = dm.addField('_peakVel', dtype=float)
	for i in dm.range():
		if dm['startPos'][i] in ['left', 'right']:
			posParams = horizParams
		else:
			posParams = vertParams
		a = tk.getTrace(dm[i], **posParams)[lookback-50:lookback+50]
		v = np.abs(a[1:]-a[:-1])
		peakVel = np.nanmax(v)
		dm['_peakVel'][i] = peakVel * (1000./pxPerDeg)
	dm = dm.select('_peakVel < 1000')
	dm = dm.removeNan('_peakVel')
	return dm

def directionPlot(dm):

	"""
	desc:
		Creates a multipanel plot that shows the pupil trace, saccade profile,
		and saccade-velocity profile for each starting position.

	arguments:
		dm:
			type:	DataMatrix
	"""

	for i, startPos in enumerate(startPositions):
		_dm = dm.select('startPos == "%s"' % startPos)
		# Position
		if startPos in ['left', 'right']:
			posParams = horizParams
		else:
			posParams = vertParams
		Plot.new(size=tilePlot)
		saccade.saccadePlot(_dm, posParams, standalone=False, trials=True,
			avg=False, vLine=False)
		plt.xticks([])
		plt.yticks([])
		plt.ylim(-384, 384)
		Plot.save('trialBitmap.%s.position' % startPos, folder='bitmaps')
		# Velocity
		if startPos in ['left', 'right']:
			posParams = horizVelParams
		else:
			posParams = vertVelParams
		Plot.new(size=tilePlot)
		saccade.saccadePlot(_dm, posParams, standalone=False, trials=True,
			avg=False, vLine=False)
		plt.xticks([])
		plt.yticks([])
		plt.ylim(0, 700)
		Plot.save('trialBitmap.%s.vel' % startPos, folder='bitmaps')
		# Orthogonal velocity
		if startPos in ['left', 'right']:
			posParams = vertVelParams
		else:
			posParams = horizVelParams
		Plot.new(size=tilePlot)
		saccade.saccadePlot(_dm, posParams, standalone=False, trials=True,
			avg=False, vLine=False, colorRange=(0,150))
		plt.xticks([])
		plt.yticks([])
		plt.ylim(0, 200)
		Plot.save('trialBitmap.%s.orthoVel' % startPos, folder='bitmaps')

	Plot.new(size=Plot.xl)
	for i, startPos in enumerate(startPositions):
		_dm = dm.select('startPos == "%s"' % startPos)
		plt.subplot2grid((4, 4), (i, 0), colspan=2)
		model = 'match + (1+match|subject_nr)'
		pupil.pupilPlot(_dm, standalone=False, suffix='.'+startPos, model=model,
			setYLim=False)
		plt.title('startPos = %s, N = %d' % (startPos, len(_dm)))
		plt.subplot2grid((4, 4), (i, 2))
		if startPos in ['left', 'right']:
			posParams = horizParams
		else:
			posParams = vertParams
		plt.ylim(-384, 384)
		plt.axhline(288, color='black', linestyle=':')
		plt.axhline(-288, color='black', linestyle=':')
		saccade.saccadePlot(_dm, posParams, standalone=False, trials=False)
		y = np.linspace(-340, 340, 5)
		plt.yticks(y, y/pxPerDeg)
		plt.xlabel('Time (ms)')
		plt.ylabel('Eye position (o)')
		plt.subplot2grid((4, 4), (i, 3))
		if startPos in ['left', 'right']:
			posParams = horizVelParams
		else:
			posParams = vertVelParams
		saccade.saccadePlot(_dm, posParams, standalone=False,
			colorRange=(200, 600), trials=False)
		plt.xlabel('Time (ms)')
		plt.ylabel('Velocity (o/s)')
		plt.ylim(0, 700)
	Plot.save('directionPlot', folder='full', show=show)

def fullPlot(dm, stats=True, suffix=''):

	"""
	desc:
		Creates a fully detailed multipanel plot.

	arguments:
		dm:
			type:	DataMatrix

	keywords:
		stats:
			desc:	Indicates whether statistics should run.
			type:	bool
		suffix:
			desc:	Indicates a filename suffix for the plot.
			type:	str
	"""

	Plot.new(size=Plot.xl)
	plt.subplot2grid((6, 2), (0, 0), colspan=2, rowspan=2)
	if stats:
		model = 'match*saccDir + (1+match+saccDir|subject_nr)'
	else:
		model = None
	pupil.pupilPlot(dm, standalone=False, suffix=suffix+'.full', model=model)
	plt.title('N = %d' % len(dm))
	for i, startPos in enumerate(('left', 'right', 'bottom', 'top')):
		_dm = dm.select('startPos == "%s"' % startPos)
		plt.subplot2grid((6, 2), (2+i, 0))
		if stats:
			model = model='match + (1+match|subject_nr)'
		else:
			model = None
		pupil.pupilPlot(_dm, standalone=False, suffix=suffix+'.'+startPos,
			model=model)
		plt.title('startPos = %s, N = %d' % (startPos, len(_dm)))
		plt.subplot2grid((6, 2), (2+i, 1))
		if startPos in ['left', 'right']:
			posParams = horizParams
		else:
			posParams = vertParams
		plt.ylim(-384, 384)
		saccade.saccadePlot(_dm, posParams, standalone=False)
	Plot.save('fullPlot'+suffix, folder='full')

def fullPlotSubject(dm):

	"""
	desc:
		Creates a full plot for each subject.

	arguments:
		dm:
			type:	DataMatrix
	"""

	for _dm in dm.group('subject_nr'):
		print(_dm['subject_nr'][0])
		fullPlot(_dm, suffix='.%d' % _dm['subject_nr'][0], stats=False)
