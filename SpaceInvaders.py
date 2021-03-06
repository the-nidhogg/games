#!/usr/bin/python
# -*- coding: utf-8 -*-
from pygame import *
from pygame.locals import *
from pygame.font import *
from time import sleep,time
from random import randrange
init()
RESOLUTION=(600,450)
fenetre=display.set_mode(RESOLUTION)
display.set_caption("Space Invaders")

collision=lambda a,b,c:b[0]<a[0]<c[0]and b[1]<a[1]<c[1]

class Vaisseau(object):
	vies=3
	vitesse=3
	vitesseBall=2
	score=0
	levels=0
	def __init__(self):
		self.largeur=20
		self.hauteur=5
		self.pos=[290,394]
		self.balls=[]
		self.lastTir=time()
		self.cadence=0.5

	def deplacement(self,sens):
		if 600-self.largeur>self.pos[0]+Vaisseau.vitesse*sens>0:self.pos[0]+=Vaisseau.vitesse*sens

	def tirer(self):
		if time()-self.lastTir>=self.cadence:
			self.balls.append([self.pos[0]+self.largeur/2.0,self.pos[1]-1])
			self.lastTir=time()

	def afficher(self,fenetre):
		fenetre.subsurface(self.pos[0],self.pos[1],self.largeur,self.hauteur).fill((255,0,0))
		for i in self.balls:
			fenetre.subsurface(i[0],i[1],2,5).fill((255,0,0))


class Invaders(object):
	form=1
	sens=1
	vitesse=2
	balls=[]
	subsurfaces1={}
	subsurfaces2={}
	form11="".join([x+x[::-1]for x in["nnnb","nnbb","nbbb","bbnb","bbbb","nbnb","bnnn","nbnn"]])
	form21="".join([x+x[::-1]for x in["nnnb","nnbb","nbbb","bbnb","bbbb","nnbn","nbnb","bnbn"]])
	form12="".join([x+x[::-1]for x in["nnbnnn","nnnbnn","nnbbbb","nbbnbb","bbbbbb","bnbbbb","bnbnnn","nnnbbn"]])
	form22="".join([x+x[::-1]for x in["nnbnnn","bnnbnn","bnbbbb","bbbnbb","bbbbbb","nbbbbb","nnbnnn","nbnnnn"]])
	form13="".join([x+x[::-1]for x in["nnbnnn","nnnbnn","nnbbbb","nbbnbb","bbbbbb","bnbbbb","bnbnnn","nnnbbn"]])
	form23="".join([x+x[::-1]for x in["nnbnnn","bnnbnn","bnbbbb","bbbnbb","bbbbbb","nbbbbb","nnbnnn","nbnnnn"]])
	balls_form=0
	balls_shape=["nb","nb","bn","bn","nb","nb"]
	balls_shape+=[x[::-1]for x in balls_shape]
	balls_shape="".join(balls_shape)
	
	def __init__(self,pos,number):
		self.number=number
		self.pos=pos
		self.hauteur=16
		if number!=1:
			self.largeur=24
			self.subsurfaces=[[self.pos[0]+x,self.pos[1]+y]for y in xrange(0,16,2)for x in xrange(0,24,2)]
		else:
			self.subsurfaces=[[self.pos[0]+x,self.pos[1]+y]for y in xrange(0,16,2)for x in xrange(0,16,2)]
			self.tire_max=7
			self.score=10
			self.largeur=16
		if number==2:
			self.tire_max=10
			self.score=20
		elif number==3:
			self.tire_max=15
			self.score=50
			
	def tirer(self):
		if len(Invaders.balls)<=self.tire_max+Vaisseau.levels and not randrange(500):
			Invaders.balls.append([self.pos[0]+self.largeur/2.0,self.pos[1]])
			
	def deplacement(self):
		self.pos[0]+=Invaders.sens*Invaders.vitesse
		if self.number!=1:
			if str(self.pos[0]*1000)+str(self.pos[1]) in Invaders.subsurfaces2:
				self.subsurfaces=[]+Invaders.subsurfaces2[str(self.pos[0]*1000)+str(self.pos[1])]
			else:
				self.subsurfaces=[[self.pos[0]+x,self.pos[1]+y]for y in xrange(0,16,2)for x in xrange(0,24,2)]
				Invaders.subsurfaces2[str(self.pos[0]*1000)+str(self.pos[1])]=[]+self.subsurfaces
		else:
			if str(self.pos[0]*1000)+str(self.pos[1]) in Invaders.subsurfaces1:
				self.subsurfaces=[]+Invaders.subsurfaces1[str(self.pos[0]*1000)+str(self.pos[1])]
			else:
				self.subsurfaces=[[self.pos[0]+x,self.pos[1]+y]for y in xrange(0,16,2)for x in xrange(0,16,2)]
				Invaders.subsurfaces1[str(self.pos[0]*1000)+str(self.pos[1])]=[]+self.subsurfaces
		
	def afficher(self,fenetre):
		if Invaders.form==1:
			if self.number==1:forme=Invaders.form11
			if self.number==2:forme=Invaders.form12
			if self.number==3:forme=Invaders.form13
		else:
			if self.number==1:forme=Invaders.form21
			if self.number==2:forme=Invaders.form22
			if self.number==3:forme=Invaders.form23
		for i,j in enumerate(self.subsurfaces):
			if forme[i]=="n":continue
			elif forme[i]=="b":color=(255,255,255)
			fenetre.subsurface(j[0],j[1],2,2).fill(color)


