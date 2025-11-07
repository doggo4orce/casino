# python modules
import socket

# local modules
import config
import descriptor_data
import game_data
import object_data
import pc_data
import room_data
import string_handling
import zone_data

def create_test_object():
  obj = object_data.object_data()
  obj.name = "a sharp knife"
  obj.desc = "This knife looks extra sharp -- be careful!"
  obj.ldesc = "A sharp knife has been stuck into the ground here."
  obj.remove_all_aliases()
  obj.add_alias("sharp")
  obj.add_alias("knife")
  return obj

def create_test_players(number):
  # build return values
  players = list()
  clients = list()

  for j in range(0, number):
    host, client = socket.socketpair()

    # hook descriptor up to host side client
    d = descriptor_data.descriptor_data(host, f"{j}.localhost")

    # hook pc up to descriptor
    pc = pc_data.pc_data()
    pc.name = f"player{j}"
    pc.descriptor = d
    d.character = pc

    # append to return value lists
    players.append(pc)
    clients.append(client)

  return clients, players

def create_test_player():
  clients, players = create_test_players(1)
  return clients[0], players[0]

def create_single_room_test_world():
  mud = game_data.game_data()
  zone = zone_data.zone_data()
  zone.id = "zone_id"
  room = room_data.room_data()
  room.id = "room_id"
  room.zone_id = zone.id
  zone.add_room(room)
  mud.add_zone(zone)
  return mud, zone, room

def create_single_room_test_world_with_void():
  # find out where the VOIDROOM belongs according to config.py
  void_room, void_zone = string_handling.parse_reference(config.VOIDROOM)

  mud = game_data.game_data()
  zone = zone_data.zone_data()
  zone.id = void_zone
  room = room_data.room_data()
  room.id = void_room
  room.zone_id = zone.id
  zone.add_room(room)

  # now make the "single" room
  room = room_data.room_data()
  room.id = "room_id"
  room.zone_id = zone.id
  zone.add_room(room)
  mud.add_zone(zone)
  return mud, zone, room

def create_single_room_test_world_and_players(number):
  mud, zone, room = create_single_room_test_world()
  clients, players = create_test_players(number)
  return clients, players, mud, zone, room

def create_single_room_test_world_with_void_and_players(number):
  mud, zone, room = create_single_room_test_world_with_void()
  clients, players = create_test_players(number)
  return clients, players, mud, zone, room

def create_single_room_test_world_and_player():
  clients, players, mud, zone, room = create_single_room_test_world_and_players(1)
  return clients[0], players[0], mud, zone, room

def create_single_room_test_world_with_void_and_player():
  clients, players, mud, zone, room = create_single_room_test_world_with_void_and_players(1)
  return client[0], player[0], mud, zone, room
