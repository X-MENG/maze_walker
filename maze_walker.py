import pygame
import os
import math
import random

class Room:
	def __init__(self, main, gx, gy):
		self.main = main;
		self.gx = gx;
		self.gy = gy;
		self.neighbours = [];
		self.score = 0;pass;

	def get_unexplored_neighbours(self):
		neighbour_list = [];
		for n in self.neighbours:
			if n in self.main.unexplored_list:
				neighbour_list.append(n);

		return neighbour_list;

	def get_passed_neighbours(self):
		neighbour_list = [];
		for n in self.neighbours:
			if n in self.main.passed_list:
				neighbour_list.append(n);

		return neighbour_list;

	def get_marked_neighbours(self):
		neighbour_list = [];
		for n in self.neighbours:
			if n in self.main.marked_list:
				neighbour_list.append(n);

		return neighbour_list;

class Gate:
	def __init__(self, main, connected_room):
		self.main = main;
		self.connected_room = connected_room;
		self.q = {};
		self.q[(connected_room[0], connected_room[1])] = 0;
		self.q[(connected_room[1], connected_room[0])] = 0;

	def get_r(self, from_room_index, to_room_index):
		from_room = None;
		to_room   = None;
		if from_room_index in self.connected_room:
			from_room = self.main.room_dict[from_room_index];

		if to_room_index in self.connected_room:
			to_room = self.main.room_dict[to_room_index];

		if from_room == None or to_room == None:
			return 0;

		r = to_room.score - from_room.score;

		if r < 0:
			r = 0;

		return r;

class Agent:
	def __init__(self, main, img):
		self.main = main;
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
		self.enable_move = False;
		self.__direction = (0, 0);
		self.speed = 200;
		self.__dist = 0;
		self.__type = 0;

	def get_cur_gx_gy(self):
		gx, gy = self.main.px_py_to_gx_gy(self.__cur_px, self.__cur_py);
		return gx, gy;

	def set_type(self, t):
		self.__type = t;

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

	def thinking(self):
		self.__brain.make_descision();

	def pilot(self):
		cur_room_index = self.gx_gy_to_gindex(self.__cur_px, self.__cur_py);
		cur_room = self.room_dict[cur_room_index];
		
		max_q = -9999;
		max_q_nei = 0;

		for nei_room_index in rm.neighbours:
			gate_id = self.get_gate_id_by_room(cur_room_index, nei_room_index);
			gate = self.gate_dict[gate_id];
			q = gate.q[(cur_room_index, nei_room_index)] 
			if q > max_q:
				max_q = q;
				max_q_nei = nei_room_index;

		gx, gy = self.gindex_to_gx_gy(nei_room_index);
		self.set_end_gx_gy(gx, gy);

	def start(self):
		if self.__type == 1:
			self.pilot();

		print("begin gx = %d, gy = %d" % (self.__begin_gx, self.__begin_gy));
		print("end   gx = %d, gy = %d" % (self.__end_gx, self.__end_gy));

		print("begin px = %d, py = %d" % (self.__begin_px, self.__begin_py));
		print("end   px = %d, py = %d" % (self.__end_px, self.__end_py));

		#print("cur px = %d, py = %d" % (self.__cur_px, self.__cur_py));

		dx = self.__end_gx - self.__begin_gx;
		dy = self.__end_gy - self.__begin_gy;

		mag = math.sqrt(dx ** 2 + dy ** 2);

		self.__direction = (dx / mag, dy / mag);
		self.__dist = math.sqrt((self.__end_px - self.__begin_px) ** 2 + (self.__end_py - self.__begin_py) ** 2);
		self.enable_move = True;


	def __gx_gy_to_px_py(self, gx, gy):
		ppx, ppy = self.main.gx_gy_to_px_py(gx, gy);
		px = ppx + self.__img_size / 2;
		py = ppy + self.__img_size / 2;
		return px, py;

	def update(self):
		if self.enable_move == True:
			if self.__type == 0:
				#print("cur px = %d, py = %d" % (self.__cur_px, self.__cur_py));
				self.main.screen.blit(self.__img, (self.__cur_px, self.__cur_py));

				self.__cur_px = self.__cur_px + self.speed * self.__direction[0] * self.main.delta_time;
				self.__cur_py = self.__cur_py + self.speed * self.__direction[1] * self.main.delta_time;

				cur_dist = math.sqrt((self.__cur_px - self.__begin_px) ** 2 + (self.__cur_py - self.__begin_py) ** 2);

				if cur_dist - self.__dist > 0:
					self.enable_move = False;
					begin_gindex = self.main.gx_gy_to_gindex(self.__begin_gx, self.__begin_gy);
					end_gindex = self.main.gx_gy_to_gindex(self.__end_gx, self.__end_gy);

					self.main.pass_grid(end_gindex);
					self.__cur_px = self.__end_px;
					self.__cur_py = self.__end_py;

					print("cur_px = %s, cur_py = %s, find new target grid" % (self.__cur_px, self.__cur_py));
					
					if self.thinking() == False:
						self.enable_move = False;
			else:
				#print("cur px = %d, py = %d" % (self.__cur_px, self.__cur_py));
				self.main.screen.blit(self.__img, (self.__cur_px, self.__cur_py));

				self.__cur_px = self.__cur_px + self.speed * self.__direction[0] * self.main.delta_time;
				self.__cur_py = self.__cur_py + self.speed * self.__direction[1] * self.main.delta_time;				

