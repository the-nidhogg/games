#include <stdio.h>
#include <stdlib.h>
#include <time.h>

//nombre_aleatoire = (rand() % (MAX - MIN + 1)) + MIN;

int appels=0;
int longeur=2;
int tete[2]={300,196};
int corps[(600/4)*(400/4)][2]={0};
int food=0;
int food_pos[2]={0,0};


void initialise(){
		srand(time(NULL));}	

void feeding(){
	food=1;
	food_pos[0]=(rand() % (124))*4;
	food_pos[1]=(rand() % (99))*4;
}

void append(){
	corps[longeur][0]=396;
	corps[longeur][1]=596;
	longeur++;
}

void init(){
	int i;
	longeur=2;
	for(i=0;i<(600/4)*(400/4);i++){
		corps[i][0]=0;
		corps[i][1]=0;}
	tete[0]=300;
	tete[1]=196;
	corps[0][0]=204;
	corps[0][1]=300;
	corps[1][0]=200;
	corps[1][1]=300;
}

int get(){
	int a;
	if (appels==0){
		appels++;
		a=tete[0]+tete[1]*1000;}
	else{
		a=corps[appels-1][0]*1000+corps[appels-1][1];
		appels++;
		if(appels-1>longeur){
			appels=0;
			a=-1;}}
	return a;
}
int getFood(){
	int a=food_pos[0]+food_pos[1]*1000;
	return a;
}

int deplacement(int sens){
	if (food==0)feeding();
	int i;
	int notPerdu=1;
	for(i=longeur;i>=0;i--){
		corps[i][0]=corps[i-1][0];
		corps[i][1]=corps[i-1][1];}
	corps[0][0]=tete[1];
	corps[0][1]=tete[0];
	switch (sens){
		case 1:{
			tete[1]-=4;
			break;}
		case 2:{
			tete[0]+=4;
			break;}
		case -1:{
			tete[0]-=4;
			break;}
		case -2:{
			tete[1]+=4;
			break;}
		break;
		}
	if (tete[0]>596 | tete[0]<0 | tete[1]>396 | tete[1]<4){notPerdu=0;}
	for(i=0;i<longeur;i++){
		if (tete[0]==corps[i][1] && tete[1]==corps[i][0]){
			notPerdu=0;
			break;}
			}
	if (tete[0]==food_pos[0] && tete[1]==food_pos[1]){
		feeding();
		append();
	}
	return notPerdu;
}

void eat(){
	longeur++;
	return ;
}
