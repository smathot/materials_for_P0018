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

q1 = 'match == 1'
q2 = 'match == 0'

@cachedArray
def subjectDiffTraces(dm):

	pupil = np.empty( (dm.count('subject_nr'), traceParams['traceLen']),
		dtype=float)
	for i, (subject_nr, _dm) in enumerate(dm.walk('subject_nr')):
		x1, y1, err1 = tk.getTraceAvg(_dm.select(q1, verbose=False),
			**traceParams)
		x2, y2, err2 = tk.getTraceAvg(_dm.select(q2, verbose=False),
			**traceParams)
		pupil[i] = y2-y1
	return pupil

def corrTrace(dm):

	rm = CsvReader('data/ratings.csv').dataMatrix()
	print(rm)
	behav = np.empty(dm.count('subject_nr'), dtype=float)
	for i, (subject_nr, _dm) in enumerate(rm.walk('subject_nr')):
		behav[i] = rm['rating_mean'][i]
	pupil = subjectDiffTraces(dm) #, cacheId='.subjectDiffTraces')
	ar = np.empty(traceParams['traceLen'], dtype=float)
	ap = np.empty(traceParams['traceLen'], dtype=float)
	for _i in range(pupil.shape[1]):
		s, i, r, p, se = linregress(behav, pupil[:,_i])
		ar[_i] = r
		ap[_i] = p
	# Create an example plot for the strongest correlation
	iMax = np.argmax(ar)
	x = behav
	y = pupil[:,iMax]
	Plot.regress(x, y)
	plt.title('Sample: %d' % iMax)
	Plot.save('corrExample', folder='corr')
	return ar, ap

def corrPlot(dm):

	ar, ap = corrTrace(dm)
	Plot.new(Plot.r)
	plt.subplot(211)
	plt.xlabel('Time (ms)')
	plt.ylabel('R(pupil - rating)')
	plt.plot(ar, color=orange[1], label='memory')
	plt.axhline(0, linestyle=':', color='black')
	plt.ylim(-1,1)
	plt.xlim(0, traceLen)
	plt.xticks(range(100, traceParams['traceLen'], 200),
		range(100-lookback, traceParams['traceLen']-lookback, 200))	
	plt.subplot(212)
	plt.xlabel('Time (ms)')
	plt.ylabel('P value for R')
	plt.axhline(.05, linestyle=':', color='black')
	plt.plot(ap, color=blue[1], label='memory')
	plt.legend(frameon=False)
	plt.xlim(0, traceLen)
	plt.xticks(range(100, traceParams['traceLen'], 200),
		range(100-lookback, traceParams['traceLen']-lookback, 200))
	Plot.save('corrTrace',  show=show, folder='corr')