class Brain:
	def __init__(self, agent):
		self.agent  = agent;
		self.main   = agent.main;
		self.factor = 0.8;

	def roulette(self, roulette_list):
		prob_list = [];

		s = sum(roulette_list);
		for r in roulette_list:
			prob_list.append(r / s);

		r = random.randint(1, 100) / 100;

		s = 0;
		idx = 0;
		for p in prob_list:
			s = s + p;
			if s >= r:
				return idx;
			idx = idx + 1;

		return -1;

	def make_descision(self):
		print("make descision");
		gx, gy = self.agent.get_cur_gx_gy();
		cur_index = self.main.gx_gy_to_gindex(gx, gy);

		print("gx = %s, gy = %s, cur_index = %s" % (gx, gy, cur_index));

		cur_room = self.main.room_dict[cur_index];

		unexplored_neighbour_list = cur_room.get_unexplored_neighbours();
		passed_neighbour_list = cur_room.get_passed_neighbours();
		marked_neighbour_list = cur_room.get_marked_neighbours();

		active_neighbour_list = [];

		if len(unexplored_neighbour_list) > 0 and len(passed_neighbour_list) == 0 and len(marked_neighbour_list) == 0:
			active_neighbour_list = unexplored_neighbour_list;
			print("active - unexplored_neighbour_list: %s" % active_neighbour_list);
		elif len(unexplored_neighbour_list) == 0 and len(passed_neighbour_list) > 0 and len(marked_neighbour_list) == 0:
			active_neighbour_list = passed_neighbour_list;
			print("active - passed_neighbour_list: %s" % active_neighbour_list);
		elif len(unexplored_neighbour_list) == 0 and len(passed_neighbour_list) == 0 and len(marked_neighbour_list) > 0:
			active_neighbour_list = marked_neighbour_list;
			print("active - marked_neighbour_list: %s" % active_neighbour_list);
		elif len(unexplored_neighbour_list) > 0 and len(passed_neighbour_list) > 0 and len(marked_neighbour_list) == 0:
			idx = self.roulette([7, 3]);
			print("[7, 3] - idx = %s" % idx);
			if idx == 0:
				active_neighbour_list = unexplored_neighbour_list;
				print("active - unexplored_neighbour_list: %s" % active_neighbour_list);
			else:
				active_neighbour_list = passed_neighbour_list;
				print("active - passed_neighbour_list: %s" % active_neighbour_list);
		elif len(unexplored_neighbour_list) > 0 and len(passed_neighbour_list) == 0 and len(marked_neighbour_list) > 0:
			idx = self.roulette([3, 7]);
			print("[3, 7] - idx = %s" % idx);
			if idx == 0:
				active_neighbour_list = unexplored_neighbour_list;
				print("active - unexplored_neighbour_list: %s" % active_neighbour_list);
			else:
				active_neighbour_list = marked_neighbour_list;
				print("active - marked_neighbour_list: %s" % active_neighbour_list);
		elif len(unexplored_neighbour_list) == 0 and len(passed_neighbour_list) > 0 and len(marked_neighbour_list) > 0:
			idx = self.roulette([2, 8]);
			print("[2, 8] - idx = %s" % idx);
			if idx == 0:
				active_neighbour_list = passed_neighbour_list;
				print("active - passed_neighbour_list: %s" % active_neighbour_list);
			else:
				active_neighbour_list = marked_neighbour_list;
				print("active - marked_neighbour_list: %s" % active_neighbour_list);
		else:
			idx = self.roulette([3, 2, 5]);
			print("[3, 2, 5] - idx = %s" % idx);
			if idx == 0:
				active_neighbour_list = unexplored_neighbour_list;
				print("active - unexplored_neighbour_list: %s" % active_neighbour_list);
			elif idx == 1:
				active_neighbour_list = passed_neighbour_list;
				print("active - passed_neighbour_list: %s" % active_neighbour_list);
			else:
				active_neighbour_list = marked_neighbour_list;
				print("active - marked_neighbour_list: %s" % active_neighbour_list);

		rand_list = [];

		for n_index in active_neighbour_list:
			rand_list.append(1);

		if len(rand_list) > 0:
			idx = self.roulette(rand_list);

			target_room_index = active_neighbour_list[idx];

			print("target_room_index = %s" % target_room_index);

			target_room = self.main.room_dict[target_room_index];

			max_q = -9999;

			print("target_room neighbours = %s" % target_room.neighbours);

			for n in target_room.neighbours:
				n_room = self.main.room_dict[n];
				target_nei_index = self.main.gx_gy_to_gindex(n_room.gx, n_room.gy);
				gate_id = self.main.get_gate_id_by_room(target_room_index, target_nei_index);
				gate = self.main.gate_dict[gate_id];
				q = gate.q[(target_room_index, target_nei_index)];
				print("target_room_index = %d, target_nei_index = %d, q = %d" % (target_room_index, target_nei_index, q));

				if q > max_q:
					max_q = q;

			target_room_index = self.main.gx_gy_to_gindex(target_room.gx, target_room.gy);
			print("cur_index = %d, target_room_index = %d" % (cur_index, target_room_index));
			gate_id = self.main.get_gate_id_by_room(cur_index, target_room_index);
			gate = self.main.gate_dict[gate_id];
			r = gate.get_r(cur_index, target_room_index);

			new_q = r + self.factor * max_q;
			gate.q[(cur_index, target_room_index)]  = new_q;

			print("new_q = %s" % new_q);

			if target_room_index in self.main.marked_list:
				print("new episode");
				self.main.mark_grid(cur_index);
				is_successed = self.main.new_episode();
				return is_successed;
			else:
				self.agent.set_begin_gx_gy(cur_room.gx, cur_room.gy);
				self.agent.set_end_gx_gy(target_room.gx, target_room.gy);
				print("agent start!");
				self.agent.start();

			return True;
		else:
			return False;

