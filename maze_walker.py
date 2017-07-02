import pygame
import os
import math
import random

class Room:
	def __init__(self, owner, gx, gy, tile):
		self.owner = owner;
		self.gx = gx;
		self.gy = gy;
		self.__tile = tile;
		self.neighbours = [];
		self.score = -1;	#-1: unexplored, 0: explored, >0: marked

	def render(self):
		px, py = self.owner.gx_gy_to_px_py(self.gx, self.gy);
		self.owner.screen.blit(self.__tile, (px, py));

class Gate:
	def __init__(self, owner, connected_room):
		self.owner = owner;
		self.pass_count = 0;
		self.connected_room = connected_room;
		self.q = {};
		self.q[(connected_room[0], connected_room[1])] = 0;
		self.q[(connected_room[1], connected_room[0])] = 0;

	def get_r(self, from_room_index, to_room_index):
		from_room = None;
		to_room   = None;
		if from_room_index in self.connected_room:
			from_room = self.owner.room_dict[from_room_index];

		if to_room_index in self.connected_room:
			to_room = self.owner.room_dict[to_room_index];

		if from_room = None or to_room = None:
			return 0;

		r = to_room.score - from_room.score;

		if r < 0:
			r = 0;

		return r;



	def add_pass_count(self):
		self.pass_count = self.pass_count + 1;

class Robot:
	def __init__(self, owner, img):
		self.owner = owner;
		self.__img = img;
		self.__begin_gx = 0;
		self.__begin_gy = 0;
		self.__begin_px = 0;
		self.__begin_py = 0;
		self.__cur_px = 0;
		self.__cur_py = 0;
		self.__end_gx = 0;
		self.__end_gy = 0;
		self.__end_px = 0;
		self.__end_py = 0;
		self.__img_size = 16;
		self.__brain = Brain(self);
		self.__enable_move = False;
		self.__direction = (0, 0);
		self.speed = 5;
		self.__dist = 0;

	def get_cur_gx_gy(self):
		gx, gy = self.owner.px_py_to_gx_gy(self.__cur_px, self.__cur_py);
		return gx, gy;

	def set_begin_gx_gy(self, gx, gy):
		self.__begin_gx = gx;
		self.__begin_gy = gy;

		self.__begin_px, self.__begin_py = self.__gx_gy_to_px_py(self.__begin_gx, self.__begin_gy);

		self.__cur_px = self.__begin_px;
		self.__cur_py = self.__begin_py;

	def set_end_gx_gy(self, gx, gy):
		self.__end_gx = gx;
		self.__end_gy = gy;

		self.__end_px, self.__end_py = self.__gx_gy_to_px_py(self.__end_gx, self.__end_gy);

	def start():
		dx = self.__end_gx - self.__end_gx;
		dy = self.__end_gy - self.__end_gy;

		mag = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2));

		self.__direction = (dx / mag, dy / mag);
		self.__dist = math.sqrt(math.pow(self.__end_px - self.__begin_px, 2) + math.pow(self.__end_py - self.__begin_py, 2));
		self.__enable_move = True;


	def __gx_gy_to_px_py(self, gx, gy):
		ppx, ppy = self.owner.gx_gy_to_px_py(gx, gy);
		px = ppx + self.__img_size / 2;
		py = ppy + self.__img_size / 2;
		return px, py;

	def update(self):
		if self.__enable_move == True:
			self.owner.screen.blit(self.__img, (self.__cur_px, self.__cur_py));
			delta_time = self.owner.clock.tick() / 1000;
			self.__cur_px = self.__cur_px + self.speed * self.__direction[0] * delta_time;
			self.__cur_py = self.__cur_py + self.speed * self.__direction[1] * delta_time;

			cur_dist = math.sqrt(math.pow(self.__cur_px - self.__begin_px, 2) + math.pow(self.__cur_py - self.__begin_py, 2));
			if cur_dist - self.__dist > 0:
				self.__enable_move = False;
				begin_gindex = self.owner.gx_gy_to_gindex(self.__begin_gx, self.__begin_gy);
				end_gindex = self.owner.gx_gy_to_gindex(self.__end_gx, self.__end_gy);

				gate_id = self.owner.pass_gate(begin_gindex, end_gindex);

				self.__brain.make_descision();

