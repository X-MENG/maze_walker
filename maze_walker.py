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
		self.__screen = pygame.display.set_mode((640, 640), 0, 32);
		pygame.display.set_caption("maze walker");
		self.__is_shift_pressed = False;
		self.__is_ctrl_pressed = False;

	def __move_left(self):
		if self.__is_shift_pressed == True:
			print("remove");
		elif self.__is_ctrl_pressed == True:
			print("add");
		else:
			print("move");

	def __move_right(self):
		if self.__is_shift_pressed == True:
			print("remove");
		elif self.__is_ctrl_pressed == True:
			print("add");
		else:
			print("move");

	def __move_up(self):
		if self.__is_shift_pressed == True:
			print("remove");
		elif self.__is_ctrl_pressed == True:
			print("add");
		else:
			print("move");

	def __move_down(self):
		if self.__is_shift_pressed == True:
			print("remove");
		elif self.__is_ctrl_pressed == True:
			print("add");
		else:
			print("move");

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
			pygame.display.update();

if __name__ == '__main__':
	game = Main();
	game.Update();