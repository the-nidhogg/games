#!/usr/bin/python
# -*- coding: utf-8 -*-
from pygame import *
from pygame.locals import *
from ctypes import CDLL
from os import getcwd,system
from time import sleep,time
from random import randrange
system("gcc -shared -Wl,-soname,snake -o snake.so -fPIC snake.c")
moteur=CDLL(getcwd()+"/snake.so")

fenetre=display.set_mode((600,400))
sens=-1
moteur.init()
moteur.initialise()
while 1:
	sleep(0.06125)
	if not moteur.deplacement(sens):moteur.init()
	while 1:
		a=moteur.get()
		if a==-1:break
		try:
			a=[int(str(a)[:-3]),int(str(a)[-3:])]
			fenetre.subsurface(a[1], a[0], 4, 4).fill((255, 255, 255))
		except:print 'error'
	posFood=moteur.getFood()
	posFood=[int(str(posFood)[:-3]),int(str(posFood)[-3:])]
	fenetre.subsurface(posFood[1], posFood[0], 4, 4).fill((255, 255, 255))
	display.flip()
	fenetre.fill(0)
	for i in event.get():
		if i.type==KEYDOWN:
			if i.key==K_UP and sens!=-2:
				sens=1
			elif i.key==K_DOWN and sens!=1:
				sens=-2
			elif i.key==K_RIGHT and sens !=-1:
				sens=2
			elif i.key==K_LEFT and sens != 2:
				sens=-1
		elif i.type==QUIT:quit();exit()
