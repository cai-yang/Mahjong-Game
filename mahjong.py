#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import random
REST=[] #牌库
CURRENTPLAYER=int(4*random.random())+1 #选定庄家
CURRENTDELIVERY=None
PENGINDEX=0
GANGINDEX=0

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
    def __init__(self,name,num,gateway=[],handcard=[],flowers=[],flag=1):
        self.name=name
        self.num=num
        self.handcard=handcard
        self.gateway=gateway
        self.flowers=flowers
        self.flag=flag

    def showcard(self):
        if self.gateway!=[]:
            print 'gateways:',
            for i in range(len(self.gateway)):
                self.gateway[i].selfprint()
                print '|',
            print
        print '%s handcards:'%(len(self.handcard))
        for i in range(len(self.handcard)):
            print '%2s|'%(int(i+1)),
            self.handcard[i].selfprint()
            print
        #for i in range(len(self.handcard)):

        #print
        return


    def buhua(self):
        global REST
        self.handcard.append(REST[-1])
        REST=REST[:-1]
        if self.handcard[-1].ishua():
            self.flowers.append(self.handcard[-1])
            self.handcard.pop(-1)
            self.buhua()
        return

    def grab(self):
        global REST
        self.handcard.append(REST[0])
        REST=REST[1:]
        if self.handcard[-1].ishua():
            self.flowers.append(self.handcard[-1])
            self.handcard.pop(-1)
            self.buhua()
        GANGTAR=self.handcard[-1]
        i=0
        j=0
        while (i<len(self.handcard)-1 and j<3):
            if self.handcard[i].value==GANGTAR.value and self.handcard[i].kind==GANGTAR.kind:
                GANGINDEX=i-2
                j=j+1
                print 'have %s'%(j)
            i=i+1
        if i==len(self.handcard)-1:
            if j>=3:
                self.gang()
            else:
                pass
        else:
            self.gang()

        return

    def sorting(self):
        for i in range(len(self.handcard)):
            if self.handcard[i].kind=='Hua':
                self.flowers.append(self.handcard[i])
                self.handcard.pop(i)
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
        self.handcard=sorted(self.handcard,order)
        return

    def deliver(self,i=0):
        global CURRENTDELIVERY
        global CURRENTPLAYER
        while (i<0 or i>len(self.handcard)):
            i=int(raw_input('Please type in the correct number(between 1 and %s)'%(len(self.handcard))))
        print '%s delivers'%(self.name),
        self.handcard[i-1].selfprint()
        print
        CURRENTDELIVERY=self.handcard[i-1]
        self.handcard.pop(i-1)
        self.sorting()
        CURRENTPLAYER=CURRENTPLAYER%4+1
        return

    def canpeng(self):
        global CURRENTDELIVERY
        global PENGINDEX
        j=0
        i=0
#        for i in range(len(self.handcard)):
        while (i<len(self.handcard) and j<2):
            if self.handcard[i].value==CURRENTDELIVERY.value and self.handcard[i].kind==CURRENTDELIVERY.kind:
                PENGINDEX=i-1
                j=j+1
                print 'have %s'%(j)
            i=i+1
        if i==len(self.handcard):
            if j>=2:
                return 1
            else:
                return 0
        else:
            return 1

    def peng(self):
        global PENGINDEX
        global CURRENTPLAYER
        self.showcard()
        print PENGINDEX
        for i in range(3):
            self.gateway.append(CURRENTDELIVERY)
        for i in range(2):
            self.handcard.pop(PENGINDEX)
        self.sorting()
        CURRENTPLAYER=self.num
        return

    def cangang(self):#期待修复自己gang
        global CURRENTDELIVERY
        global GANGINDEX
        j=0
        i=0
#        for i in range(len(self.handcard)):
        while (i<len(self.handcard) and j<3):
            if self.handcard[i].value==CURRENTDELIVERY.value and self.handcard[i].kind==CURRENTDELIVERY.kind:
                GANGINDEX=i-2
                j=j+1
                print 'have %s'%(j)
            i=i+1
        if i==len(self.handcard):
            if j>=3:
                return 1
            else:
                return 0
        else:
            return 1

    def gang(self):
        global GANGINDEX
        global CURRENTPLAYER
        self.showcard()
        print GANGINDEX
        for i in range(4):
            self.gateway.append(CURRENTDELIVERY)
        for i in range(3):
            self.handcard.pop(GANGINDEX)
        self.buhua()
        self.sorting()
        CURRENTPLAYER=self.num
        return




def deliver2(i):
    global REST
    global PLAYERDICT
    q=[[],[],[],[]]
    for x in range(3):
        for y in range(4):
            q[0].append(REST[16*x+y])
            q[1].append(REST[16*x+4+y])
            q[2].append(REST[16*x+8+y])
            q[3].append(REST[16*x+12+y])
    q[0].append(REST[48])
    q[0].append(REST[52])
    q[1].append(REST[49])
    q[2].append(REST[50])
    q[3].append(REST[51])
    REST=REST[53:]
    w=PLAYERDICT
    for y in range(4):
        w[i].handcard=q[y]
        w[i].sorting()
        i=i%4+1




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
    a.handcard=ac
    b.handcard=bc
    c.handcard=cc
    d.handcard=dc
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
    player.handcard=sorted(player.handcard,order)
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

#playername=raw_input('Start a new GAME? Set a name!\n')
a=player('playername',1)
b=player('b',2)
c=player('c',3)
d=player('d',4)

PLAYERDICT={1:a,2:b,3:c,4:d}



random.shuffle(REST)

#deliver(REST,a,b,c,d) #尝试修改 只需输入第一个摸牌的人即可
print CURRENTPLAYER
deliver2(CURRENTPLAYER)
print len(a.handcard)
PLAYERDICT[CURRENTPLAYER].deliver()
while(len(REST)!=0):
    print 'a have %s cards'%len(a.handcard)
    p=PLAYERDICT[CURRENTPLAYER]
    if p==a:
        print 'yes'
        if p.flag==1:
            p.grab()
        p.flag=1
        p.showcard()
        x=int(raw_input('which?'))
        p.deliver(x)
    p=PLAYERDICT[CURRENTPLAYER]
    p.grab()
    p.deliver()
    print CURRENTPLAYER
    if a.canpeng():
        print a.canpeng()
        a.showcard()
        CURRENTDELIVERY.selfprint()
        i=raw_input('is delivered! Peng?[y/n]')
        if i=='y':
            a.peng()
            a.flag=0
    else:
        print a.canpeng()







#print 'The rest card is %s left, they are:'%(len(REST))
#for i in range (len(REST)):
#    REST[i].selfprint()
