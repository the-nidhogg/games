#!/usr/bin/python
# -*- coding: utf-8 -*-
from pygame import *
from pygame.locals import *
from pygame.font import *
from time import sleep,time
from math import fabs
from random import randrange
init()
fen=display.set_mode((600,400))
display.set_caption("PONG")
class Palette(object):
	point=0
	def __init__(self):
		self.hauteur=50
		self.pos=[10,((400-self.hauteur)/2.0)]
		self.vitesse=0.75
	 
	def deplacement(self,direct):
		if self.pos[1]+direct*self.vitesse>=(400-self.hauteur)or self.pos[1]+direct*self.vitesse<=0:return 
		self.pos[1]+=direct*self.vitesse
		
	def affichage(self,fen):
		fen.subsurface((self.pos[0],self.pos[1],5,self.hauteur)).fill((255,255,255))
		
		
class Ia(object):
	point=0
	def __init__(self):
		self.hauteur=50
		self.pos=[600-10,((400-self.hauteur)/2.0)]
		self.vitesse=0.75
		self.NoIa=2
		self.computed=0
		self.target=0
		
	def ia(self):
		if self.NoIa==0:self.ia0()
		if self.NoIa==1:self.ia1()
		if self.NoIa==2:self.ia2()
		
	def ia0(self):
		if self.pos[1]+self.hauteur/2-2>ball.pos[1]+ball.hauteur/2:self.deplacement(-1)
		elif self.pos[1]+self.hauteur/2+2<ball.pos[1]+ball.hauteur/2:self.deplacement(1)
	
	def ia1(self):
		if fabs(ball.sens[0])!=ball.sens[0]:
			if self.pos[1]+self.hauteur/2>200:self.deplacement(-1)
			elif self.pos[1]+self.hauteur/2<200:self.deplacement(1)
			else:return
		else:
			if self.pos[1]+self.hauteur/2-2>ball.pos[1]+ball.hauteur/2:self.deplacement(-1)
			elif self.pos[1]+self.hauteur/2+2<ball.pos[1]+ball.hauteur/2:self.deplacement(1)
			
	def ia2(self):
		if fabs(ball.sens[0])!=ball.sens[0]:
			self.computed=0
			if self.pos[1]+self.hauteur/2>200:self.deplacement(-1)
			elif self.pos[1]+self.hauteur/2<200:self.deplacement(1)
			return
		else:
			if not self.computed:
				self.target=self.compute()
				return
			else:
				if self.pos[1]>self.target:self.deplacement(-1)
				elif self.pos[1]<self.target:self.deplacement(1)
				else:return
					
	def compute(self):
		self.computed=1
		emulPos=[]+ball.pos
		emulSens=[]+ball.sens
		emulAngle=ball.angle
		while 1:
			if emulPos[1]>398 or emulPos[1]<2:
				emulAngle=modifAngle(emulAngle,180)
				emulSens=convertAngle(emulAngle)
			if 0<emulPos[1]+ball.vitesse*emulSens[1]<400:emulPos[1]+=self.vitesse*emulSens[1]
			if 0<emulPos[0]+ball.vitesse*emulSens[0]<600:emulPos[0]+=self.vitesse*emulSens[0]
			if emulPos[0]+ball.hauteur>=self.pos[0]:return emulPos[1]-randrange(self.hauteur)

	def deplacement(self,direct):
		if self.pos[1]+direct*self.vitesse>=(400-self.hauteur)or self.pos[1]+direct*self.vitesse<=0:return 
		self.pos[1]+=direct*self.vitesse
		
	def affichage(self,fen):
		fen.subsurface((self.pos[0],self.pos[1],5,self.hauteur)).fill((255,255,255))
		
		