class Special(object):
	formExplosion="".join(x+x[::-1] for x in["nnnnnnnnbbnnn","nnnnnnnnbbbnn","nnbbnnnnnbbbn","nnbbbnnnnnbbn","nnnbbbnnnnnnn","nnnnbbbnnnnnn","nnnnnbbbnnnnn","nnnnnnbbnnnnn","bbbbnnnnnnnnn"])
	formExplosion=formExplosion+formExplosion[::-1]
	formVaisseau="".join(x+x[::-1] for x in["nnnnvvv","nnvvvvv","vvvvvvv","vvnnvvn","vvvvvvv","vvvvvvn","nnvvnnn"])
	tempsExplo=0.5	#s
	vitesse=1.5	#px
	lastApear=time()
	def __init__(self,pos,number=0,sens=1):
		self.pos=pos
		self.number=number
		if number==0:#explo
			self.apparition=time()
			self.hauteur=18
			self.largeur=26
			self.subsurfaces=[[pos[0]+x,pos[1]+y]for y in xrange(0,18,2)for x in xrange(0,26,2)]
		if number==1:
			self.sens=sens
			self.hauteur=14
			self.largeur=28
			self.subsurfaces=[[pos[0]+x,pos[1]+y]for y in xrange(0,14,2)for x in xrange(0,28,2)]

	def deplacement(self):
		self.pos[0]+=Special.vitesse*self.sens
		self.subsurfaces=[[self.pos[0]+x,self.pos[1]+y]for y in xrange(0,14,2)for x in xrange(0,28,2)]

	def afficher(self,fenetre):
		if self.number==0:
			a,b=0,0
			for i in Special.formExplosion:
				if i=="b":
					try:fenetre.subsurface(self.pos[0]+a,self.pos[1]+b,1,1).fill((255,255,255))
					except:pass
				a+=1
				if a==self.largeur:
					b+=1
					a=0
		elif self.number==1:
			a,b=0,0
			for i in Special.formVaisseau:
				if i=="v":
					fenetre.subsurface(self.pos[0]+a,self.pos[1]+b,2,2).fill((0,255,0))
				a+=2
				if a==self.largeur:
					b+=2
					a=0
			self.deplacement()


niveaux=(([(x*20+1,y*20+20)for y in xrange(5)for x in xrange(10)],1),
		 ([(x*28+1,y*20+20)for y in xrange(5)for x in xrange(10)],2),
		 ([(x*32+1,y*20+20)for y in xrange(5)for x in xrange(10)],3))
