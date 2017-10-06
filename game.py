import pygame
from pygame.locals import *
import sys
from functools import reduce
import random
import math

SCREEN_SIZE=(640,480)
WIDTH=13
HEIGHT=23
screen=0
sysfont=0
graphic=0
TETRIS=[[[-1, 0],[0,0],[1,0],[2,0]],[[0,1],[0,0],[0,-1],[0,-2]],[[-1,0],[0,0],[1,0],[2,0]],[[0,1],[0,0],[0,-1],[0,-2]],   #tate
         [[0,0],[1,0],[0,1],[1,1]],[[0,0],[1,0],[0,1],[1,1]],[[0,0],[1,0],[0,1],[1,1]],[[0,0],[1,0],[0,1],[1,1]],         #sikaku
         [[-1,0],[0,0],[1,0],[0,1]],[[0,-1],[0,0],[0,1],[1,0]],[[-1,0],[0,0],[1,0],[0,-1]],[[0,-1],[0,0],[0,1],[-1,0]],   #T-ji
         [[-1,1],[-1,0],[0,0],[1,0]],[[1,1],[0,1],[0,0],[0,-1]],[[1,-1],[1,0],[0,0],[-1,0]],[[-1,-1],[0,-1],[0,0],[0,1]], #L-ji(1)
         [[1,1],[1,0],[0,0],[-1,0]],[[1,-1],[0,-1],[0,0],[0,1]],[[-1,-1],[-1,0],[0,0],[1,0]],[[-1,1],[0,1],[0,0],[0,-1]], #L-ji(2)
         [[-1,1],[0,1],[0,0],[1,0]],[[1,1],[1,0],[0,0],[0,-1]],[[-1,1],[0,1],[0,0],[1,0]],[[1,1],[1,0],[0,0],[0,-1]],     #-ji(1)
         [[1,1],[0,1],[0,0],[-1,0]],[[-1,1],[-1,0],[0,0],[0,-1]],[[1,1],[0,1],[0,0],[-1,0]],[[-1,1],[-1,0],[0,0],[0,-1]]] #-ji(2)

class Graphic():
	def __init__(self):
		self.Colors=[[200,200,0],[0,180,0],[0,0,200],[0,200,255],[200,0,200],[255,0,0],[100,100,100]]
		self.Comment=["Next","Game Over","Press the Enter key","Press the Space key","Speed Up!!","Tetris"]
		self.Msg=list(map(self.MsgLoad,self.Comment))		

	def MsgLoad(self,filename):
		return sysfont.render(filename, True, (255,255,255))

