REST=[] #牌库
#CURRENTPLAYER=int(4*random.random())+1 #选定庄家
CURRENTPLAYER=1 #调试用
import random
class mahjong(object):
    def __init__(self,value,kind):
        self.value=value
        self.kind=kind
    def selfprint(self):
        print '%s:%s'%(self.value,self.kind),
        return '%s:%s'%(self.value,self.kind)
    def ishua(self):
        if self.kind=='Hua':
            return 1
        return 0

class zi(mahjong):
    def __init__(self,value,kind):
        self.value=value
        self.kind=kind


class feng(mahjong):
    def __init__(self,value,kind='Feng'):
        self.value=value
        self.kind=kind
    def selfprint(self):
        d={1:'dong',2:'nan',3:'xi',4:'bei',5:'zhong',6:'fa',7:'bai'}
        print '%s:%s'%(d[int(self.value)],self.kind),
        return '%s:%s'%(d[int(self.value)],self.kind)

class hua(mahjong):
    def __init__(self,value,kind='Hua'):
        self.value=value
        self.kind=kind
    def selfprint(self):
        d={1:'chun',2:'xia',3:'qiu',4:'dong',5:'mei',6:'lan',7:'zhu',8:'ju'}
        print '%s:%s'%(d[int(self.value)],self.kind),
        return '%s:%s'%(d[int(self.value)],self.kind)


class wan(zi):
    def __init__(self,value,kind='Wan'):
        self.value=value
        self.kind=kind

class tiao(zi):
    def __init__(self,value,kind='Tiao'):
        self.value=value
        self.kind=kind

class tong(zi):
    def __init__(self,value,kind='Tong'):
        self.value=value
        self.kind=kind

class player(object):
    def __init__(self,name,num,card=[]):
        self.name=name
        self.num=num
        self.card=card

    def showcard(self):
        print '%s has %s cards:'%(self.name,len(self.card))
        for i in range(len(self.card)):
            self.card[i].selfprint()
            print '|',
        print
        for i in range(len(self.card)+1):
            print '%s\t'%i,
        print
        return


    def buhua(self):
        global REST
        self.card.append(REST[-1])
        REST=REST[:-1]
        if self.card[-1].ishua():
            self.buhua()
        return

    def grab(self):
        global REST
        self.card.append(REST[0])
        REST=REST[1:]
        if self.card[-1].ishua():
            self.buhua()
        return

    def sorting(self):
        for i in range(len(self.card)):
            if self.card[i].kind=='Hua':
                self.card.pop(i)
                self.buhua()
                self.sorting()
        def order(x,y):
            d1={'Wan':1,'Tiao':2,'Tong':3,'Feng':4,'Hua':5}
            if d1[x.kind]>d1[y.kind]:
                return 1
            if d1[x.kind]==d1[y.kind]:
                if x.value>y.value:
                    return 1
                elif x.value<y.value:
                    return -1
                return 0
            if d1[x.kind]<d1[y.kind]:
                return -1
        self.card=sorted(self.card,order)
        return

    def deliver(self,i=-1):
        global CURRENTPLAYER
        print '%s delivers'%(self.name),
        self.card[i].selfprint()
        print
        self.card.pop(i)
        self.sorting()
        CURRENTPLAYER=CURRENTPLAYER%4+1
        return






def deliver(rest,a=player('a',1),b=player('b',2),c=player('c',3),d=player('d',4)):
    global REST
    ac=[]
    bc=[]
    cc=[]
    dc=[]
    for i in range(12):
        ac.append(REST[4*i])
        bc.append(REST[4*i+1])
        cc.append(REST[4*i+2])
        dc.append(REST[4*i+3])
    ac.append(REST[48])
    ac.append(REST[52])
    bc.append(REST[49])
    cc.append(REST[50])
    dc.append(REST[51])
    REST=REST[53:]
    a.card=ac
    b.card=bc
    c.card=cc
    d.card=dc
    a.sorting()
    b.sorting()
    c.sorting()
    d.sorting()



def sorting(player):
    def order(x,y):
        d1={'Wan':1,'Tiao':2,'Tong':3,'Feng':4,'Hua':5}
        if d1[x.kind]>d1[y.kind]:
            return 1
        if d1[x.kind]==d1[y.kind]:
            if x.value>y.value:
                return 1
            elif x.value<y.value:
                return -1
            return 0
        if d1[x.kind]<d1[y.kind]:
            return -1
    player.card=sorted(player.card,order)
    return





w=[wan(1),wan(1),wan(1),wan(1)]
s=[tiao(1),tiao(1),tiao(1),tiao(1)]
t=[tong(1),tong(1),tong(1),tong(1)]
f=[feng(1),feng(1),feng(1),feng(1)]
h=[hua(1)]

for i in range(8):
    for j in range(4):
        w.append(wan(i+2))
        s.append(tiao(i+2))
        t.append(tong(i+2))


for i in range(6):
    for j in range(4):
        f.append(feng(i+2))

for i in range(7):
    h.append(hua(i+1))

REST=w
REST.extend(s)
REST.extend(t)
REST.extend(f)
REST.extend(h)

playername=raw_input('Start a new GAME? Set a name!\n')
a=player(playername,1)
b=player('b',2)
c=player('c',3)
d=player('d',4)



random.shuffle(REST)

deliver(REST,a,b,c,d) #尝试修改 只需输入第一个摸牌的人即可


a.deliver() #为保证游戏继续 
while(len(REST)!=0):
    dic={1:a,2:b,3:c,4:d}
    p=dic[CURRENTPLAYER]
    if p==a:
        print 'yes'
        p.grab()
        p.showcard()
        x=int(raw_input('which?'))
        p.deliver(x)
    p=dic[CURRENTPLAYER]
    p.grab()
    p.deliver()





#print 'The rest card is %s left, they are:'%(len(REST))
#for i in range (len(REST)):
#    REST[i].selfprint()