class Brain:
	def __init__(self, owner):
		self.owner  = owner;
		self.main   = owner.owner;
		self.factor = 0.8;

	def roulette(self, roulette_list):
		prob_list = [];
		s = sum(roulette_list);

		for r in roulette_list:
			prob_list.add(r / s);

		r = random.randomint(1, 100) / 100;

		s = 0;
		idx = -1;
		for p in prob_list:
			s = s + p;
			if s >= r:
				return idx;
			idx = idx + 1;

		return idx;

	def make_descision(self):
		gx, gy = self.owner.get_cur_gx_gy();
		cur_index = self.main.gx_gy_to_gindex(gx, gy);
		cur_room = self.main.room_dict[cur_index];

		normal_neighbours = [];

		rand_list = [];
		for n_index in cur_room.neighbours:
			gate_id = self.main.get_gate_id_by_room(cur_index, n_index);
			gate = self.main.gate_dict[gate_id];
			rand_list.add(gate.pass_count + 1);
		idx = self.roulette(rand_list);
		target_room_index = cur_room.neighbours[idx];

		target_room = self.main.room_dict[target_room_index];

		max_q_room = None;
		max_q = -9999;

		for n in target_room.neighbours:
			n_room = self.main.room_dict[n];
			target_nei_index = self.main.gx_gy_to_gindex(n_room.gx, n_room.gy);
			gate_id = self.main.get_gate_id_by_room(target_room_index, target_nei_index);
			gate = self.main.gate_dict[gate_id];
			q = gate.q[(target_room_index, target_nei_index)];
			if q > max_q:
				max_q = q;
				max_q_room = n_room;

		max_q_room_index = self.main.gx_gy_to_gindex(max_q_room.gx, max_q_room.gy);
		gate_id = self.main.get_gate_id_by_room(cur_index, max_q_room_index);
		gate = self.main.gate_dict[gate_id];
		r = gate.get_r(cur_index, max_q_room_index);

		new_q = r + self.factor * max_q;
		gate.q[(cur_index, nei_index)]  = new_q;
		
		self.owner.set_end_gx_gy(max_q_room.gx, max_q_room.gy);
		self.owner.start();

