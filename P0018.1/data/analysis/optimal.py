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

def addOrthoVel(dm, nBin=2):

	"""
	desc:
		Adds orthogonal velocity information. That is, the peak velocity in the
		direction perpendicular to the saccade.

	arguments:
		dm:
			type:	DataMatrix

	keywords:
		nBin:
			desc:	The number of bins for `orthoVelPerc`.
			type:	int

	returns:
		type:	DataMatrix
	"""

	dm = dm.addField('orthoVel', dtype=float)
	dm = dm.addField('orthoVelPerc', dtype=float)
	for i in dm.range():
		startPos = dm['startPos'][i]
		if startPos in ['left', 'right']:
			posParams = vertVelParams
		else:
			posParams = horizVelParams
		a = tk.getTrace(dm[i], **posParams)
		orthoVel = np.nanmax(a)
		dm['orthoVel'][i] = orthoVel
	dm = dm.calcPerc('orthoVel', 'orthoVelPerc', ['subject_nr', 'startPos'],
		nBin=nBin)
	return dm

def addErrVel(dm, nBin=2):

	"""
	desc:
		Adds peak-velocity error information. That is, the mismatch between the
		peak velocity that is optimal to perceove the intrasaccadic percept, and
		the actual peak velocity.

	arguments:
		dm:
			type:	DataMatrix

	keywords:
		nBin:
			desc:	The number of bins for `errelPerc`.
			type:	int

	returns:
		type:	DataMatrix
	"""

	dm = dm.addField('errVel', dtype=float)
	dm = dm.addField('errVelPerc', dtype=float)
	for i in dm.range():
		peakVel = dm['_peakVel'][i]
		startPos = dm['startPos'][i]
		sf = dm['sf_%s' % startPos][i]
		optPeakVel = (.5/sf)/pxPerDeg*(1000/frameDur)
		d = abs(peakVel-optPeakVel)
		dm['errVel'][i] = d
	dm = dm.calcPerc('errVel', 'errVelPerc', keys=['subject_nr', 'startPos'],
		nBin=nBin)
	return dm

def plotOptimal(dm, saccDir='vert'):

	"""
	desc:
		Creates a pupil plot with only the trials that are best in terms
		of peak-velocity error and orthogonal velocity, based on a median split.

	arguments:
		dm:
			type:	DataMatrix

	keywords:
		saccDir:
			desc:	The saccade direction to analyze.
			type:	str
	"""

	dm = addErrVel(dm)
	dm = addOrthoVel(dm)
	dm = dm.select('errVelPerc == 0')
	dm = dm.select('orthoVelPerc == 0')
	dm = dm.select('saccDir == "vert"')
	pupil.pupilPlot(dm, suffix='.optimal', model='match + (1+match|subject_nr)')
