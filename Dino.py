
import pygame
import random
import os
import neat

clock= pygame.time.Clock()
display_width=1300
display_height=600

black=(0,0,0)
white=(255,255,255)

DINO_IMG=[pygame.image.load(os.path.join("dinoimgs","dinorun0000.png")),pygame.image.load(os.path.join("dinoimgs","dinorun0001.png")),pygame.image.load(os.path.join("dinoimgs","dinoduck0000.png")),pygame.image.load(os.path.join("dinoimgs","dinoduck0001.png")),pygame.image.load(os.path.join("dinoimgs","dinoJump0000.png"))]
OBS_IMG=[pygame.image.load(os.path.join("dinoimgs","berd.png")),pygame.image.load(os.path.join("dinoimgs","berd2.png")),pygame.image.load(os.path.join("dinoimgs","cactusBig0000.png")),pygame.image.load(os.path.join("dinoimgs","cactusSmall0000.png")),pygame.image.load(os.path.join("dinoimgs","cactusSmallMany0000.png"))]
BASE_IMG=pygame.image.load(os.path.join("dinoimgs","Base.png"))

class Dino:
    IMGS=DINO_IMG
    img_count=0

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.u=0
        self.t=0
        self.dino_img=self.IMGS[0]
        self.position=self.y
        self.duck=0
        self.duck_count=0

    def jump(self):
        if(self.y==self.position):
            self.u=-25
            self.t=0
            self.y+=.1
            self.duck=0
        self.duck=0




    def straight(self):
        self.duck=0

    def ducki(self):
        self.duck=1





    def move(self):

        if(self.duck==1):
            self.dino_img=self.IMGS[2]
        else:
            self.dino_img=self.IMGS[0]



        if(self.y!=self.position):
            self.t+=.5
            add=self.u*self.t + .5*9.8* self.t**2
            self.y+=add
            if(self.y>self.position):
                self.y=self.position
        else:
            self.y=self.position

    def draw(self,win):
        if(self.duck==1):
            if(self.duck_count==0):
                self.duck_count=1
                win.blit(self.IMGS[2],(self.x,self.y+40))
            else:
                self.duck_count=0
                win.blit(self.IMGS[3],(self.x,self.y+40))
        elif(self.img_count==0):
            self.img_count=1
            win.blit(self.IMGS[0],(self.x,self.y))
        else:
            self.img_count=0
            win.blit(self.IMGS[1],(self.x,self.y))


    def get_mask(self):
        return pygame.mask.from_surface(self.dino_img)


class Obs:
    IMGS=OBS_IMG
    def __init__(self,x,y,type):
        self.x=x
        self.y=y
        self.type=type
        self.vel=25
        self.bird_count=0
        self.obj_img=self.IMGS[0]
        if (self.type == 0):
           self.obj_img=self.IMGS[0]

        elif (self.type == 1):
            self.obj_img = self.IMGS[2]

        elif (self.type == 2):
            self.obj_img = self.IMGS[3]

        elif (self.type == 3):
            self.obj_img=self.IMGS[4]




    def move(self):
        self.x-=self.vel

    def draw(self,win):
        if(self.type==0):
            if(self.bird_count==0):
                self.bird_count=1
                win.blit(self.IMGS[0], (self.x, self.y))
            else:
                self.bird_count=0
                win.blit(self.IMGS[1], (self.x, self.y))

        elif (self.type == 1):
            win.blit(self.IMGS[2], (self.x, self.y))

        elif (self.type == 2):
            win.blit(self.IMGS[3], (self.x, self.y))

        elif (self.type == 3):
            win.blit(self.IMGS[4], (self.x, self.y))


    def collide(self,dino):
        dino_mask=dino.get_mask()
        obs_mask=pygame.mask.from_surface(self.obj_img)


        if(dino.dino_img==DINO_IMG[2]):
            obs_offset = (self.x-dino.x,self.y - round(dino.y+40))
        else:
            obs_offset = (self.x - dino.x, self.y - round(dino.y ))



        b_point=dino_mask.overlap(obs_mask,obs_offset)


        if( b_point):
            return True
        else:
            return False