class Main:
	def __init__(self):
		pygame.init();
		self.grid_size = 32;
		self.width = 640;
		self.height = 640;
		self.clock = pygame.time.Clock();
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
		self.__mode = 1;	#1: editor mode; 2: explore mode
		self.__unexplored_list = [];
		self.__passed_list = [];
		self.__marked_list = [];
		self.room_dict = {};
		self.gate_dict = {};

		self.__begin_gindex = 0;
		self.__end_gindex = 0;

		self.__robot = Robot(self, self.__robot);

		if os.path.exists("config.txt") == True:
			fp = open("config.txt", "r");
			txt = fp.readline();
			txt_list = txt.split(',');
			for item in txt_list:
				gindex = int(item);
				gx, gy = self.gindex_to_gx_gy(gindex);
				self.room_dict[gindex] = Room(self, gx, gy, self.__blue_room);

			self.__update_gate_info();

			keys = list(self.room_dict.keys());
			gidx = keys[3];
			gx, gy = self.gindex_to_gx_gy(gidx);
			self.__robot.set_begin_gx_gy(gx, gy);

	def pass_gate(self, begin_gate_index, end_gate_index):
		gate_index = self.get_gate_id_by_room(begin_gate_index, end_gate_index);
		if gate_index in self.gate_dict:
			gate = self.gate_dict[gate_index];
			gate.add_pass_count();

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

	def gindex_to_px_py(self, gindex):
		gx, gy = self.gindex_to_gx_gy(gindex);
		px, py = self.gx_gy_to_px_py(gx, gy);
		return px, py;

	def gindex_to_gx_gy(self, gindex):
		gx = gindex % self.grid_size;
		gy = gindex // self.grid_size;
		return gx, gy;

	def gx_gy_to_gindex(self, gx, gy):
		gindex = gy * self.grid_size + gx;
		return gindex;

	def __add_neighbour(self, my_room_index, neighbour_room_index):
		if not my_room_index in self.room_dict or not neighbour_room_index in self.room_dict:
			return;

		my_room = self.room_dict[my_room_index];
		neighbour_room = self.room_dict[neighbour_room_index];

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

	def get_gate_id_by_room(self, room1, room2):
		min_room, max_room = self.__min_max(room1, room2);
		for k, v in self.gate_dict.items():
			if v[0] == min_room and v[1] == max_room:
				return k;

		return 0;

	def __add_gate(self, gate_index, room1, room2):
		if gate_index in self.gate_dict:
			return;

		min_room, max_room = self.__min_max(room1, room2);

		gate = Gate(self, [min_room, max_room]);
		self.gate_dict[gate_index] = gate;

	def __update_gate_info(self):
		keys = list(self.room_dict.keys());
		gate_index = 1;
		for gindex in keys:
			gx, gy = self.gindex_to_gx_gy(gindex);
			if gx - 1 >= 0:
				l_gindex = self.gx_gy_to_gindex(gx - 1, gy);
				if l_gindex in self.room_dict:
					self.__add_gate(gate_index, gindex, l_gindex);
					gate_index = gate_index + 1;

			if gx + 1 < self.grid_width:
				r_gindex = self.gx_gy_to_gindex(gx + 1, gy);
				if r_gindex in self.room_dict:
					self.__add_gate(gate_index, gindex, r_gindex);
					gate_index = gate_index + 1;

			if gy - 1 >= 0:
				u_gindex = self.gx_gy_to_gindex(gx, gy - 1);
				if u_gindex in self.room_dict:
					self.__add_gate(gate_index, gindex, u_gindex);
					gate_index = gate_index + 1;

			if gy + 1 < self.grid_height:
				d_gindex = self.gx_gy_to_gindex(gx, gy + 1);
				if d_gindex in self.room_dict:
					self.__add_gate(gate_index, gindex, d_gindex);
					gate_index = gate_index + 1;

	def __update_editor_mode(self):
		for v in self.room_dict.values():
			v.render();

		self.screen.blit(self.__cursor, self.__cursor_pos);

		if self.__begin_gindex > 0:
			px, py = self.gindex_to_px_py(self.__begin_gindex);
			self.screen.blit(self.__yellow_room, (px, py));

		if self.__end_gindex > 0:
			px, py = self.gindex_to_px_py(self.__end_gindex);
			self.screen.blit(self.__red_room, (px, py));

	def __update_explore_mode(self):
		for v in self.room_dict.values():
			v.render();

		self.__robot.update();

	def __change_mode(self, new_mode):
		if self.__mode == new_mode:
			return;

		if new_mode == 1:
			self.__exit_explore_mode();
			self.__enter_editor_mode();
		elif new_mode == 2:
			self.__exit_editor_mode();
			self.__enter_explore_mode();

		self.__mode = new_mode;

	def __enter_editor_mode(self):
		self.__begin_gindex = 0;
		self.__end_gindex = 0;

	def __exit_editor_mode(self):
		pass;

	def __enter_explore_mode(self):
		keys = list(self.room_dict.keys());

		self.__unexplored_list = [];
		self.__passed_list = [];
		self.__marked_list = [];

		for k in keys:
			if k == self.__begin_gindex:
				self.__passed_list.add(k);
			elif k == self.__end_gindex:
				self.__marked_list.add(k);
			else:
				self.__unexplored_list.add(k);
		begin_gx, begin_gy = self.gindex_to_gx_gy(self.__begin_gindex);

		if self.__begin_gindex in self.room_dict:
			room = self.room_dict[self.__begin_gindex];
			room.score = 0;

		if self.__end_gindex in self.room_dict:
			room = self.room_dict[self.__end_gindex];
			room.score = 100;

		self.__robot.set_begin_gx_gy(begin_gx, begin_gy);
		self.__robot.make_descision();

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

	def __explore_mode_message_process(self, event):
		if event.key == pygame.K_0:
			# 切换到editor_mode
			self.__change_mode(0);

	def __editor_mode_message_process(self, event):
		if event.key == pygame.K_LEFT:
			self.__move_left();
		elif event.key == pygame.K_RIGHT:
			self.__move_right();
		elif event.key == pygame.K_UP:
			self.__move_up();
		elif event.key == pygame.K_DOWN:
			self.__move_down();
		elif event.key == pygame.K_1:
			# 切换到explore_mode
			self.__change_mode(1);
		elif event.key == pygame.K_F1:
			items = list(self.room_dict.keys());
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

			if not gindex in self.room_dict:
				# 添加元素
				room = Room(self, gx, gy, self.__blue_room);
				self.room_dict[gindex] = room;
			else:
				# 删除元素
				del self.room_dict[gindex];
		elif event.key == pygame.K_b:
			px, py = self.__cursor_pos;
			self.__begin_gindex = self.px_py_to_gindex(px, py);

			if self.__begin_gindex in self.room_dict:
				begin_room = self.room_dict[self.__begin_gindex];

		elif event.key == pygame.K_e:
			px, py = self.__cursor_pos;
			self.__end_gindex = self.px_py_to_gindex(px, py);

	def __message_process(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit();
			elif event.type == pygame.KEYDOWN:
				if self.__mode == 1:
					self.__editor_mode_message_process(event);
				elif self.__mode == 2:
					self.__explore_mode_message_process(event);
	def update(self):
		while True:
			self.__message_process();
			self.screen.fill((0, 0, 0));
			if self.__mode == 1:
				# 编辑模式
				self.__update_editor_mode();
			elif self.__mode == 2:
				# 探索模式
				self.__update_explore_mode();

			pygame.display.update();

if __name__ == '__main__':
	game = Main();
	game.update();