class PlayerCharactor():
	def __init__(self):
		pass

	def reset(self):
		self.field = list(map(self.CreateBlock,range(0,HEIGHT)))
		self.sc=0
		self.x=5
		self.y=2
		self.score=0
		self.rotime=20
		self.hitime=5
		self.dtime=self.rotime
		self.time=self.dtime
		self.actiontime=0
		self.next=0
		self.rotate=0
		self.count=0
		self.nextcolor=random.randint(0,6)
		self.color=random.randint(0,6)
		list(map(self.BlockSet(self.field,self.x,self.y),TETRIS[self.color*4+self.rotate]))

	def CreateBlock(self,y):
		def _CreateBlock(x):
			if y<=1:
				return 1
			if y==HEIGHT-1:
				return 1
			if x==0:
				return 1
			if x>=WIDTH-2:
				return 1
			return 0
		return list(map(_CreateBlock,range(0,WIDTH)))

	def BlockSet(self,field,_x,_y):
		def _BlockSet(tetris):
			def __BlockSet(x,y):
				field[y+_y][x+_x]=self.color+2
			return __BlockSet(tetris[0],tetris[1])
		return _BlockSet

	def BlockClear(self,field,_x,_y):
		def _BlockClear(tetris):
			def __BlockClear(x,y):
				field[y+_y][x+_x]=0
			return __BlockClear(tetris[0],tetris[1])
		return _BlockClear

	def SearchBlock(self,field,_x,_y):
		def _SearchBlock(tetris):
			def __SearchBlock(x,y):
				result = True if field[y+_y][x+_x]>0 else False
				return result
			return __SearchBlock(tetris[0],tetris[1])
		return _SearchBlock
		
	def SearchLine(self,field):
		def _SearchLine(y):
			def __SearchLine(x):
				result=True if field[y][x]>1 else False
				return result
			return reduce(lambda _x,_y:_x and _y,list(map(__SearchLine,range(1,WIDTH-2))))
		return _SearchLine


	def ClearLine(self,field):
		def _ClearLine(result):
			def __ClearLine(y,_result):
				if _result==True:
					if field[y+self.count][1]<10:
						field[y+self.count]=[1]+[10]*(WIDTH-3)+[1]*2
					else:
						field[y+self.count]=[1]+[field[y+self.count][1]+1]*(WIDTH-3)+[1]*2
						if field[y+self.count][1]==30:
							field.pop(y+self.count)
							field.insert(2,[1]+[0]*(WIDTH-3)+[1]*2)
							self.score+=(self.count+1)*100
							self.count+=1
			return __ClearLine(HEIGHT-2-result[0],result[1])
		return _ClearLine

	def Rotate(self,dr):
		list(map(self.BlockClear(self.field,self.x,self.y),TETRIS[self.color*4+self.rotate]))
		self.rotate+=dr
		if self.rotate>=4:
			self.rotate=0
		if self.rotate<=-1:
			self.rotate=3
		result= list(map(self.SearchBlock(self.field,self.x,self.y),TETRIS[self.color*4+self.rotate]))
		if True in result:
			self.rotate-=dr
			if self.rotate>=4:
				self.rotate=0
			if self.rotate<=-1:
				self.rotate=3
		else:
			self.actiontime=10						
		list(map(self.BlockSet(self.field,self.x,self.y),TETRIS[self.color*4+self.rotate]))					
		
	def Move(self,dx):
		list(map(self.BlockClear(self.field,self.x,self.y),TETRIS[self.color*4+self.rotate]))
		self.x+=dx
		result= list(map(self.SearchBlock(self.field,self.x,self.y),TETRIS[self.color*4+self.rotate]))
		if True in result:
			self.x-=dx
		else:
			self.actiontime=8
		list(map(self.BlockSet(self.field,self.x,self.y),TETRIS[self.color*4+self.rotate]))

	def Down(self):
		list(map(self.BlockClear(self.field,self.x,self.y),TETRIS[self.color*4+self.rotate]))
		self.y+=1
		result= list(map(self.SearchBlock(self.field,self.x,self.y),TETRIS[self.color*4+self.rotate]))
		if True in result:
			self.y-=1
			self.next=1
		list(map(self.BlockSet(self.field,self.x,self.y),TETRIS[self.color*4+self.rotate]))
		self.time=self.dtime

	def update(self):
		self.time-=1
		self.actiontime-=1
		if self.next==0:
			if self.time>0:
				pressed = pygame.key.get_pressed()
				if self.actiontime<=0:
					if pressed[K_z]:
						self.Rotate(1)
					elif pressed[K_x]:
						self.Rotate(-1)
					elif pressed[K_LEFT]:
						self.Move(-1)
					elif pressed[K_RIGHT]:
						self.Move(1)
					else:
						if pressed[K_DOWN]:
							self.dtime=self.hitime
						else:
							self.dtime=self.rotime
						self.actiontime=0
			if self.time==0:
				self.Down()
		if self.next==1:
			result = list(map(self.SearchLine(self.field),range(HEIGHT-2,1,-1)))
			self.count=0
			list(map(self.ClearLine(self.field),enumerate(result)))
			result=reduce(lambda x,y:x or y,result)
			if result==False:
				self.next=2	
			if self.field[2][5]>0:
				self.next=3
				self.sc=0
		if self.next==2:
			if self.score>=3000:
				self.rotime=10
			else:
				self.rotime=20
			self.next=0
			self.x=5
			self.y=2
			self.time=self.dtime
			self.actiontime=0
			self.color=self.nextcolor
			self.nextcolor=random.randint(0,6)
			self.rotate=0
			list(map(self.BlockSet(self.field,self.x,self.y),TETRIS[self.color*4+self.rotate]))
		if self.next==3:
			self.sc+=1
			if self.sc>40:
				self.sc=0
			pressed = pygame.key.get_pressed()
			if pressed[K_SPACE]:
				self.next=4

	def DrawBlock(self,field):
		def _DrawBlock(x):
			def __DrawBlock(y):
				_x=20+x*20
				_y=y*20
				if field[y][x]>1 and field[y][x]<10:
					pygame.draw.rect(screen,(graphic.Colors[field[y][x]-2][0],graphic.Colors[field[y][x]-2][1],graphic.Colors[field[y][x]-2][2]),Rect(_x,_y,20,20))
					pygame.draw.rect(screen,(255,255,255),Rect(_x,_y,20,20),1)
				if field[y][x]>=10:
					colors=255-field[y][x]*5
					pygame.draw.rect(screen,(colors,colors,colors),Rect(_x,_y,20,20))
			return list(map(__DrawBlock,range(2,HEIGHT)))
		return _DrawBlock

	def DrawNextBlock(self,color):
		def _DrawNextBlock(tetris):
			def __DrawNextBlock(x,y):
				_x=310+20*x
				_y=90+20*y
				pygame.draw.rect(screen,(graphic.Colors[color][0],graphic.Colors[color][1],graphic.Colors[color][2]),Rect(_x,_y,20,20))
				pygame.draw.rect(screen,(255,255,255),Rect(_x,_y,20,20),1)
			return __DrawNextBlock(tetris[0],tetris[1])
		return _DrawNextBlock

	def draw(self):
		pygame.draw.rect(screen,(0,0,0),Rect(40,40,200,400))
		list(map(self.DrawBlock(self.field),range(0,WIDTH)))
		list(map(self.DrawNextBlock(self.nextcolor),TETRIS[self.nextcolor*4]))
		screen.blit(graphic.Msg[0], (280,50))
		pygame.draw.rect(screen,(255,255,255),Rect(39,39,201,401),1)
		pygame.draw.rect(screen,(255,255,255),Rect(37,37,205,405),1)
		if self.score>=3000:
			screen.blit(graphic.Msg[4], (280,400))			
		if self.next==3:
			if self.sc>20:
				screen.blit(graphic.Msg[1], (280,240))
				screen.blit(graphic.Msg[3], (280,280))


