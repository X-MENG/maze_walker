import pygame
import numpy as np
import os

class Room:
	def __init__(self, owner, gx, gy, tile):
		self.owner = owner;
		self.gx = gx;
		self.gy = gy;
		self.tile = tile;
		self.neighbours = [];
		self.explore_state = 0; # 0: unexplored, 1: explored, 2: marked

	def render(self):
		px, py = self.owner.gx_gy_to_px_py(self.gx, self.gy);
		self.owner.screen.blit(self.tile, (px, py));

class Gate:
	def __init__(self):
		self.pass_count = 0;

class Robot:
	def __init__(self, owner, img):
		self.owner = owner;
		self.img = img;
		self.gx = 0;
		self.gy = 0;
		self.img_size = 16;
		self.brain = Brain(self);

	def set_gx_gy(self, gx, gy):
		self.gx = gx;
		self.gy = gy;

	def __gx_gy_to_px_py(self, gx, gy):
		ppx, ppy = self.owner.gx_gy_to_px_py(gx, gy);
		px = ppx + self.img_size / 2;
		py = ppy + self.img_size / 2;
		return px, py;

	def render(self):
		px, py = self.__gx_gy_to_px_py(self.gx, self.gy);
		self.owner.screen.blit(self.img, (px, py));

class Brain:
	def __init__(self, owner):
		self.owner = owner;