class Main:
	def __init__(self):
		pygame.init();
		self.grid_size = 32;
		self.width = 640;
		self.height = 640;
		self.clock = pygame.time.Clock();
		self.delta_time = 0.0;
		self.grid_width = int(self.width / self.grid_size);
		self.grid_height = int(self.height / self.grid_size);

		self.screen = pygame.display.set_mode((self.width, self.height), 0, 32);
		pygame.display.set_caption("maze walker");
		self.__cursor = pygame.image.load("res/Cursor.png");
		self.blue_tile = pygame.image.load("res/BlueRoom.png");
		self.red_tile = pygame.image.load("res/RedRoom.png");
		self.yellow_tile = pygame.image.load("res/YellowRoom.png");
		self.__agent = pygame.image.load("res/Robot.png");

		self.__cursor_pos = [0, 0];
		self.__mode = 1;	#1: editor mode; 2: explore mode
		self.unexplored_list = [];
		self.passed_list = [];
		self.marked_list = [];
		self.room_dict = {};
		self.gate_dict = {};

		self.begin_gindex = 0;
		self.end_gindex = 0;

		self.__agent = Agent(self, self.__agent);

		if os.path.exists("config.txt") == True:
			fp = open("config.txt", "r");
			txt = fp.readline();
			txt_list = txt.split(',');
			for item in txt_list:
				gindex = int(item);
				gx, gy = self.gindex_to_gx_gy(gindex);
				self.room_dict[gindex] = Room(self, gx, gy);

			self.__update_neighbour_info();

	def new_episode(self):
		if len(self.passed_list) > 0:
			begin_gindex = random.choice(self.passed_list);
			gx, gy = self.gindex_to_gx_gy(begin_gindex);
			self.__agent.set_begin_gx_gy(gx, gy);
			return self.__agent.thinking();
		else:
			if len(self.unexplored_list) > 0:
				begin_gindex = random.choice(self.unexplored_list);

				self.pass_grid(begin_gindex);

				gx, gy = self.gindex_to_gx_gy(begin_gindex);
				self.__agent.set_begin_gx_gy(gx, gy);
				self.__agent.thinking();
				return True;

			return False;
	def pass_grid(self, gindex):
		if gindex in self.unexplored_list:
			self.unexplored_list.remove(gindex);
			self.passed_list.append(gindex);

	def mark_grid(self, gindex):
		if gindex in self.passed_list:
			self.passed_list.remove(gindex);
			self.marked_list.append(gindex);

	def gx_gy_to_px_py(self, gx, gy):
		px = gx * self.grid_size;
		py = gy * self.grid_size;

		return px, py;

	def px_py_to_gx_gy(self, px, py):
		gx = int(px // self.grid_size);
		gy = int(py // self.grid_size);

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
		gx = gindex % self.grid_width;
		gy = gindex // self.grid_width;
		return gx, gy;

	def gx_gy_to_gindex(self, gx, gy):
		gindex = gy * self.grid_width + gx;
		return int(gindex);

	def __add_neighbour(self, gate_index, my_room_index, neighbour_room_index):
		if not my_room_index in self.room_dict or not neighbour_room_index in self.room_dict:
			return;

		my_room = self.room_dict[my_room_index];
		neighbour_room = self.room_dict[neighbour_room_index];

		if not neighbour_room_index in my_room.neighbours:
			my_room.neighbours.append(neighbour_room_index);

		if not my_room_index in neighbour_room.neighbours:
			neighbour_room.neighbours.append(my_room_index);

		self.__add_gate(gate_index, my_room_index, neighbour_room_index);

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
			if v.connected_room[0] == min_room and v.connected_room[1] == max_room:
				return k;

		return 0;

	def __add_gate(self, gate_index, room1, room2):
		if gate_index in self.gate_dict:
			return;

		min_room, max_room = self.__min_max(room1, room2);

		gate = Gate(self, [min_room, max_room]);
		self.gate_dict[gate_index] = gate;

	def __update_neighbour_info(self):
		keys = list(self.room_dict.keys());
		gate_index = 1;
		for gindex in keys:
			gx, gy = self.gindex_to_gx_gy(gindex);
			if gx - 1 >= 0:
				l_gindex = self.gx_gy_to_gindex(gx - 1, gy);
				if l_gindex in self.room_dict:
					self.__add_neighbour(gate_index, gindex, l_gindex);
					gate_index = gate_index + 1;

			if gx + 1 < self.grid_width:
				r_gindex = self.gx_gy_to_gindex(gx + 1, gy);
				if r_gindex in self.room_dict:
					self.__add_neighbour(gate_index, gindex, r_gindex);
					gate_index = gate_index + 1;

			if gy - 1 >= 0:
				u_gindex = self.gx_gy_to_gindex(gx, gy - 1);
				if u_gindex in self.room_dict:
					self.__add_neighbour(gate_index, gindex, u_gindex);
					gate_index = gate_index + 1;

			if gy + 1 < self.grid_height:
				d_gindex = self.gx_gy_to_gindex(gx, gy + 1);
				if d_gindex in self.room_dict:
					self.__add_neighbour(gate_index, gindex, d_gindex);
					gate_index = gate_index + 1;

	def __update_editor_mode(self):
		for v in self.room_dict.values():
			px, py = self.gx_gy_to_px_py(v.gx, v.gy);
			self.screen.blit(self.blue_tile, (px, py));

		self.screen.blit(self.__cursor, self.__cursor_pos);

		if self.begin_gindex > 0:
			px, py = self.gindex_to_px_py(self.begin_gindex);
			self.screen.blit(self.yellow_tile, (px, py));

		if self.end_gindex > 0:
			px, py = self.gindex_to_px_py(self.end_gindex);
			self.screen.blit(self.red_tile, (px, py));

	def __update_explore_mode(self):
		for r in self.unexplored_list:
			rm = self.room_dict[r];
			px, py = self.gx_gy_to_px_py(rm.gx, rm.gy);
			self.screen.blit(self.blue_tile, (px, py));

		for r in self.passed_list:
			rm = self.room_dict[r];
			px, py = self.gx_gy_to_px_py(rm.gx, rm.gy);
			self.screen.blit(self.yellow_tile, (px, py));

		for r in self.marked_list:
			rm = self.room_dict[r];
			px, py = self.gx_gy_to_px_py(rm.gx, rm.gy);
			self.screen.blit(self.red_tile, (px, py));

		self.__agent.update();

	def __update_test_mode(self):
		for r in self.marked_list:
			rm = self.room_dict[r];
			px, py = self.gx_gy_to_px_py(rm.gx, rm.gy);
			self.screen.blit(self.red_tile, (px, py));

		px, py = self.gindex_to_px_py(self.self.end_gindex);
		sele.screen.blit(self.blue_tile, (px, py));

	def __change_mode(self, new_mode):
		if self.__mode == new_mode:
			return;

		if new_mode == 1:
			self.__exit_explore_mode();
			self.__enter_editor_mode();
		elif new_mode == 2:
			self.__exit_editor_mode();
			self.__enter_explore_mode();
		elif new_mode == 3:
			self.__exit_explore_mode();
			self.__enter_test_mode();

		self.__mode = new_mode;

	def __enter_editor_mode(self):
		self.begin_gindex = 0;
		self.end_gindex = 0;

	def __exit_editor_mode(self):
		pass;

	def __enter_explore_mode(self):
		print("enter explore mode");
		keys = list(self.room_dict.keys());

		self.unexplored_list = [];
		self.passed_list = [];
		self.marked_list = [];

		for k in keys:
			if k == self.begin_gindex:
				self.passed_list.append(k);
			elif k == self.end_gindex:
				self.marked_list.append(k);
			else:
				self.unexplored_list.append(k);
		begin_gx, begin_gy = self.gindex_to_gx_gy(self.begin_gindex);

		if self.end_gindex in self.room_dict:
			room = self.room_dict[self.end_gindex];
			room.score = 100;

		self.__agent.set_begin_gx_gy(begin_gx, begin_gy);
		self.__agent.thinking();

	def __enter_test_mode(self):
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

	def __test_mode_message_process(self, event):
		pos = pygame.mouse.get_pos();
		gx, gy = self.px_py_to_gx_gy(pos[0], pos[1]);
		self.Robot.set_begin_gx_gy(gx, gy);
		self.Robot.set_type(1);
		self.Robot.start();

	def __explore_mode_message_process(self, event):
		if event.key == pygame.K_1:
			# switch to editor_mode
			self.__change_mode(1);
		elif event.key == pygame.K_3:
			self.__change_mode(3);

	def __editor_mode_message_process(self, event):
		if event.key == pygame.K_LEFT:
			self.__move_left();
		elif event.key == pygame.K_RIGHT:
			self.__move_right();
		elif event.key == pygame.K_UP:
			self.__move_up();
		elif event.key == pygame.K_DOWN:
			self.__move_down();
		elif event.key == pygame.K_2:
			# switch to explore_mode
			self.__change_mode(2);
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
				# add elem
				room = Room(self, gx, gy);
				self.room_dict[gindex] = room;
			else:
				# remove elem
				del self.room_dict[gindex];
		elif event.key == pygame.K_b:
			px, py = self.__cursor_pos;
			self.begin_gindex = self.px_py_to_gindex(px, py);

			if self.begin_gindex in self.room_dict:
				begin_room = self.room_dict[self.begin_gindex];

		elif event.key == pygame.K_e:
			px, py = self.__cursor_pos;
			self.end_gindex = self.px_py_to_gindex(px, py);

	def __message_process(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit();
			elif event.type == pygame.KEYDOWN:
				if self.__mode == 1:
					self.__editor_mode_message_process(event);
				elif self.__mode == 2:
					self.__explore_mode_message_process(event);
			elif event.type == pygame.MOUSEBUTTONDOWN:
				elif self.__mode == 3:
					self.__test_mode_message_process(event);
	def update(self):
		while True:
			self.delta_time = self.clock.tick() / 1000;
			self.__message_process();
			self.screen.fill((0, 0, 0));
			if self.__mode == 1:
				# edit mode
				self.__update_editor_mode();
			elif self.__mode == 2:
				# explore mode
				self.__update_explore_mode();
			elif self.__mode == 3:
				# test mode
				self.__update_test_mode();

			pygame.display.update();

if __name__ == '__main__':
	game = Main();
	game.update();