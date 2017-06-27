import pygame
import numpy as np

class Room:
	def __init__(self, owner, x, y, tile):
		self.owner = owner;
		self.x = x;
		self.y = y;
		self.tile = tile;

	def render(self):
		self.owner.screen.blit(self.tile, (self.x * self.owner.grid_size, self.y * self.owner.grid_size));


class Gate:
	def __init__(self):
		print("Gate");

class Robot:
	def __init__(self):
		print("Robot");

class Brain:
	def __init__(self):
		print("Brain");

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

		self.__cursor_pos = [0, 0];
		self.__mode = 0;
		self.__unexplored_list = [];
		self.__passed_list = [];
		self.__marked_list = [];
		self.__room_dict = {};
		self.__gate_dict = {};

	def __update_editor_mode(self):
		for v in self.__room_dict.values():
			v.render();

		self.screen.blit(self.__cursor, self.__cursor_pos);


	def __update_explore_mode(self):
		pass

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
				elif event.key == pygame.K_SPACE:
					px, py = self.__cursor_pos;

					gx = px // self.grid_size;
					gy = py // self.grid_size;

					gindex = gy * self.grid_size + gx;

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