def Event_Processing(event):
	if event.type==QUIT:
		sys.exit()

def main():

	#初期化タイトル記入
	global screen
	global sysfont
	global graphic
	pygame.init()
	screen=pygame.display.set_mode(SCREEN_SIZE)
	pygame.display.set_caption("Tetris")
	pygame.mouse.set_visible(False)
	sysfont = pygame.font.SysFont(None, 40)
	graphic=Graphic()
	#画面更新時間を管理
	fps=pygame.time.Clock()
	player1=PlayerCharactor()
	player1.reset()
	sc=0
	game=0
	while True:
		fps.tick(60)
		if game==1:
			screen.fill((0,0,200))    #画面を青くする
			player1.update()			
			score =sysfont.render("SCORE:"+str(player1.score), True, (255,255,255))
			player1.draw()			
			screen.blit(score, (280,150))
		if game==0:
			screen.fill((0,0,0))    #画面を黒くする
			screen.blit(graphic.Msg[5], (280,100))
			if sc>20:
				screen.blit(graphic.Msg[2], (200,260))
			sc+=1;
			if sc>40:
				sc=0
		if player1.next==4:
			game=0
		pressed = pygame.key.get_pressed()
		if pressed[K_RETURN]:
			if game==0:
				player1.reset()
				game=1
		if pressed[K_ESCAPE]:
			break
		pygame.display.update()

		#イベント処理
		list(map(Event_Processing,pygame.event.get()))

if __name__=='__main__':
	main()
