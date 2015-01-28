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

def ratingPlot(dm):

	"""
	desc:
		Creates a plot for the subjective ratings.

	arguments:
		dm:
			type:	DataMatrix
	"""

	rm = CsvReader('data/ratings.csv').dataMatrix()
	gm = np.mean(
		[rm['rating_%s' % startPos].mean() for startPos in startPositions])
	for startPos in startPositions:
		rm = rm.addField(startPos, dtype=float)
	for i in rm.range():
		# Subject mean
		sm = np.mean(
			[rm['rating_%s' % startPos][i] for startPos in startPositions])
		for startPos in startPositions:
			rm[startPos][i] = rm['rating_%s' % startPos][i] + gm - sm
	rm._print(sign=3)
	colors = allColors[:]
	Plot.new(size=tilePlot)
	for i in rm.range():
		color = colors.pop()
		for x, startPos in enumerate(startPositions):
			r = rm['rating_%s' % startPos][i]
			plt.plot(x-.2+i/25., r, '.', color=color)
	for x, startPos in enumerate(startPositions):
		r = rm[startPos].mean()
		se = 1.96*rm[startPos].std() / np.sqrt(len(rm))
		plt.bar(x-.4, r, edgecolor=blue[2], color='white')
		plt.errorbar(x, r, se, color=blue[2], capsize=0)
	plt.xlim(-1, 4)
	plt.ylim(1, 6)
	plt.xticks(range(0,4), saccadeDirections)
	plt.yticks(range(1,6))
	plt.xlabel('Saccade direction')
	plt.ylabel('Rating (0-5)')
	Plot.save('ratingPlot', folder='ratings', show=show)
