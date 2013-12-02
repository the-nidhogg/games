#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import choice
from time import sleep,time
from pygame import *
from pygame.locals import *


class Snake(object):
	def __init__(self):
		self.tete = [296,196]
		self.corps = [[296,192], [296,188]]
		self.sens = [0,0]
		self.vitesse = 4
		self.taille = 4

	def deplacement(self):
		for i in range(len(self.corps)):
			try:
				self.corps[i] = [] + self.corps[i+1]
			except:
				self.corps[i] = [] + self.tete
		self.tete[0] += self.vitesse * self.sens[0]
		self.tete[1] += self.vitesse * self.sens[1]
		if self.tete[0] < 0 or self.tete[0] >= 600 or \
			self.tete[1] < 0 or self.tete[1] >= 400 or self.tete in self.corps:
				return 0
		return 1

	def add(self):
		self.corps.append(self.tete)


def afficher(food):
	fen.fill(0)
	fen.subsurface(snake.tete[0], snake.tete[1], snake.taille,
		snake.taille).fill((255, 255, 255))
	for i in snake.corps:
		fen.subsurface(i[0], i[1], snake.taille,
			snake.taille).fill((255, 255, 255))
	fen.subsurface(food[0], food[1], snake.taille, 
	snake.taille).fill((255, 255, 255))
	display.flip()


fen = display.set_mode((600,400))
display.set_caption("SNAKE")

snake = Snake()
liste = [[x, y]for x in range(0, 600, 4)for y in range(0, 400, 4)]
food = choice(liste)
start = 0

while 1:
	sleep(0.06125)
	afficher(food)
	if snake.tete == food:
		snake.add()
		liste = [[x, y]for x in range(0, 600, 4)for y in range(0, 400, 4)]
		food = choice(liste)
		
	for i in event.get():
		if i.type == QUIT:
			quit()
			exit()
			
		elif i.type == KEYDOWN:
			if i.key == K_UP and snake.sens[1] != 1:
				snake.sens = [0,-1]
			elif i.key == K_DOWN and snake.sens[1] != -1:
				snake.sens = [0,1]
			elif i.key == K_RIGHT and snake.sens[0] != -1:
				snake.sens = [1,0]
			elif i.key == K_LEFT and snake.sens[0] != 1:
				snake.sens = [-1,0]
			if not start:
				start = 1
				continue
				
	if start:
		start = snake.deplacement()
		if not start:
			snake.__init__()