class Main:
	def __init__(self):
		pygame.init();
		self.grid_size = 32;
		self.width = 640;
		self.height = 640;

		self.grid_width = self.width / self.grid_size;
		self.grid_height = self.height / self.grid_size;

		self.screen = pygame.display.set_mode((self.width, self.height), 0, 32);
		pygame.display.set_caption("maze walker");
		self.__cursor = pygame.image.load("res/Cursor.png");
		self.__blue_room = pygame.image.load("res/BlueRoom.png");
		self.__red_room = pygame.image.load("res/RedRoom.png");
		self.__yellow_room = pygame.image.load("res/YellowRoom.png");
		self.__robot = pygame.image.load("res/Robot.png");

		self.__cursor_pos = [0, 0];
		self.__mode = 0;
		self.__unexplored_list = [];
		self.__passed_list = [];
		self.__marked_list = [];
		self.__room_dict = {};
		self.__gate_dict = {};

		self.__robot = Robot(self, self.__robot);

		if os.path.exists("config.txt") == True:
			fp = open("config.txt", "r");
			txt = fp.readline();
			txt_list = txt.split(',');
			for item in txt_list:
				gindex = int(item);
				gx, gy = self.gindex_to_gx_gy(gindex);
				self.__room_dict[gindex] = Room(self, gx, gy, self.__blue_room);

			self.__update_gate_info();

			keys = list(self.__room_dict.keys());
			gidx = keys[3];
			gx, gy = self.gindex_to_gx_gy(gidx);
			self.__robot.set_gx_gy(gx, gy);

			#keys = list(self.__room_dict.keys());
			#print(keys);
			#print(self.__gate_dict);

	def gx_gy_to_px_py(self, gx, gy):
		px = gx * self.grid_size;
		py = gy * self.grid_size;

		return px, py;

	def px_py_to_gx_gy(self, px, py):
		gx = px // self.grid_size;
		gy = py // self.grid_size;

		return gx, gy;

	def px_py_to_gindex(self, px, py):
		gx, gy = self.px_py_to_gx_gy(px, py);
		gindex = self.gx_gy_to_gindex(gx, gy);

		return gindex;

	def gindex_to_gx_gy(self, gindex):
		gx = gindex % self.grid_size;
		gy = gindex // self.grid_size;
		return gx, gy;

	def gx_gy_to_gindex(self, gx, gy):
		gindex = gy * self.grid_size + gx;
		return gindex;

	def __add_neighbour(self, my_room_index, neighbour_room_index):
		if not my_room_index in self.__room_dict or not neighbour_room_index in self.__room_dict:
			return;

		my_room = self.__room_dict[my_room_index];
		neighbour_room = self.__room_dict[neighbour_room_index];

		if not neighbour_room_index in my_room.neighbours:
			my_room.neighbours.add(neighbour_room_index);

		if not my_room_index in neighbour_room.neighbours:
			neighbour_room.add(my_room_index);

	def __min_max(self, id_1, id_2):
		max_id = 0;
		min_id = 0;

		if id_1 > id_2:
			max_id = id_1;
			min_id = id_2;
		else:
			max_id = id_2;
			min_id = id_1;

		return min_id, max_id;

	def __get_gate_id_by_room(self, room1, room2):
		minRoom, maxRoom = self.__min_max(room1, room2);
		for k, v in self.__gate_dict.items():
			if v[0] == minRoom and v[1] == maxRoom:
				return k;

		return 0;

	def __add_gate(self, gate_index, room1, room2):
		if gate_index in self.__gate_dict:
			return;

		minRoom, maxRoom = self.__min_max(room1, room2);

		self.__gate_dict[gate_index] = [minRoom, maxRoom];

	def __update_gate_info(self):
		keys = list(self.__room_dict.keys());
		gate_index = 1;
		for gindex in keys:
			gx, gy = self.gindex_to_gx_gy(gindex);
			if gx - 1 >= 0:
				l_gindex = self.gx_gy_to_gindex(gx - 1, gy);
				if l_gindex in self.__room_dict:
					self.__add_gate(gate_index, gindex, l_gindex);
					gate_index = gate_index + 1;

			if gx + 1 < self.grid_width:
				r_gindex = self.gx_gy_to_gindex(gx + 1, gy);
				if r_gindex in self.__room_dict:
					self.__add_gate(gate_index, gindex, r_gindex);
					gate_index = gate_index + 1;

			if gy - 1 >= 0:
				u_gindex = self.gx_gy_to_gindex(gx, gy - 1);
				if u_gindex in self.__room_dict:
					self.__add_gate(gate_index, gindex, u_gindex);
					gate_index = gate_index + 1;

			if gy + 1 < self.grid_height:
				d_gindex = self.gx_gy_to_gindex(gx, gy + 1);
				if d_gindex in self.__room_dict:
					self.__add_gate(gate_index, gindex, d_gindex);
					gate_index = gate_index + 1;

	def __update_editor_mode(self):
		for v in self.__room_dict.values():
			v.render();

		self.screen.blit(self.__cursor, self.__cursor_pos);


	def __update_explore_mode(self):
		for v in self.__room_dict.values():
			v.render();

		self.__robot.render();

	def __change_mode(self, new_mode):
		if self.__mode == new_mode:
			return;

		if new_mode == 0:
			self.__exit_explore_mode();
		elif new_mode == 1:
			self.__exit_editor_mode();

		self.__mode = new_mode;

	def __exit_editor_mode(self):
		pass;

	def __exit_explore_mode(self):
		pass;

	def __move_left(self):
		new_x = self.__cursor_pos[0] - self.grid_size;
		if new_x >= 0:
			self.__cursor_pos[0] = new_x;

	def __move_right(self):
		new_x = self.__cursor_pos[0] + self.grid_size;
		if new_x < self.width:
			self.__cursor_pos[0] = new_x;

	def __move_up(self):
		new_y = self.__cursor_pos[1] - self.grid_size;
		if new_y >= 0:
			self.__cursor_pos[1] = new_y;

	def __move_down(self):
		new_y = self.__cursor_pos[1] + self.grid_size;
		if new_y < self.height:
			self.__cursor_pos[1] = new_y;

	def __message_process(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit();
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.__move_left();
				elif event.key == pygame.K_RIGHT:
					self.__move_right();
				elif event.key == pygame.K_UP:
					self.__move_up();
				elif event.key == pygame.K_DOWN:
					self.__move_down();
				elif event.key == pygame.K_0:
					# 切换到explore_mode
					self.__change_mode(0);
				elif event.key == pygame.K_1:
					# 切换到editor_mode
					self.__change_mode(1);
				elif event.key == pygame.K_F1:
					items = list(self.__room_dict.keys());
					index = 0;
					outputStr = "";
					for k in items:
						if index > 0:
							outputStr = outputStr + ",";
						
						outputStr = outputStr + str(k);
						index = index + 1;

					fp = open("config.txt", "w");
					fp.write(outputStr);
					fp.close();
					print("saved!");
				elif event.key == pygame.K_SPACE:
					px, py = self.__cursor_pos;
					gx, gy = self.px_py_to_gx_gy(px, py);
					gindex = self.gx_gy_to_gindex(gx, gy);

					if not gindex in self.__room_dict:
						# 添加元素
						room = Room(self, gx, gy, self.__blue_room);
						self.__room_dict[gindex] = room;
					else:
						# 删除元素
						del self.__room_dict[gindex];
	def update(self):
		while True:
			self.__message_process();
			self.screen.fill((0, 0, 0));
			if self.__mode == 0:
				# 编辑模式
				self.__update_editor_mode();
			else:
				# 探索模式
				self.__update_explore_mode();

			pygame.display.update();

if __name__ == '__main__':
	game = Main();
	game.update();