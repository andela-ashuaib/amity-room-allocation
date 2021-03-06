
"""This is the model class for Amity"""
class Room(object):

	def __init__(self, name):
		""" initialize the function with room name only
		"""
		self.name = name
		self.people = []

	def get_people(self):
		""" gets the number of occupants for this office/living space and returns them in a string
		"""
		return ', '.join([people.name for people in self.people])

	def add_person(self, person):
		""" This utility method add person to the room
		@params instace of People
		"""
		if not self.is_filled():
			self.people.append(person)
			if isinstance(self, Office):
				person.set_office(str(self))
			else:
				person.set_living(str(self))
		else:
			print "No more spaces in this room"
	
	def is_filled(self):
		""" Checks if this room is avaialble 
		"""
		if len(self.people) < self.max_people:
			return False
		else:
			return True




class Office(Room):
	
	def __init__(self, name, max_people=6):
		"""
		This calls the super class to set the maximum number of people needed
		for this office
		"""
		super(Office,self).__init__(name)
		self.max_people = max_people
	
	def __str__(self):
		""" Changes the way this room displays to the format
		e.g ROOM 1 (Office)
		"""
		return self.name + " (Office)"

	

	
class Living(Room):
	def __init__(self, name, max_people=4):
		"""This calls the super class to set the maximum number of people needed
		for this room
		"""
		super(Living,self).__init__(name)
		self.max_people = max_people
	
	def __str__(self):
		""" Changes the way this room displays to the format
		e.g ROOM 1 (Living)
		"""
		return self.name + " (Living)"