class Base:
    IMGS=BASE_IMG
    def __init__(self,y):
        self.y=y
        self.vel=25
        self.x1=0
        self.x2=self.IMGS.get_width()-200
        self.x3=2*(self.IMGS.get_width())-200
    def move(self):

        self.x1-=self.vel
        self.x2-=self.vel
        self.x3-=self.vel

        if(self.x1+self.IMGS.get_width()<0):
            self.x1=2*(self.IMGS.get_width())-200
        if (self.x2 + self.IMGS.get_width() < 0):
            self.x2 = 2*(self.IMGS.get_width())-200
        if (self.x3 + self.IMGS.get_width() < 0):
            self.x3 = 2 * (self.IMGS.get_width())-200


    def draw(self,win):
        win.blit(self.IMGS, (self.x1, self.y))
        win.blit(self.IMGS, (self.x2, self.y))
        win.blit(self.IMGS, (self.x3, self.y))



def draw_window(win,dino,base,obs):
    win.fill(white)
    base.draw(win)
    for ob in obs:
        ob.draw(win)

    for d in dino:
        d.draw(win)
    pygame.display.update()



def main(genomes,config):

    dino=[]
    ge=[]
    nets=[]
    for _, g in genomes:
        g.fitness = 0
        net=neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        dino.append(Dino(100,300))
        ge.append(g)


    run=True
    win=pygame.display.set_mode((display_width,display_height))
    base=Base(130)

    obs=[Obs(1500,280,1)]
    while(run):
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                run=False
                pygame.quit()
                quit()
            if(event.type==pygame.KEYDOWN):
                if(event.key==pygame.K_UP):
                    pass
                if(event.key==pygame.K_DOWN):
                    pass
            if(event.type==pygame.KEYUP):
                pass

        ob_ind = 0
        if (len(dino) > 0):
            if len(obs) > 1 and dino[0].x > obs[0].x + obs[0].obj_img.get_width():
                ob_ind = 1
        else:
            run = False


        for z,d in enumerate(dino):
            d.move()
            ge[z].fitness+=0.1
            output = nets[z].activate((d.y, abs(d.y - obs[ob_ind].obj_img.get_height()),abs(obs[ob_ind].x-d.x),
                                           obs[ob_ind].obj_img.get_height(), obs[ob_ind].obj_img.get_width()))

            if(output[0]>0.5):
                d.jump()
            elif(output[0]<-0.5):
                d.ducki()
            else:
                d.straight()



        for obi in obs:
            for x,d in enumerate(dino):
                if(obi.collide(d)):
                    ge[x].fitness -= 1
                    dino.pop(x)
                    nets.pop(x)
                    ge.pop(x)

        for y,d in enumerate(dino):
            if(d.x>obs[0].x):
                ge[y].fitness+=5






        if(len(obs)<3):
            temp_add=0
            random_type=random.randrange(0,4)
            random_range=random.randrange(800,1200)
            if(random_type==0):
                temp_add=random.randrange(10,110)
            if(random_type==1):
                temp_add=40
            obs.append(Obs(obs[-1].x+random_range,320-temp_add,random_type))

        if(obs[0].x+obs[0].obj_img.get_width()<0):
            obs.pop(0)

        for ob in obs:
            ob.move()

        base.move()
        clock.tick(30)
        draw_window(win, dino,base,obs)











def run(config_path):
    config=neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
    p=neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats=neat.StatisticsReporter()
    p.add_reporter(stats)
    winner=p.run(main,50)




if __name__=="__main__":
    local_dir = os.path.dirname(__file__)
    config_path=os.path.join(local_dir,"NEAT.txt")
    run(config_path)