class Ball(object):
	def __init__(self):
		self.sens=[0,0]
		self.hauteur=5
		self.vitesse=2
		self.pos=[20,((400-self.hauteur)/2.0)]
		self.angle=180
		self.lastch=time()
		
	def deplacement(self):
		gagne=0
		if fabs(self.sens[0])!=self.sens[0]:
			if self.pos[0]<=2:
				Ia.point+=1
				gagne=-1
			else:
				for i in range(self.hauteur):
					if collision((self.pos[0],self.pos[1]+i),palette.pos,(palette.pos[0]+5,palette.pos[1]+palette.hauteur)):
						self.angle=modulo(fabs(palette.pos[1]-(self.pos[1]+2))-25+self.angle,360)[0]
						self.angle=modifAngle(self.angle,90)
						self.sens=convertAngle(self.angle)
						break
		else:
			if self.pos[0]>=598:
				Palette.point+=1
				gagne=1
			else:
				for i in range(self.hauteur):
					if collision((self.pos[0]+self.hauteur,self.pos[1]+1),(ia.pos),(ia.pos[0]+5,ia.pos[1]+ia.hauteur)):
						self.angle=modulo(self.angle-(fabs(ia.pos[1]-(self.pos[1]+2))-25),360)[0]
						self.angle=modifAngle(self.angle,90)
						self.sens=convertAngle(self.angle)
						break
		if self.pos[1]>398 or self.pos[1]<2:
			self.angle=modifAngle(self.angle,180)
			self.sens=convertAngle(self.angle)
		if 0<self.pos[1]+self.vitesse*self.sens[1]<400:self.pos[1]+=self.vitesse*self.sens[1]
		if 0<self.pos[0]+self.vitesse*self.sens[0]<600:self.pos[0]+=self.vitesse*self.sens[0]
		return gagne
		
	def affichage(self,fen):
		try:fen.subsurface((self.pos[0],self.pos[1],self.hauteur,self.hauteur)).fill((255,255,255))
		except:pass


def convertAngle(angle):
	if angle>90:angle90=fabs(90-(angle-90))
	else:angle90=angle
	if angle90>=90:angle90=fabs(angle90-180)
	y=1/90.0*angle90
	x=1-y
	if angle>90 and angle<270:x*=-1
	if angle>0 and angle<180:y*=-1
	return [x,y]

def modulo(nombre,modul):
	degres=0
	while nombre>=modul:
		nombre-=modul
		degres+=1
	return nombre,degres

def modifAngle(angle,symetrie):
	if symetrie>360:symetrie-=360
	if angle>=symetrie:angle-=(angle-symetrie)*2
	else:angle+=(symetrie-angle)*2
	if angle<0:angle+=360
	elif angle>=360:angle-=360
	return angle

def affichage():
	fen.fill(0)
	fen.subsurface((297,0,6,400)).fill((255,255,255))
	fen.blit(font.Font(None,32).render(str(Palette.point),1,(255,255,255)),(250,10))
	fen.blit(font.Font(None,32).render(str(Ia.point),1,(255,255,255)),(340,10))
	palette.affichage(fen)
	ia.affichage(fen)
	ball.affichage(fen)
	display.flip()

def pause():
	fen.blit(font.Font(None,62).render("PAUSE",1,(255,255,255)),(225,175))
	display.flip()
	while 1:
		sleep(0.25)
		for i in event.get():
			if i.type==QUIT:quit;exit()
			elif i.type==KEYDOWN or i.type==MOUSEBUTTONDOWN:
				return

palette=Palette()
ia=Ia()
ball=Ball()
collision=lambda a,b,c:b[0]<a[0]<c[0] and b[1]<a[1]<c[1]
clavier={K_UP:0,K_DOWN:0}
start=0
while 1:
	sleep(0.0006125)
	affichage()
	for i in event.get():
		if i.type==KEYDOWN:
			if i.key==K_UP:
				clavier[K_UP]=1
			elif i.key==K_DOWN:
				clavier[K_DOWN]=1
			elif i.key==K_ESCAPE or i.key==K_SPACE:
				pause()
			elif i.key==K_RETURN and not start:
				ball.sens=[-1,0]
				start=1
		elif i.type==KEYUP:
			if i.key==K_UP:
				clavier[K_UP]=0
			elif i.key==K_DOWN:
				clavier[K_DOWN]=0
		elif i.type==QUIT:quit;exit()
	if clavier[K_UP]:palette.deplacement(-1)
	elif clavier[K_DOWN]:palette.deplacement(1)
	if start:ia.ia()
	if ball.deplacement():
		start=0
		palette.__init__()
		ball.__init__()
		ia.__init__()
