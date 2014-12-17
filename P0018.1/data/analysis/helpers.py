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
	dm = dm.select('saccVel > 5')
	dm = dm.select('saccLat > 0')
	dm = dm.select('saccLat < 2000')
	print dm.collapse(['subject_nr'], 'subject_nr')
	print dm.collapse(['startPos'], 'subject_nr')
	# Add regression parameters
	dm = dm.addField('pupilIntercept', dtype=float, default=0)
	dm = dm.addField('slopeX', dtype=float, default=0)
	dm = dm.addField('slopeY', dtype=float, default=0)
	for subject_nr in dm.unique('subject_nr'):		
		l = []
		for startPos in ['left', 'right', 'bottom', 'top']:
			_dm = dm.select('subject_nr == %d' % subject_nr, verbose=False) \
				.select('startPos == "%s"' % startPos, verbose=False)
			for trialDm in _dm:
				ps = tk.getTrace(trialDm, **baselineParams).mean()
				x = _dm['startX'].mean()
				y = -_dm['startY'].mean() # In PsychoPy, negative is down
				l.append( [x, y, ps] )
		a = np.array(l)
		df = pd.DataFrame(a, columns=['x', 'y', 'ps'])
		model = sm.ols('ps ~ x+y', data=df)
		results = model.fit()
		print 'Subject %d' % subject_nr
		print results.params		
		print results.params[0], results.params[1], results.params[2]
		i = np.where(dm['subject_nr'] == subject_nr)
		dm['pupilIntercept'][i] = results.params[0]
		dm['slopeX'][i] = results.params[1]
		dm['slopeY'][i] = results.params[2]
	return dm

def peakVel(dm):
	
	"""
	desc:
		Analyses peak velocity per startPos.
		
	arguments:
		dm:
			type:	DataMatrix		
	"""
	
	for startPos in ['left', 'right', 'bottom', 'top']:
		pm = PivotMatrix(dm, ['subject_nr'], ['subject_nr'],
			dv='sf_%s' % startPos)
		pm._print(startPos, sign=4)

