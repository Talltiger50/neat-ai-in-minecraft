import time

from javascript import require, On, Once

mineflayer = require("mineflayer")
Vec3=require("Vec3")

class createAI():
    def __init__(self, ip, port, name):
        self.bot = mineflayer.createBot({
            "host": 'localhost',
            "port": port,
            "username": name
        })
        self.joined = False
        self.name=name
        self.offset=(0,-1,0)
        @On(self.bot, "spawn")
        def join(*args):
            self.joined = True
            #self.bot.chat("joined")

    def chat(self,text):
        self.bot.chat(text)

    def move(self, direction, length=1):#move bot
        self.bot.setControlState(direction, True)
        time.sleep(length)
        self.bot.setControlState(direction, False)

    def pos(self):
        return (self.bot.entity.position.x,self.bot.entity.position.y,self.bot.entity.position.z)

    def Whenjoined(self): #tells code when joined
        return self.joined

    def getBlockIds(self,size,offset,default=True):
        if default:
            x2 ,y2,z2=(-size,-1,-size)
        else:
            x2, y2, z2 = offset
        #print(self.bot.entity.position.y)
        blocks=[(self.bot.blockAt(Vec3(self.bot.entity.position.x+x,self.bot.entity.position.y+y,self.bot.entity.position.z+z)).stateId) for z in range(z2,size+z2) for y in range(y2,size+y2) for x in range(x2,size+x2)]
        return blocks

    def botfaceing(self):
        return self.bot.entity.yaw

    def changeRot(self,rotation):
        self.bot.look(rotation[0],rotation[1])

    def Name(self):
        return self.name

    def getBlockNames(self,size,offset):
        x2,y2,z2=offset
        #print(self.bot.entity.position.y)
        blocks=[(self.bot.blockAt(Vec3(self.bot.entity.position.x+x,self.bot.entity.position.y+y,self.bot.entity.position.z+z)).displayName) for z in range(z2,size+z2) for y in range(y2,size+y2) for x in range(x2,size+x2)]
        return blocks

    def getBlock(self,size,offset):
        x2,y2,z2=offset
        #print(self.bot.entity.position.y)
        blocks=[(self.bot.blockAt(Vec3(self.bot.entity.position.x+x,self.bot.entity.position.y+y,self.bot.entity.position.z+z))) for z in range(z2,size+z2) for y in range(y2,size+y2) for x in range(x2,size+x2)]
        return blocks

    def getinventory(self):
        outslot=[]
        slots=self.bot.inventory.slots
        for i in range(46):
            try:
                outslot.append(slots[i].Item.name)

            except Exception:
                outslot.append(-1)
        return outslot