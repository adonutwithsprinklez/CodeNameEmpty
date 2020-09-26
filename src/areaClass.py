import copy
import random
import math

from dieClass import rollDice
from enemyClass import Enemy
from eventClass import Event
from itemGeneration import generateName

# Hostility will range 1-10
# Hostility affects how close to player strength enemys will be
# 0   = No hostiles
# 1-3 = below
# 4-6 = equal
# 7-9 = above
# 10  = Much higher
# This not only will affect strength but also rewards, with higher hostility giving better rewards.

class Area(object):
	def __init__(self,areaType,debug = 0,**kwargs):
		self.name = generateName(areaType)
		self.desc = random.choice(areaType["desc"])
		self.newArea = random.randint(areaType["minNewAreas"],areaType["maxNewAreas"])
		self.newAreaTypes = areaType["areas"]
		self.aType = areaType["aType"]
		self.enemy = []
		self.event = None
		self.npc = None
		self.hostility = random.randint(areaType["hostilityMin"],areaType["hostilityMax"])

		self.kwargs = kwargs

		chance = random.randint(0,areaType["eventChance"])
		# chance = 3
		if chance < 5 and chance != 0 and len(areaType["events"])>0:
			self.event = self.chooseAnEvent(areaType)

		# ENEMY GENERATION
		# MUST BE DEDONE
		chance = areaType["enemyChance"]
		enemies = []
		c = math.pow(15,(self.hostility-2.0)/10.0)
		for enemy, echance in areaType["enemies"]:
			enemies+=[enemy]*echance
		for i in range(0,10):
			if len(self.enemy)<self.hostility:
				x = random.random()*chance
				if x<c:
					self.enemy.append(random.choice(enemies))

		chance = random.randint(0,areaType["npcChance"])
		if chance < 10 and chance != 0 and len(areaType["npcs"])>0:
			self.npc = random.choice(areaType["npcs"])
		
	def chooseAnEvent(self, areaType):
		areaChoices = areaType["events"][::]
		currentEvent = areaChoices[0]
		highRoll = rollDice(currentEvent[1])
		for event in areaChoices[1:]:
			newRoll = rollDice(event[1])
			if newRoll > highRoll:
				currentEvent = event
				highRoll = newRoll
		return currentEvent[0]

	def load(self,weapons,armor,misc,enemies,npcs,events,modifiers):
		# Loads in the enemies and events with any objects that they may need
		if self.enemy != []:
			e = []
			for enemy in self.enemy:
				newEnemy = Enemy(enemies[enemy],weapons,armor,misc,modifiers)
				e.append(newEnemy)
			self.enemy = e
		if self.event:
			self.event = Event(events[self.event])
