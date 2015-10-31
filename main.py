from models.person import *
from models.room import *
import re
from random import choice


class Building(object):

	def __init__(self):
		"""initialization of Offices and Living spaces with people to be allocated.
		Setting the arrays of each space to be empty and to be filled.
		"""
		self.spaces = {
			'offices': [],
			'livingspaces': []
		}

		self.filled_spaces = {
			'offices': [],
			'livingspaces': []
		}

		self.unallocated_people = {

			'offices': [],
			'livingspaces':[],

		}
		self.allocated_people = {
		'offices':[],
		'livingspaces':[]
		}
		self.employees = []

	def add_people_from_files(self,path):
		"""this utility function reads from the input file
		strip the tabs seperate it into dictionaries and append it to the employess array
		@params path to file
		returns lists
		"""
		offset = len(self.employees) - 1 if self.employees else 0
		with open(path,"r") as input_file:
			file_contents = input_file.read().splitlines()

		for line in file_contents:
			temp =  re.split(r'\t+', line.rstrip('\t'))

			
			person = Fellow(unicode(temp[0], errors='ignore')) if temp[1] == "FELLOW" else Staff(unicode(temp[0], errors='ignore'))

			if 2 < len(temp):
				person.set_livingspace(temp[2])
			self.employees.append(person)

		for person in self.employees[offset:]:
			self.add_person_to_room(person)

	
	def add_office(self, room_name):
		""" This adds more office 
		@params office name
		@return void
		"""

		room = Office(room_name)
		self.spaces['offices'].append(room)

	def add_livingspace(self, room_name):
		""" This adds more living space
		@params living room name
		@return void
		"""

		room = Living(room_name)
		self.spaces['livingspaces'].append(room)

	def populate_spaces_with_rooms(self, populate_number=10):
		""" This auto populates the offices and the living spaces in the andela classes
		it poplates both the room and the office from 1 - 10 
		"""
		for i in range(1, populate_number+1):

			self.add_office("ROOM " + str(i))
			self.add_livingspace("ROOM " + str(i))

	def allocate_to_space(self, person, space_type):
		"""

		"""
		room = self.check_and_return_avaialable_space(space_type)
		_class = Living if isinstance(room, Living) else Office
		if isinstance(room, Room):
			room.add_person(person)
			self.allocated_people[space_type].append(person)
		else:
			print "{} Could not be allocated to a {}".format(person.name, space_type)
			self.unallocated_people[space_type].append(person)

	def add_person_to_room(self, person):
		""" this is the function that gets called each time a fellow or a staff is to be randomly assigned to an office or a room
		it made use of the recursive method check_if_room_is_filled()
		@params person's dictionary, option only availale for fellows(Y for living space no for none)
		(might change, thinking if dictionary should be an elegant way of executing this)
		"""

		self.allocate_to_space(person, 'offices')


		# This randomly assigns living spaces for fellows that have an option of living space
		if isinstance(person,Fellow) and person.wants_livingspace is "Y":
			self.allocate_to_space(person, "livingspaces")


	def check_and_return_avaialable_space(self, space_type):
		""" This is a recursive function to randomly allocate living space and offices for staffs and fellows alike 
		This append filled rooms to self.filled_offices or self.filled_livings respectively
		@returns instace of Office or Living if there are spaces left
		@returns string if there isn't
		@params space_type(offices or livings)
		"""
		if self.spaces[space_type]:
			room = choice(self.spaces[space_type])
			if not room.is_filled():
				return room
			else:
				self.spaces[space_type].remove(room)
				self.filled_spaces[space_type].append(room)
				return self.check_and_return_avaialable_space(space_type)
		else:
			return None;

	def print_occupants_names(self, space_type):
		"""get the number of people allocated to all the living on a print_living_name
		no @params needed
		"""
		for space in self.filled_spaces[space_type]:
				print  "\n" + str(space)
				print space.get_people()
		for space in self.spaces[space_type]:
			print  "\n" + str(space)
			print space.get_people()

	def get_all_rooms_and_occupants(self):
		""" Returns all the occupants Room names Offices Names in Amity
		"""
		self.print_occupants_names("offices")
		self.print_occupants_names("livingspaces")

	def get_total_occupants(self, space_type, name):
		""" This is to get the total occupants of a particular room
		the params needed are the space_type which can either be offices or living space
		Then the name of the room range from 1 - 10
		for eg andela.get_total_occupants("office","2") gets the total number of offices in ROOM 2 (Office)
		"""
		room = self.find_room(space_type, name)
		if isinstance(room,Room):
			if room.get_people():
				print "\n" + str(room) + " Occupants"
				print room.get_people()
			else:
				print "No Occupant in this room"
		else:
			print "Invalid room name"
	
	def get_info_of_worker(self, person_name, space_type, number):
		"""

		"""
		room = self.find_room(space_type,number)
		if room:
			for person in room.people:
				if person_name == person.name:
					return person.get_info()

	def find_room(self, space_type, number):
		""" This is a utility function to get a particular room properties in amity
		@params space_type(office or living), room number
		@returns instace of ROOM
		"""
		for room in self.spaces[space_type]:
				if number == room.name:
					return room
		for room in self.filled_spaces[space_type]:
				if number == room.name:
					return room

	def get_unallocated_employee_for_office(self):
		""" Get the number of people that are yet to be allocated to an office
		@params none
		@returns strings of names / a string passing in the error
		"""
		print "\n" + "Unallocated people for office space"
		return ', '.join([person.name for person in self.unallocated_people['offices']]) if len(self.unallocated_people['offices']) > 0 else  "No Unallocated Fellows\Staffs for Office Space"
	
	def get_unallocated_employee_for_living(self):
		"""Returns the number of fellows that are yet to be allocated living spaces
		@params none
		@return string of names

		"""
		print "\n" + "Unallocated people for living space"
		return ', '.join([person.name for person in self.unallocated_people['livingspaces']]) if len(self.unallocated_people['livingspaces']) > 0 else  "No Unallocated Fellow\Staffs for Living Space"

if __name__ == '__main__':
    andela = Building()
    andela.populate_spaces_with_rooms()
    andela.add_office("Undefined")
    andela.add_office("Elixir")
    andela.add_livingspace("Tinker")
    andela.add_livingspace("Compass")
    andela.add_people_from_files("data/input.txt")
    andela.get_all_rooms_and_occupants()
    andela.get_total_occupants("offices","ROOM 2")
    andela.get_info_of_worker("ANDREW PHILLIPS","offices","ROOM 2")
    print andela.get_unallocated_employee_for_office()
    print andela.get_unallocated_employee_for_living()


