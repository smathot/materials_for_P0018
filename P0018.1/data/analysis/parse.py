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

class DryReader(EyelinkAscFolderReader):
	def initTrial(self, trialDict):
		self.trialId = trialDict['trialId']
	def parseLine(self, trialDict, l):
		trialDict['trialId'] = self.trialId

class MyReader(EyelinkAscFolderReader):

	"""An experiment-specific reader to parse the EyeLink data files."""

	def endTrial(self, l):

		return 'RECCFG' in l

	def initTrial(self, trialDict):

		"""
		desc:
			Performs pre-trial initialization.

		arguments:
			trialDict:
				desc:	Trial information.
				type:	dict
		"""

		global dryrun
		self.trialId = trialDict['trialId']
		self.trialDm = dryrun.select('trialId == %d' % self.trialId,
			verbose=False).select('file == "%s"' % trialDict['file'],
			verbose=False)
		assert(len(self.trialDm) == 1)
		self.startPos = self.trialDm['startPos'][0]
		self.checkFix = 0
		trialDict['saccLat'] = None
		trialDict['saccVel'] = 0
		self._sample = None
		self.inSacc = False
		self.cueTime = None
		self.saccTime = None
		self.baselineTime = None
		self.saccVel = []
		self.n = 0
		self.minN = 10

	def finishTrial(self, trialDict):

		"""
		desc:
			Performs post-trial initialization.

		arguments:
			trialDict:
				desc:	Trial information.
				type:	dict
		"""

		if trialDict['driftDir'] == 'horiz':
			if trialDict['startPos'] in ['left', 'right']:
				trialDict['match'] = 1
			else:
				trialDict['match'] = 0
		if trialDict['driftDir'] == 'vert':
			if trialDict['startPos'] in ['left', 'right']:
				trialDict['match'] = 0
			else:
				trialDict['match'] = 1
		trialDict['subject_nr'] = trialDict['file'][2:4]
		if 'sacc' in self.traceDict and len(self.traceDict['sacc']) > 0:
			trialDict['hasSaccTrace'] = 1
		else:
			trialDict['hasSaccTrace'] = 0
		if 'cue' in self.traceDict and len(self.traceDict['cue']) > 0:
			trialDict['hasCueTrace'] = 1
		else:
			trialDict['hasCueTrace'] = 0
		trialDict['saccVel'] = np.mean(self.saccVel)
		trialDict['saccLat'] = self.saccTime - self.cueTime
		print trialDict['saccLat'], self.startPos

	def parseStartTracePhase(self, l):

		"""
		descL
		Checks whether a new trace phase is started.

		Arguments:
		l	--	A list.
		"""

		if 'baseline' in l:
			self.tracePhase = 'baseline'
			self.baselineTime = l[1]

	def parseLine(self, trialDict, l):

		"""
		desc:
			Parses a single line from the EyeLink .asc file.

		arguments:
			trialDict:
				desc:	Trial information.
				type:	dict
			l:
				desc:	A white-space-splitted line.
				type:	list
		"""

		if self.inSacc:
			self.tracePhase = 'sacc'

		trialDict['trialId'] = self.trialId
		if 'phase' in l and 'cue' in l:
			self.cueTime = l[1]

		# Keep track of sample to sample velocity
		s = self.toSample(l)
		if s != None:
			if self._sample != None:
				self.vel = np.sqrt((self._sample['x']-s['x'])**2 \
					+ (self._sample['y']-s['y'])**2)
			self._sample = s

		# Detect saccades
		if s != None and self.baselineTime != None \
			and s['time'] - self.baselineTime > 100 and not self.inBlink \
			and not self.inSacc:
			if self.startPos == 'left':
				saccStart = s['x'] > xc
			elif self.startPos == 'right':
				saccStart = s['x'] < xc
			elif self.startPos == 'top':
				saccStart = s['y'] < yc
			elif self.startPos == 'bottom':
				saccStart = s['y'] > yc
			else:
				raise Exception('Invalid startpos')
			if saccStart:
				if self.n < self.minN:
					self.n += 1
				else:
					self.inSacc = True
					self.traceDict['sacc'] = \
						self.traceDict['baseline'][-lookback:]
					if len(self.traceDict['sacc']) < lookback:
						print 'Not enough baseline, padding %d' \
							% (lookback-len(self.traceDict['sacc']))
						self.traceDict['sacc'] = \
							[(np.nan, np.nan, np.nan)] \
							*(lookback-len(self.traceDict['sacc'])) \
							+ self.traceDict['sacc']
					assert(len(self.traceDict['sacc']) == lookback)
					self.traceDict['baseline'] = \
						self.traceDict['baseline'][:-lookback]
					self.saccVel.append(self.vel)
					self.saccTime = s['time']
					self.tracePhase = 'sacc'

		# Detect saccade errors
		if not self.inBlink and self.inSacc \
			and len(self.traceDict['sacc']) > 50:
			s = self.toSample(l)
			if s != None:
				if self.startPos == 'left':
					error = s['x'] < xc
				elif self.startPos == 'right':
					error = s['x'] > xc
				elif self.startPos == 'top':
					error = s['y'] > yc
				elif self.startPos == 'bottom':
					error = s['y'] < yc
				else:
					raise Exception('Invalid startpos')
				if error:
					self.traceDict['sacc'] = self.traceDict['sacc'][:-50]
					self.tracePhase = None

@cachedDataMatrix
def getDryRun():
	return DryReader(maxN=maxN, path='data/events').dataMatrix()

@cachedDataMatrix
def getDataMatrix():

	global dryrun
	dryrun = getDryRun(cacheId='dryrun')
	return MyReader(blinkReconstruct=True, maxN=maxN,
		requireEndTrial=False, path='data/samples+events').dataMatrix()