level=0
vaisseau=Vaisseau()
spe=[]
explo=[]
chform=time()
destruct=[]
clavier={x:0 for x in xrange(400)}
vitesseBallEnnemi=2
destructBall=[]
largeurBlocs=50
hauteurBlocs=20
blocs=[[[y+50,z+300]for y in xrange(largeurBlocs)for z in xrange(hauteurBlocs)],[[y+200,z+300]for y in xrange(largeurBlocs)for z in xrange(hauteurBlocs)],[[y+350,z+300]for y in xrange(largeurBlocs)for z in xrange(hauteurBlocs)],[[y+500,z+300]for y in xrange(largeurBlocs)for z in xrange(hauteurBlocs)]]
chform_ball=time()
def pause(fenetre,texte=["PAUSE"]):
	if texte!=["PAUSE"]:fenetre.fill(0)
	a=0
	for i in texte:
		fenetre.blit(font.Font(None,36).render(i,1,(255,255,255)),((600-len(i)*15)/2.0,(400-len(texte)*36)/2.0+a))
		a+=36
	display.flip()
	sleep(0.5)
	paused=1
	while paused:
		sleep(0.125)
		for i in event.get():
			if i.type==QUIT:quit;exit()
			elif i.type==KEYDOWN:
				if texte==["PAUSE"]:
					if i.key==K_SPACE:paused=0
				else:paused=0

