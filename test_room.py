import room
import unittest

# I wrote this to explore the unittest module.  I'm not sure what tests would belong here...
class TestRoom(unittest.TestCase):

	def setUp(self):
		self.room = { }

		self.room[0] = room.room()
		
		for dir in room.direction:
			self.room[0]

		self.room[1] = room.room()
		self.room[1].vnum = 0
		self.room[1].name = "Outside the Inn"
		self.room[1].desc = "  Warm light from the fireplace can be seen within the inn."
		self.room[1].connect(room.direction.EAST, 2)

		self.room[2] = room.room()
		self.room[2].vnum = 1
		self.room[2].name = "Inside the Inn"
		self.room[2].desc = "  The inn is toasty warm by the fire."
		self.room[2].connect(room.direction.WEST, 1)

	def test_connections(self):
		index = self.room[1].get_destination(room.direction.EAST)
		rm = self.room[index]
		self.assertIs(rm, self.room[2])

	def tearDown(self):
		pass

	def test(self):
		print(f"{self.room[1].name}")
		print(f"{self.room[1].desc}")
		print(f"{self.room[1].show_exits()}")

		print(f"{self.room[2].name}")
		print(f"{self.room[2].desc}")
		print(f"{self.room[2].show_exits()}")

if __name__ == '__main__':
	unittest.main()