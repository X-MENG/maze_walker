import pygame
import numpy as np

class Room:
	def __init__(self):
		print("Room");

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
		self.width = 640;
		self.height = 640;
		self.__screen = pygame.display.set_mode((self.width, self.height), 0, 32);
		pygame.display.set_caption("maze walker");
		self.__is_shift_pressed = False;
		self.__is_ctrl_pressed = False;
		self.__cursor = pygame.image.load("res/BlueRoom.png").convert();
		self.__cursor_pos = [0, 0];
		self.__cursor_step = 32;

	def __move_left(self):
		if self.__is_shift_pressed == True:
			print("remove");
		elif self.__is_ctrl_pressed == True:
			print("add");
		else:
			new_x = self.__cursor_pos[0] - self.__cursor_step;
			if new_x >= 0:
				self.__cursor_pos[0] = new_x;

	def __move_right(self):
		if self.__is_shift_pressed == True:
			print("remove");
		elif self.__is_ctrl_pressed == True:
			print("add");
		else:
			new_x = self.__cursor_pos[0] + self.__cursor_step;
			if new_x < self.width:
				self.__cursor_pos[0] = new_x;

	def __move_up(self):
		if self.__is_shift_pressed == True:
			print("remove");
		elif self.__is_ctrl_pressed == True:
			print("add");
		else:
			new_y = self.__cursor_pos[1] - self.__cursor_step;
			if new_y >= 0:
				self.__cursor_pos[1] = new_y;

	def __move_down(self):
		if self.__is_shift_pressed == True:
			print("remove");
		elif self.__is_ctrl_pressed == True:
			print("add");
		else:
			new_y = self.__cursor_pos[1] + self.__cursor_step;
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
				elif event.key == pygame.K_LSHIFT:
					self.__is_shift_pressed = True;
				elif event.key == pygame.K_LCTRL:
					self.__is_ctrl_pressed = True;
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LSHIFT:
					self.__is_shift_pressed = False;
				elif event.key == pygame.K_LCTRL:
					self.__is_ctrl_pressed = False;
	def Update(self):
		while True:
			self.__message_process();
			self.__screen.fill((0, 0, 0));
			self.__screen.blit(self.__cursor, self.__cursor_pos);
			pygame.display.update();

if __name__ == '__main__':
	game = Main();
	game.Update();