while 1:
	pause(fenetre,["APPUYEZ SUR UNE TOUCHE","POUR COMMENCER","level {}".format(Vaisseau.levels)])
	if level==3:level=0
	if niveaux[level][1]==1:ennemi=[]+[Invaders([x[0],x[1]],1)for x in niveaux[level][0]]
	elif niveaux[level][1]==2:ennemi=[]+[Invaders([x[0],x[1]],2)for x in niveaux[level][0]]
	elif niveaux[level][1]==3:ennemi=[]+[Invaders([x[0],x[1]],3)for x in niveaux[level][0]]
	perdu=0
	gagne=0
	Special.lastApear=time()

	while not perdu and not gagne:
		#sleep(0.006125)

		if time()-chform>=0.5:
			Invaders.form=bool(not Invaders.form)
			chform=time()
		if time()-chform_ball>=0.125:
			chform_ball=time()
			if Invaders.balls_form:Invaders.balls_form=0
			else:Invaders.balls_form=12
			
		chsens=0
		fenetre.fill(0)
		delExplo=[]
		for i in explo:
			i.afficher(fenetre)
			if i.apparition>=Special.tempsExplo:delExplo.append(i)
		for i in delExplo:explo.remove(i)
		for i in blocs:
			for j in i:
				fenetre.subsurface(j[0],j[1],1,1).fill((255,0,0))
		fenetre.blit(font.Font(None,20).render("Vies",1,(255,255,255)),(5,420))
		fenetre.blit(font.Font(None,20).render("Score: ",1,(255,255,255)),(150,420))
		fenetre.blit(font.Font(None,20).render(str(Vaisseau.score),1,(255,255,255)),(200,420))
		fenetre.blit(font.Font(None,20).render("Level: ",1,(255,255,255)),(300,420))
		fenetre.blit(font.Font(None,20).render(str(Vaisseau.levels),1,(255,255,255)),(360,420))
		fenetre.blit(font.Font(None,20).render("Vitesse de descente: ",1,(255,255,255)),(400,420))
		fenetre.blit(font.Font(None,20).render(str(5+min(Vaisseau.levels/3,10))+" pxl",1,(255,255,255)),(550,420))
		for i in xrange(3):
			if i<Vaisseau.vies:color=(0,255,0)
			else:color=(255,0,0)
			fenetre.subsurface(40+(vaisseau.largeur+5)*i,425,vaisseau.largeur,vaisseau.hauteur).fill(color)
			
		for i in ennemi:
			i.afficher(fenetre)
			i.deplacement()
			if i.pos[0]+i.largeur>=599 or i.pos[0]<=1:chsens=1
			if i.pos[1]>=350:
				perdu=1
				break
			i.tirer()
			
		for i in Invaders.balls:
			for j,k in enumerate([[i[0]+x,i[1]+y]for y in range(6)for x in range(2)]):
				if Invaders.balls_shape[j+Invaders.balls_form]=="n":continue
				else:fenetre.subsurface(k[0],k[1],1,1).fill((255,255,255))

		if len(spe):
			spe[0].afficher(fenetre)
			if spe[0].pos[0]>RESOLUTION[0]-28 or spe[0].pos[0]<=0 :spe=[]
		vaisseau.afficher(fenetre)
		display.flip()

		if chsens:
			Invaders.sens=-Invaders.sens
			for i in ennemi:i.pos[1]+=5+min(Vaisseau.levels/3,10)

		destructBall=[]
		for i in Invaders.balls:
			i[1]+=vitesseBallEnnemi
			if collision(i,vaisseau.pos,[vaisseau.pos[0]+vaisseau.largeur,vaisseau.pos[1]+vaisseau.hauteur])or collision([i[0]+2,i[1]+5],vaisseau.pos,[vaisseau.pos[0]+vaisseau.largeur,vaisseau.pos[1]+vaisseau.hauteur]):
				destructBall.append(i)
				Vaisseau.vies-=1
				if Vaisseau.vies<0:perdu=1
				break
			a=0
			for k,l in enumerate([[(50,300),(100,300+hauteurBlocs)],[(200,300),(250,300+hauteurBlocs)],[(350,300),(400,300+hauteurBlocs)],[(500,300),(550,300+hauteurBlocs)]]):
				if collision(i,l[0],l[1]):
					for j in blocs[k]:
						if collision((i[0],i[1]),j,(j[0]+2,j[1]+2)):
							a=0
							destructBall.append(i)
							blocs[k].remove(j)
							for x in xrange(3):
								for y in xrange(2):
									try:
										blocs[k].remove([j[0]+x+1,j[1]-y])
										blocs[k].remove([j[0]+x+1,j[1]+y])
									except:pass
							break
				if a:break
			if a:break
			if i[1]+5>=400:
				destructBall.append(i)
				break

		for i in destructBall:
			Invaders.balls.remove(i)

		for threeTimes in xrange(6):
			for i in vaisseau.balls:
				a=0
				for k,l in enumerate([[(50,300),(100,300+hauteurBlocs)],[(200,300),(250,300+hauteurBlocs)],[(350,300),(400,300+hauteurBlocs)],[(500,300),(550,300+hauteurBlocs)]]):
					if collision(i,l[0],l[1]):
						for j in blocs[k]:
							if (collision((i[0],i[1]),j,(j[0]+2,j[1]+2)) or collision((i[0],i[1]),(j[0],j[1]-1),(j[0]+2,j[1]+2))):
								a=1
								destruct.append([None,i])
								blocs[k].remove(j)
								for x in xrange(2):
									for y in xrange(2):
										try:
											blocs[k].remove([j[0]+x+1,j[1]-y])
											blocs[k].remove([j[0]+x+1,j[1]+y])
										except:pass
								break
					if a:break
				if a:break
				i[1]-=Vaisseau.vitesseBall
				if i[1]<=0:
					destruct.append([None,i])
					Vaisseau.score-=1
					break
				for j in ennemi:
					if collision(i,j.pos,[j.pos[0]+j.largeur,j.pos[1]+j.hauteur])or collision([i[0]+2,i[1]+5],j.pos,[j.pos[0]+j.largeur,j.pos[1]+j.hauteur]):
						destruct.append([j,i])
						explo.append(Special(j.pos))
						if Vaisseau.vies<3 and randrange(2):Vaisseau.vies+=1
						else:Vaisseau.score+=j.score
							
						break
				if len(spe):
					if collision(i,spe[0].pos,[spe[0].pos[0]+spe[0].largeur,spe[0].pos[1]+spe[0].hauteur])or collision([i[0]+2,i[1]+5],spe[0].pos,[spe[0].pos[0]+spe[0].largeur,spe[0].pos[1]+spe[0].hauteur]):
						Vaisseau.score+=250
						spe=[]
						break
			for i in destruct:
				try:ennemi.remove(i[0])
				except:pass
				vaisseau.balls.remove(i[1])
			destruct=[]

		if not len(spe) and not randrange(2500) and time()-Special.lastApear>=30:
			Special.lastApear=time()
			a=randrange(2)
			if a:b=-1
			else:b=1
			spe.append(Special([a*(RESOLUTION[0]-28),1],1,b))
		gagne=not len(ennemi)

		for i in event.get():
			if i.type==QUIT:quit;exit()
			elif i.type==KEYDOWN:
				if i.key==K_RIGHT:
					clavier[K_RIGHT]=1
					if clavier[K_LEFT]==1:clavier[K_LEFT]=2
				elif i.key==K_LEFT:
					clavier[K_LEFT]=1
					if clavier[K_RIGHT]==1:clavier[K_RIGHT]=2
				elif i.key==K_UP:
					clavier[K_UP]=1
				elif i.key==K_ESCAPE:fenetre=display.set_mode(RESOLUTION)
				elif i.key==K_SPACE:pause(fenetre)
			elif i.type==KEYUP:
				if i.key==K_RIGHT:
					clavier[K_RIGHT]=0
					if clavier[K_LEFT]==2:clavier[K_LEFT]=1
				elif i.key==K_LEFT:
					clavier[K_LEFT]=0
					if clavier[K_RIGHT]==2:clavier[K_RIGHT]=1
				elif i.key==K_UP:
					clavier[K_UP]=0

		if clavier[K_RIGHT]==1:vaisseau.deplacement(1)
		elif clavier[K_LEFT]==1:vaisseau.deplacement(-1)
		if clavier[K_UP]:vaisseau.tirer()

	Invaders.sens=1
	Invaders.balls=[]
	spe=[]
	explo=[]

	if gagne:
		level+=1
		vaisseau.__init__()
		clavier={x:0 for x in xrange(400)}
		Vaisseau.levels+=1

	if perdu:
		a=0
		fini=0
		nom=""
		scores={}
		with open("spaceInvaders.py","r")as f:f=f.read().split("\n#/§")[1:][1:]
		for i in f:
			i=i.split("#/§")[:2]
			if i[0]not in scores:scores[i[0]]=[int(i[1])]
			else:scores[i[0]].append(int(i[1]))
		maxi=[0,"personne"]
		for i in scores:
			if max(scores[i])>maxi[0]:maxi=[max(scores[i]),i]
		while not fini:
			sleep(0.05)
			a=bool(not a)
			fenetre.fill(0)
			fenetre.blit(font.Font(None,32).render("VOUS AVEZ PERDU",1,(255,0,0)),(175,135))
			fenetre.blit(font.Font(None,32).render("Ecrivez votre nom pour enregistrer votre scors",1,(255,0,0)),(60,175))
			fenetre.blit(font.Font(None,32).render("Score: "+str(Vaisseau.score)+"    nom: "+nom+"".join(["_" for x in xrange(1)if a]),1,(255,0,0)),(175,200))
			fenetre.blit(font.Font(None,32).render("Puis appuyez sur entree pour valider",1,(255,0,0)),(100,225))
			fenetre.blit(font.Font(None,32).render("Sinon, appuyez sur 'echap'",1,(255,0,0)),(133,250))
			fenetre.blit(font.Font(None,32).render("Meilleur score: {}  par:  {}".format(maxi[0],maxi[1]),1,(255,0,0)),(300-len(maxi[1])*26,275))
			display.flip()
			for i in event.get():
				if i.type==KEYDOWN:
					if str(i.unicode) in [chr(j)for j in xrange(30,128)]:
						nom+=str(i.unicode)
					elif i.key==K_RETURN and nom!="":
						with open("spaceInvaders.py","a")as f:f.write("#/§"+nom+"#/§"+str(Vaisseau.score)+"#/§")
						fini=1
					elif i.key==K_ESCAPE:
						fini=1
					elif i.key==K_BACKSPACE:nom=nom[:-1]
		clavier={x:0 for x in xrange(400)}
		blocs=[[[y+50,z+300]for y in xrange(largeurBlocs)for z in xrange(hauteurBlocs)],[[y+200,z+300]for y in xrange(largeurBlocs)for z in xrange(hauteurBlocs)],[[y+350,z+300]for y in xrange(largeurBlocs)for z in xrange(hauteurBlocs)],[[y+500,z+300]for y in xrange(largeurBlocs)for z in xrange(hauteurBlocs)]]
		level=0
		vaisseau=Vaisseau()
		Vaisseau.levels=0
		Vaisseau.vies=3
		ennemi=[]
		Vaisseau.score=0
		fenetre.fill(0)
		display.flip()
		
#/§None#/§None#/§
#/§nidhogg#/§15531#/§
#/§nidhogg#/§20060#/§
