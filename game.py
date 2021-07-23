#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 18:45:12 2020

@author: huyvo
"""
import numpy as np
import random
slist=[]


class User(object):
    # user have public variable: name
    def __init__(self,name,gender,Map,location=(3,-3)):
        self.name=name
        self.gender=gender
        self.stuff=[] # list of  special objects
        
        
        self.onhand=empty()
        self.roomnum=None
        self.location=location
        self.maxcapacity=2
        self.usedcapacity=0
        self.gamestatus=False
        self.Map=Map
        
        #special object status
        self.bag=False
        self.flash_light=False
        
    def __str__(self):
        return self.name
        
        
    def get_location(self):
        return self.location
    def addcapacity(self):
        # update used capacity raise Value error is cannot
        if self.usedcapacity==self.maxcapacity:
            raise ValueError
        else:
            self.usedcapacity=self.usedcapacity+1
    def startgame(self):
        self.gamestatus= True
    def gameover(self):
        self.gamestatus=False
    def check_capacity(self):
        #raise value error if used capacity exceed the maximum capacity
        if self.usedcapacity>self.maxcapacity:
            raise ValueError
    def get_usedcapacity(self):
        #return usable capcaity
        return self.maxcapacity-self.usedcapacity
    
    
    

    def pickup(self):
        # update user stirage and activate if yes
        stuff=self.Map.mapdict[self.location]
        if str(stuff)=='empty' or str(stuff)=='wall':
            print('wow, nice workout :) ')
        elif not stuff.pickstatus:
            stuff.pick()
        elif self.get_usedcapacity()>0:
            self.stuff.append(stuff)
            self.addcapacity()
            
            stuff.activate(self)
            self.Map.mapdict[self.location]=empty()
            print('you pick up '+str(stuff))
            stuff.pick()
        else:
            print('you need extra space, please drop some stuffs')

    def use(self):
        if str(self.onhand)=='axe':
            if self.location==(12,14) or self.location==(14,14):
                self.onhand.use(self.Map.mapdict[(13,14)])
                # self.Map.replace_obj((13,14),empty())
                return
            elif self.location==(10,14) or self.location==(8,14):
                self.onhand.use(self.Map.mapdict[(9,14)])
                # self.Map.replace_obj((9,14),empty())
                return
            elif self.location==(2,12) :
                self.onhand.use(self.Map.mapdict[(2,13)])
                # self.Map.replace_obj((2,13),empty())
                return
            elif self.location==(15,2) :
                self.onhand.use(self.Map.mapdict[(14,2)])
                # self.Map.replace_obj((14,2),empty())
                return
            else:
                return self.onhand.use(self.Map.mapdict[self.location])
        if str(self.onhand)=='hammer':
            if self.location==(2,14):
                return self.onhand.use(self.Map.mapdict[(3,14)])
            elif self.location==(15,14):
                return self.onhand.use(self.Map.mapdict[(15,13)])
            elif self.location==(2,17):
                return self.onhand.use(self.Map.mapdict[(2,16)])
            elif self.location==(10,17):
                print('banggg! the floor is break')
                return self.Map.replace_obj(self.location,breakfloor())

            else:
                return self.onhand.use(self.Map.mapdict[self.location])
        if str(self.onhand)=='GOLD-key':
            if self.location==(2,15):
                return self.onhand.use(self.Map.mapdict[(2,16)],self)
            else:
                return self.onhand.use(self.Map.mapdict[self.location],self)
        if str(self.onhand)=='red-laser':
            return self.onhand.use(self)
        if str(self.onhand)=='Panties':
            return self.onhand.use(self)
        return self.onhand.use(self)
    def choose(self,obj):
        if obj in self.stuff:
            self.onhand=obj
        else:
            print('what you say again')
    def drop(self):
        #update user storage
        
        if self.Map.check_object(self):
            print('cant drop, there is something here')
        else:
        
        
        
            if str(self.onhand)!='empty':
                
                
                try:
                    self.onhand.deactivate(self)
                    self.stuff.remove(self.onhand)
                    self.usedcapacity=self.usedcapacity-1
                    self.bagstatus()
                    self.check_capacity()
                    self.Map.mapdict[self.location]=self.onhand
                    print('you drop '+str(self.onhand))
                    self.onhand.drop()
                    self.onhand=empty()
                    
                except (ValueError):
                    self.stuff.append(self.onhand)
                    self.usedcapacity=self.usedcapacity+1
                    self.onhand.activate(self)
                    self.bagstatus()
                    
                    print('cannot drop')
                        
            else:
                print('choose something')
    def check_stuff(self):
        #check user tools
        print (self.stuff)
        return self.stuff
    def move_up(self):
        # update location
        x,y=  self.location
        y=y+1
        if self.Map.check_location((x,y)):
            self.location=(x,y)
            y=y-1
            if self.Map.check_object(self):
                            
                if self.Map.get_object(self.location).enter:
                    if self.Map.get_object(self.location).Type()=='boss':
                        self.Map.get_object(self.location).etalk()
                    else:
                        self.Map.get_object(self.location).talk()

                    
                elif self.Map.get_object(self.location).Type()=='special_object':
                    print('cant move')
                    self.Map.get_object(self.location).talk()
                    self.location=(x,y)
                elif self.Map.get_object(self.location).Type()=='boss':
                    print('cant move')
                    self.Map.get_object(self.location).talk(self)
                    self.location=(x,y)
            

        else:
            print('ouch, walls!')
    def move_down(self):
        # update location
        x,y=  self.location
        y=y-1
        if self.Map.check_location((x,y)):
            self.location=(x,y)
            y=y+1
            if self.Map.check_object(self):
                    
                if self.Map.get_object(self.location).enter:
                    if self.Map.get_object(self.location).Type()=='boss':
                        self.Map.get_object(self.location).etalk()
                    else:
                        self.Map.get_object(self.location).talk()
                elif self.Map.get_object(self.location).Type()=='special_object':
                    print('cant move')
                    self.Map.get_object(self.location).talk()
                    self.location=(x,y)
                elif self.Map.get_object(self.location).Type()=='boss':
                    print('cant move')
                    self.Map.get_object(self.location).talk(self)
                    self.location=(x,y)
        else:
            print('cant move!!')
    def move_left(self):
        # update location
        x,y=  self.location
        x=x-1
        if self.Map.check_location((x,y)):
            self.location=(x,y)
            x=x+1
            if self.Map.check_object(self):
                                
                if self.Map.get_object(self.location).enter:
                    if self.Map.get_object(self.location).Type()=='boss':
                        self.Map.get_object(self.location).etalk()
                    else:
                        self.Map.get_object(self.location).talk()
                elif self.Map.get_object(self.location).Type()=='special_object':
                    print('cant move')
                    self.Map.get_object(self.location).talk()
                    self.location=(x,y)
                elif self.Map.get_object(self.location).Type()=='boss':
                    print('cant move')
                    self.Map.get_object(self.location).talk(self)
                    self.location=(x,y)
        else:
            print('walls everywhere')    
    def move_right(self):
        # update location
        x,y=  self.location
        x=x+1
        if self.Map.check_location((x,y)):
            self.location=(x,y)
            x=x-1
            if self.Map.check_object(self):
                                
                if self.Map.get_object(self.location).enter:
                    if self.Map.get_object(self.location).Type()=='boss':
                        self.Map.get_object(self.location).etalk()
                    else:
                        self.Map.get_object(self.location).talk()
                elif self.Map.get_object(self.location).Type()=='special_object':
                    print('cant move')
                    self.Map.get_object(self.location).talk()
                    self.location=(x,y)
                elif self.Map.get_object(self.location).Type()=='boss':
                    print('cant move')
                    self.Map.get_object(self.location).talk(self)
                    self.location=(x,y)
        else:
            print('can walls break?')    
    def openbag(self):
        a=[str(i) for i in self.stuff]
        print ('you have: '+str(a))
    def list_command(self):
        return self.Map.get_command_list()
        # (x,y)=self.location
        # if self.Map.check_location((x,y)):
        #     return self.Map.get_map()[x,y].get_command_list()
    def talk(self):
        return self.Map.mapdict[self.location].talk()
    def save(self,savelist):   
        self.Map.save(self,savelist)
    
    
    
# use function of special object    


# bag stuff    
    def bagstatus(self):
        #update status of the bag and max capacity
        str_stuff=[str(i) for i in self.stuff]
        if 'bag' in str_stuff:  
            self.bag=True
            self.maxcapacity=8
        else:
            self.bag=False
            self.maxcapacity=2
# flash light stuff    


    
    
    
    
    
    
##################################            
class Map(object):
    def __init__(self,room_list,road_list,special_location):
        #special location: list contain location class with special objects
        self.room_list=room_list
        self.road_list=road_list
        self.mapdict={}
        self.gamer={}
        self.command_list={'up':'move up','w':'move up','down':'move down','s':'move down','left':'move left','a':'move left','right':'move right','d':'move right','pick':'pick up','j':'pick up','drop':'drop','k':'drop','use':'use','u':'use','--toolsname--':'choose','talk':'talk','t':'talk','open':'open','o':'open','location':'location','l':'location', 'close':'close','c':'close','y':'save','save':'save'}

        self.special_location=special_location
    def check_location(self,location):
        return location in self.mapdict
    def get_map(self):
        return self.mapdict
    def get_object(self,location):
        if self.check_location(location):
            (x,y)=location
            return self.mapdict[location]
        print('no location find')    
    def check_object(self,user):
        #if location has objects return true
        return str(self.get_object(user.location))!='empty'
    def build_map(self):
        for i in self.room_list:
            self.mapdict.update(i.get_dict())
        for j in self.road_list:
            self.mapdict.update(j.get_dict())
        return self.mapdict
    def update_map(self):
        for i in self.special_location:
            if self.check_location(i.get_coordinate()):
                self.mapdict[i.get_coordinate()]=i.get_object()
            else:
                print('please check the location: '+i)
                
    def replace_obj(self,location,obj):
        self.mapdict[location]=obj
    def get_command_list(self):
        return self.command_list
    def print_location(self,location):
        return '{} : {}'.format(location,self.get_object(location))
    def save(self,user,savelist):
        savelist.append(user)
#################################            
class room(object):
    def __init__(self,l,w,startingpoint):
        self.l=l
        self.w=w
        self.locationdict={}
        self.room=[]
        self.startingpoint=startingpoint
        
    def  setup_room(self):
        (x,y)=self.startingpoint
        self.room=[(j+x,i+y) for i in range(self.w) for j in range(self.l)]

        return self.room
    def setup_dict(self)   :
        #speacial_location=['stuff',(0,0)]
        e=empty()
        for (x,y) in self.room:
            
                if not (x,y) in self.locationdict:
                    self.locationdict[(x,y)]=e
                

        return self.locationdict
    def get_dict(self):
        return self.locationdict
    # def __str__(self):
        
    #     return str(self.locationdict)

    
    
##################
# build a location class 
#location calss use to store location and objects store in that location
class location(object):
    def __init__(self,coordinate_x,coordinate_y,special_object):
        #function is the list of thing that location can take in as a command from user if different raise value error
        self.coordinate_x=coordinate_x
        self.coordinate_y=coordinate_y
        self.special_object=special_object
        self.location={(coordinate_x,coordinate_y):special_object}
    def get_coordinate(self):
        return (self.coordinate_x,self.coordinate_y)
    def get_object(self):
        return self.special_object

    
    def __str__(self):
        return '({},{}) : {}'.format(self.coordinate_x, self.coordinate_y,self.special_object)
###################

class road(room):
    pass
################## 
#class stuff(object)    
class special_object(object):
    

        def __init__(self):
            pass
        def activate(self,user):
            pass
        def deactivate(self,user):
            pass
        def pick(self):
            pass
        def drop(self):
            pass
        def Type(self):
            return 'special_object'
class empty(special_object):
    def __init__(self):
        self.pickstatus=False
        self.enter=True
    def __str__(self):
        return 'empty'
    def use(self,user):
        print('to understand and ultilize emptyness is a true master.')
    def talk(self):
        print('it is just dark matter here')

class normalobject(special_object):
    def __init__(self):
        self.pickstatus=True
        self.enter=True
        
    def use(self,user):
        pass


class bag(normalobject):

    def __str__(self):
        return 'bag'
    def activate(self,user):
        user.bag=True
        user.bagstatus()
    def use(self,user):
        print('I always want a bag')
    def talk(self):
        print('bag give u more space, pick bag')
    def pickup(self):
        print('now you have extra 3 spaces')
    def drop(self):
        print('...')
        
        
        
        
class flashlight(normalobject):

    
    def __str__(self):
        return 'flash-light'
    def activate(self,user):
        user.flash_light=True
    def deactivate(self,user):
        user.flash_light=False
    def use(self,user):
        # falshlight able to show you what in 8 pieces around you 
        # change the check location formula print 
        pass
    def talk(self):
        print('hi there, I am a flash-light, you can see more with me')

        print('let me show you the way')
    def drop(self):
        print('I wish I can do more...')
    
    
    def pick(self):
        print('you can now see 8 block around you')
        print('000')
        print('010')
        print('000')
    def FLstatus(self):
        #update status of the flash_light 
        str_stuff=[str(i) for i in self.stuff]
        if 'flash-light' in str_stuff:  
            self.flash_light=True
            
        else:
            self.flash_light=False
            
            




class axe(normalobject):
    def __str__(self):
        return 'axe'
    def pick(self):
        print('big axe definitely attract women')
    def talk(self):
        print('yo. Axe here. Pick me up')
    def drop(self):
        print('you dare to drop Axe')
    def use(self,tree):
        if str(tree)=='tree':
            tree.enter=True
            print('Tree is down. No one canstop Axe')
        elif str(tree)=='empty':
            print('Axe dont want to cut you')
        else:
            print('good swing, but nothing happen')
class hammer(normalobject):
    def __str__(self):
        return 'hammer'
    def pick(self):
        print('Hammer smash')
    def talk(self):
        print('Hammer can help you with breaking')
    def drop(self):
        print('Hammer will miss you')
    def use(self,wall):
        if str(wall)=='breakwall':
            wall.enter=True
            print('I ve done my jobs')
        elif str(wall)=='empty':
            print('watch out')
        else:
            print('good swing, but nothing happen')

class shovel(normalobject):
    def __str__(self):
        return 'shovel'
    def pick(self):
        print('dig dig dig')
    def talk(self):
        print('shovel on the floor')
    def drop(self):
        print('no dig :(')
    def use(self,user):
        if str(user.Map.mapdict[user.location])=='breakfloor':

            if user.location==(9,9):
                user.Map.replace_obj(user.location,redscroll())
                print('something weird with this floor')
                print('you dig dig dig for a while')
                print('so many mud')
                print('but finally some thing show up')
                print('you find a red scroll')
                print('you are struglling to see in the dark and mud\nbut still manage to see it with flash-light')
                print('it said: ')
                print('1027')
                print('3722')
                print('1566')
                print('?')
                print('49')
                print('87')
                print('32')
                print('76')
                print('21')
                print('Goodluck!')
            elif user.location==(10,17):
                user.Map.replace_obj(user.location,goldscroll())
                print('As the floor break you start to dig dig dig')
                print('it takes a while but finally your work paid off')
                print('you find the gold-scroll')
            else:
                user.Map.replace_obj(user.location,crown())
                print('it takes a while but finally your work paid off')
                print('you find the a crown')

        else:
            print('so hard, cant use digg')

class bluescroll(normalobject):
    
    def __str__(self):
        return 'blue-scroll'
    def pick(self):
        print('a scroll always contain some secret')
    def talk(self):
        print('Blue-scroll')
    def drop(self):
        print('waste of time')
    def use(self,user):
        
            print('you strech the scroll and look inside')

            print('it said: ')
            print('10')
            print('26')
            print('50')
            print('82')
            print('122')
            print('170')
            print('226')
            print('?')
            print('362')
class redscroll(normalobject):
    
    def __str__(self):
        return 'red-scroll'
    def pick(self):
        print('a scroll always contain some secret')
    def talk(self):
        print('RED-scroll')
    def drop(self):
        print('waste of time')
    def use(self,user):
        
            print('you strech the scroll, everything is in red ')

            print('it said: ')
            print('1027')
            print('3722')
            print('1566')
            print('?')
            print('49')
            print('87')
            print('32')
            print('76')
            print('21')
            print('Ruby Ruby on the wall please show me the way') 

class oldscroll(normalobject):
    
    def __str__(self):
        return 'old-scroll'
    def pick(self):
        print('a scroll always contain some secret')
    def talk(self):
        print('old-scroll')
    def drop(self):
        print('waste of time')
    def use(self,user):
        
            print('the scroll look really old with full of Greek letter')
            print('you somehow have taken Greek, so manage to read couple lines')
            print('it said: ')
            print('100506')
            print('100529')
            print('100596')
            print('100706')
            print('100872')
            print('101099')
            print('101376')
            print('?')
            print('102124')
            print('the scroll will show you the place not the key')
            print('You also knew that ancient Greek were passionate with prime number')

class goldscroll(normalobject):
    
    def __str__(self):
        return 'χρυσός-scroll'
    def pick(self):
        print('a scroll always contain some secret')
    def talk(self):
        print('χρυσός-scroll')
    def drop(self):
        print('waste of time')
    def use(self,user):
        
            print('the scroll is made out of pure gold, cover in ancient Roman letter  ')
            print('you are out of luck this time, you are only understand Roman numbers')
            print('it said: ')
            print('XI')
            print('CXXXVIII')
            print('LV')
            print('CXLV')
            print('CCCLXXXV')
            print('CLIV')
            print('?')
            print('?')
            print('__')
            print('LVLV')

class SOSbottle(normalobject):
    
    def __str__(self):
        return 'SOS-bottle'
    def pick(self):
        print('nice bottle, now I can carry some water now')
        print('but why it is so blurry')
    def talk(self):
        print('SOS-bottle')
    def drop(self):
        print('too heavy')
    def use(self,user):
        if str(user.Map.get_object(user.location))=='mirror':
            
            print('unbuttoned the bottle, you find a piece of paper')
            print('the paper was written in weird language, you turn it in many directions but still not understand ')
            print('suddenly, you look into the mirror, and see that it was reflected language. ')
            print('in the mirror it shows: ')
            print('380')
            print('532')
            print('836')
            print('988')
            print('?')
            print('1444')
            print('1748')
        else:
            print('there is a piece of paper inside')
            print('I wonder what it said')
            print('ancient language??')



class calculator(normalobject):

    def __str__(self):
        return 'calculator'
    def pick(self):
        print('Calculator help you look smarter')
    def talk(self):
        print('Calculator on the floor')
    def drop(self):
        print('alright, you look less cool now')
    def use(self,user):
        print('I always enjoy the time with my claculator, so manys thing to do')
    
    
class crown(normalobject):
    
    def __str__(self):
        return 'crown'
    def pick(self):
        print('I look like a king now')
    def talk(self):
        print('is that a crown?')
        print('So tiny')
    def use(self,user):
        
        user.gameover()
        print('fit perfectly')
class picture(normalobject):
    
    def __str__(self):
        return 'picture'
    def use(self,user):
        print('it is a nice picture. I will bring it back to decorate my room')
    def pick(self):
        print('you tear down a picture')
        print('And there is a piece of paper underneath')
        print('you find the array of number and a tape')
        print('in the tape it said: the password is the missing number from array: ')
        print('134')
        print('137')
        print('146')
        print('173')
        print('254')
        print('497')
        print('1226')
        print('?')
        print('9974')
        print('Goodluck!')
    def talk(self):
        print('there is cool picture on the wall')
class goldkey(normalobject):
    def __str__(self):
        return 'GOLD-key'
    def pick(self):
        print('Made by pure gold')
    def talk(self):
        print('Gold-key on the floor')
        print('I can break any locks now')
    def drop(self):
        print('I can be sell ')
    def use(self,chest,user):
        if str(chest)=='GOLD-chest':
            chest.unbox(user)
            print('the chest is unlock')
        elif str(chest)=='empty':
            print('I wonder if there is a hidden door around here')
        else:
            print('cannot')
    
class redlaser(normalobject):
    def __str__(self):
        return 'red-laser'
    def pick(self):
        print('I wonder what it can do')
    def talk(self):
        print('R-E-D LASER')
    def drop(self):
        print('that is really cool laser')
        

    def use(self,user):
        
        ######### not write
        if user.location==(9,6):
            print('when u flash the red-laser onto Ruby ')
            print('the Ruby shaking and wake up')
            print('from the script u have read u said: ')
            print('Ruby Ruby on the wall please show me the way')
            print('then Ruby points to laser light to the location (9,9) ')
            bf=breakfloor()
            user.Map.replace_obj((9,9),bf)
        
        else:
            print('wooo red light is cool')

        
class panties(normalobject)  :

    def __str__(self):
        return 'Panties'
    def pick(self):
        print('It wont hurt to carry around a spare pair.')
    def talk(self):
        print('my first panties')
        print('So tiny')
    def use(self,user):
        
        # user.gameover()
        print('cant use. its so tiny')
        
        
class rubik(normalobject)  :

    def __str__(self):
        return 'rubik'
    def pick(self):
        print('I will solve it.')
    def talk(self):
        print('wow, it is 6x6 rubiks')
    def use(self,user):
        
        
        print('it is a good time to put brain on work')
        print('...')
        print('...')
        print('...')
        print('so hard, cant solve')
        pass
class bacon(normalobject)  :

    def __str__(self):
        return 'bacon'
    def pick(self):
        print('baconnnnn!')
    def talk(self):
        print('Oh my god, its bacon!')
        
    def use(self,user):
        
        
        print('so good, i m dreaming')
class hint(normalobject)  :
    def __init__(self):
        self.pickstatus=True
        self.enter=True
        self.n=2
    def __str__(self):
        return 'hint'
    def pick(self):
        print('boreddd')
    def talk(self):
        print('Hint can be used when encounter with boss')
    def use(self,user):
        r5=user.Map.room_list[4].room[:]
        r6=user.Map.room_list[5].room[:]
        r7=user.Map.room_list[6].room[:]
        
        
        if user.location in r5:
            #r5 cerberus
            self.n-=1
            print('dog love bacon. It would be nice if you carry some in bag')
            if self.n==0:
                user.stuff.remove(user.onhand)
                user.onhand=empty()
        elif user.location in r6:
            #r6 minotaur
            print('Calculator is really good for a math test. Find it')
            self.n-=1
            if self.n==0:
                user.stuff.remove(user.onhand)
                user.onhand=empty()
        elif user.location in r7:
            #r7 hydra
            print('to decrypte the message, you need to have the private key, find it first ')
            print('also, understanding of prime number would be useful ')
            self.n-=1
            if self.n==0:
                user.stuff.remove(user.onhand)
                user.onhand=empty()
            #print('the message is a text')
        else:
            print('Hint is for some thing hard. so bad')


class piece_of_paper(normalobject):
    def __str__(self):
        return 'paper'
    def pick(self):
        print('there is some word in here!')
    def talk(self):
        print('Piece of paper on the ground ?!')
        print()
        
    def use(self,user):
        
        print('something is written in here')
        print('Private key: ')
        print('22801763489')
        print('what does this number mean?')
        
        
###################
class block_object(special_object):
    def __init__(self):
        self.pickstatus=False
        self.enter=False
    def unlock(self):
        pass
    # def Type(self):
    #     return 'block_object'
    def pick(self):
        print('cannot pick')
    def talk(self):
        pass
##############
class door(block_object):
        
    def __init__(self,password):
        block_object.__init__(self)
        self.password=password
    def __str__(self):
        return 'door'

        
    def talk(self):
        if self.enter:
            print('the door is open')
        else:
            pw=input('the door is locked. please input password: ')
            self.unlock(pw)
    def unlock(self,Input):
        if Input==self.password:
            self.enter=True
            print('Correct, the door is unlocked')
        else:
            print('wrong password.')

############
class door1(door):
    def __init__(self,password):
        self.pickstatus=False
        self.enter=True
    def talk(self):
        print('the door is open')
        print('welcome to room 1')

class door2(door):
    def __init__(self,password):
        self.pickstatus=False
        self.enter=False
    def talk(self):
            print('the door is open')
            print('welcome to room 2')

class door3(door):
    def __init__(self,password):
        self.pickstatus=False
        self.enter=False
    def talk(self):
            print('the door is open')
            print('welcome to room 3')

class door4(door):
    def __init__(self,password):
        self.pickstatus=False
        self.enter=False
    def talk(self):
            print('the door is open')
            print('welcome to room 4')

class door5(door):
    def __init__(self,password):
        self.pickstatus=False
        self.enter=False
    def talk(self):
            print('the door is open')
            print('welcome to Cerberus room ')

class door6(door):
    def __init__(self,password):
        self.pickstatus=False
        self.enter=False
    def talk(self):
            print('the door is open')
            print('welcome to Minotaur room ')

class door7(door):
    def __init__(self,password):
        self.pickstatus=False
        self.enter=False
    def talk(self):
            print('the door is open')
            print('welcome to Hydra room ')    
    





class ruby(block_object):
        
    def __init__(self):
        self.pickstatus=False
        self.enter=True
    def __str__(self):
        return 'red-ruby'
    def talk(self):
       
        print('R-E-D Ruby on the wall')

class mirror(block_object):
        
    def __init__(self):
        self.pickstatus=False
        self.enter=True
    def __str__(self):
        return 'mirror'
    def talk(self):
       
        print('why there is a mirror in here?!')
        print('so dirty')

class breakfloor(block_object):
    def __init__(self):
        self.pickstatus=False
        self.enter=True
    def __str__(self):
        return 'breakfloor'
    # def talk(self):
       
    #     print('something weird with this floor')
            
            
class tree(block_object):
    def __str__(self):
        return 'tree'
    def talk(self):
        if self.enter:
            print('the tree is down')
        else:
            print('cant pass, tree in the way. learn to respect tree first')
    def unlock(self):
        self.enter=True




class goldchest(block_object):
    def __init__(self):
        block_object.__init__(self)
        # self.status=False
        self.obj=redlaser()
    def __str__(self):
        return 'GOLD-chest'
    def pick(self):
        print('too heavy cannot carry')
    def talk (self)  :
        print('there is a shiny light in the middle of darkness')
        print('you cover your eyes to see clearer')
        print('in front of you is the gold chest')
        print('it has to have treasure in it. u think')
    def unbox(self,user):
        # self.status=True
        
        print('there is something in the chest')
        user.Map.replace_obj(user.location,self.obj)
        self.obj.talk()
class breakwall(block_object):
    def __str__(self):
        return 'breakwall'
    def talk(self):
        if self.enter:
            print('Amazing, there is path over here')
        else:
            print('there are cracks on the walls')
    def unlock(self):
        self.enter=True    
        







####################
class boss(block_object):        
    def __init__(self,riddle):
        self.pickstatus=False
        self.enter=False
        self.riddle=riddle

    def Type(self):
        return 'boss'
    def pick(self):
        print('cannot pick')
    def talk(self):
        pass



class Minotaur(boss):
    def __str__(self):
        return 'Minotaur'
    def etalk(self):
        print('your Axe move is so good')        
    def talk(self,user):
        self.riddle.talk(user)
        self.riddle.play(user,self)
class Hydra(boss):
    def __str__(self):
        return 'Hydra'
    def etalk(self):
        print('You are so smart I lose')  
        print('***contact me for present if you see this***')
    def talk(self,user):
        self.riddle.talk(user)
        self.riddle.play(user,self)
class Cerberus(boss):
    def __str__(self):
        return 'Cerberus'
    def etalk(self):
        print('no one better than Cerberus at math, why??')  
    def talk(self,user):
        self.riddle.talk(user)
        self.riddle.play(user,self)
        
########################
class riddle(object):
    pass 

class countriddle(riddle):
    def __init__(self):
        self.player1=False
        self.player2=False
        
        
    def talk(self,user):

            
            
        print(user.name+ ', this room is control by the mighty Minotaur')
        print('his hammer is way bigger than your and can crush you in a first swing')
        print('fortunately, you are able to kill him if you get to swing your big Axe first')
        print('you and him are 21 steps away')
        
        print('the rule is: ')
        print('you and Minotaur will take turn to move, and whoever reachs 21st first will be striked first and lose ')
        print('everyturn individual has to move at least 1 and no more than 3 steps')
        print('for example:\nyou go 2 and Minotaur go 3, it will show:\n1 2\n3 4 5')
    def lose(self):
        print('you got defeated ' )
    def play(self,user,boss):
        str_stuff=[str(i) for i in user.stuff]
        self.player1=True
        n1=0
        # player 1 : user
        # player 2 : boss
        self.player2=True
        n2=0
        
        
        print('game on')
        if 'calculator' in str_stuff:
            
            while True:
                move=int(input('to move first press 1 else press 2: '))
                if move !=1 and move!=2:
                    print('please input again')
                else: 
                    break
            
            if move==2:
                while True:
                    if n1%4==0:
                        bm=random.randint(1, 3)
                    else:
                        bm=4-n1%4
                    print('Minotaur go: ',bm)
                    n2+=bm
                    
                    print(str([i for i in range(n1+1,n2+1)]))
                    if n2>=21:
                        break
                    n1+=bm
                    
                    
                    
                    while True:
                        try:
                            um=int(input(str(user)+' go: '))
                        except(ValueError):
                            print('please input number')
                            continue                         
                        if um >=1 and um<=3:
                            break
                        else: 
                            print('cant execute, please follow the rule')
                    n1+=um
                    print(str([i for i in range(n2+1,n1+1)]))
                    if n1>=21:
                        break
                    n2=n1
                if n1>=21:
                    self.player1= False
                    self.lose()
                    print('try again later')
                    return
                else:
                    self.player2 = False
                    print('Minotaur got defeated')
                    boss.enter=True
                    print('congratulation! you are now able to pass')
                    return
                
        while True:
            while True:
                        try:
                            um=int(input(str(user)+' go: '))
                        except(ValueError):
                            print('please input number')
                            continue                        
                        if um >=1 and um<=3:
                            break
                        else: 
                            print('cant execute, please follow the rule')
            n1+=um
            print(str([i for i in range(n2+1,n1+1)]))
            if n1>=21:
                break
            n2=n1
            if n1%4==0:
                bm=random.randint(1, 3)
            else:
                bm=4-n1%4
            print('Minotaur go: ',bm)
            n2+=bm
            
            print(str([i for i in range(n1+1,n2+1)]))
            if n2>=21:
                break
            n1+=bm
                    
                    
                    
        
        self.player1= False
        self.lose()
        print('try again later')
        return

class alanriddle(riddle):
    def __init__(self):
        self.password='victory'
        self.enter=False
    def talk(self,user):
        print(user.name+ ', this room is control by the 9-heads robot Hydra')
        print('everytime u cut its head two more will grow')
        print('u keep fighting until exhasuted and get squeezed by the Hydra, the only way to win is to turn it off before it tear u into pieces ')
        print('when enter the room you notice there is the number written all over the walls')
        print('__________________________')

        print('')
        print('50369825549820718594667857')
        print('__________________________')

        print('you have taken some decryted courses before so you try to use your final luck')
        print('you have 3 chances to shout out the answer before Hydra kill you ')
    
    def play(self,user,boss):
        trial=0
        while trial<3:
            trial+=1
            pw=input('you shout: ')
            if pw.lower()==self.password:
                print('...')
                print('you scream out loud "Victory", and Hydra immediately stop moving and squeezing')
                print('everything collasps before your eyes')
                print('you breath heavily and said')
                print('that was the close on')
                print('Finally I defeat them all')
                print('Congratulation!!!')
                boss.enter=True

                break
            elif trial==2:
                print('"',pw,'"')
                print('Hydra squeezing tighter, cant even breath')
            elif trial==1:
                print('"',pw,'"')
                print('Hydra show sight that it doesnt care')
            elif trial==3:
                print('Last chance: ','"',pw,'"')
                print('Hydra tired and bite off your head')
                print('try again later')

class divideriddle(riddle):
    def __init__(self):
        self.player1=False
        self.player2=False
        
        
    def talk(self,user):
        print(user.name+ ', this room is protected by the mighty 3-heads Cerberus - the hound of Hades')
        print('the hound is sleeping in front of the door you want to pass through. ')
        print('if it catchs you, there is no way no can escape its deadly bite')
        print('fortunately, you can trick it to play your game and if you will Cerberus will let you go')
        print('you and him have to build a 10-digit number that divisible by 15')
        
        print('everyturn individual has to write 1 digit down')
        print('for example:\nyou choose 2 and Cerberus choose 9, it will show:\n29')
        
    def lose(self):
        print('you got defeated ' )
    def play(self,user,boss):
        str_stuff=[str(i) for i in user.stuff]
        self.player1=True
        # player 1 : user
        # player 2 : boss
        self.player2=True
        fn=''

        cn=0
        
        
        print('game on')
        if 'bacon' in str_stuff:
            
            while True:
                print('you still have some extra bacon  in the bag')
                print('you give the whole thing for Cerberus in exchange for the right choose who will make the first move')
                move=int(input('to move first press 1 else press 2: '))
                if move !=1 and move!=2:
                    print('please input again')
                else: 
                    break
            
            if move==1:
                while True:
                    if len(fn)==0:
                        while True:
                            try:
                                um=int(input(str(user)+' choose: '))
                            except(ValueError):
                                print('please input number')
                                continue                        
                            if um >=1 and um<=9:
                                break
                            else: 
                                print('cant execute')
                        fn=fn+str(um)
                        cn+=um
                        print('num: ',fn)
                    else:
                        while True:
                            try:
                                um=int(input(str(user)+' choose: '))
                            except(ValueError):
                                print('please input number')
                                continue                        
                            if um >=0 and um<=9:
                                break
                            else: 
                                print('cant execute')
                        fn=fn+str(um)
                        cn+=um
                        print('num: ',fn)                    
                        if len(fn)==9:
                            break
                    
                    
                    bm=random.randint(0, 9)
                    
                    print('Cerberus choose: ',bm)
                    fn=fn+str(bm)
                    cn+=bm
                    
                    print('num: ',fn)
                    
                if cn%3==0:
                    bm=0
                    print('Cerberus choose: ',bm)
                    fn=fn+str(bm)
                    print('num: ',fn,' is devisable for 15')
                    print('Cerberus chases you out of the room')
                    print('try again later')
                elif cn%3==1:
                    bm=5
                    print('Cerberus choose: ',bm)
                    fn=fn+str(bm)
                    print('num: ',fn,' is devisable for 15')
                    print('Cerberus chases you out of the room')
                    print('try again later')
                else:
                    bm=random.randint(0, 9)
                    
                    print('Cerberus choose: ',bm)
                    fn=fn+str(bm)
                    cn+=bm
                    
                    print('num: ',fn,' is cannot devide for 15')
                    print('Cerberus look at the number again and again to find out what he did wrong')
                    print('And you just take your time the cross the door')
                    boss.enter=True
                    return

                
        while len(fn)<10:
         
            
            if len(fn)<8:
            
            
                bm=random.randint(0, 9)
                
                print('Cerberus choose: ',bm)
                fn=fn+str(bm)
                cn+=bm
                
                print('num: ',fn)
            elif cn%3==0:
                bm=random.choice([2,5,8])
                
                print('Cerberus choose: ',bm)
                fn=fn+str(bm)
                cn+=bm
                
                print('num: ',fn)
            elif cn%3==1:
                bm=random.choice([1,4,7])
                
                print('Cerberus choose: ',bm)
                fn=fn+str(bm)
                cn+=bm
                
                print('num: ',fn)
            elif cn%3==2:
                bm=random.choice([3,6,9,0])
                
                print('Cerberus choose: ',bm)
                fn=fn+str(bm)
                cn+=bm
                
                print('num: ',fn)                    
            while True:
                try:
                    um=int(input(str(user)+' choose: '))
                except(ValueError):
                    print('please input number')
                    continue
                if um >=0 and um<=9:
                    break
                else: 
                    print('cant execute')
            fn=fn+str(um)
            cn+=um
            print('you choose: ',um)
            print('num: ',fn)        
                    
        
        self.player1= False
        print('num: ',fn,' is cannot devide for 15')

        print('Cerberus chases you away')
        print('try again later')
        return

            
                
######################        
        
        

def build_roomlist():
    
    r1=room(5,5,(0,0))
    r2=room(5,5,(0,8))
    r3=room(5,5,(8,6))
    r4=room(5,5,(8,17))
    
    r1.setup_room()
    r2.setup_room()
    r3.setup_room()
    r4.setup_room()
    
    r1.setup_dict()
    r2.setup_dict()
    r3.setup_dict()
    r4.setup_dict()
    
    r5=room(3,3,(9,24))
    r6=room(3,3,(15,19))
    r7=room(3,3,(15,24))
    
    r5.setup_room()
    r6.setup_room()
    r7.setup_room()
    
    r5.setup_dict()
    r6.setup_dict()
    r7.setup_dict()
    return [r1,r2,r3,r4,r5,r6,r7]



def build_roadlist():
    
    
    r1=road(1,3,(2,5))
    r2=road(1,4,(2,13))
    r3=road(15,1,(3,14))
    r4=road(3,1,(5,10))
    r5=road(1,6,(11,11))
    
    r6=road(1,9,(6,0))
    r7=road(1,15,(17,0))
    r8=road(4,1,(13,2))
    r9=road(5,1,(6,0))
    r10=road(9,1,(6,4))
    r11=road(1,2,(8,11))
    r12=road(1,10,(15,4))
    r13=road(1,4,(3,-3))
    
    r14=road(1,2,(10,22))
    r15=road(1,2,(16,22))
    r16=road(1,3,(16,27))
    r17=road(2,1,(13,20))
    r18=road(3,1,(12,25))
    r19=road(4,1,(16,29))
    
    r1.setup_room()
    r2.setup_room()
    r3.setup_room()
    r4.setup_room()
    r5.setup_room()
    r6.setup_room()
    r7.setup_room()
    r8.setup_room()
    r9.setup_room()
    r10.setup_room()
    r11.setup_room()
    r12.setup_room()
    r13.setup_room()
    r14.setup_room()
    r15.setup_room()
    r16.setup_room()
    r17.setup_room()
    r18.setup_room()
    r19.setup_room()
    
    r1.setup_dict()
    r2.setup_dict()
    r3.setup_dict()
    r4.setup_dict()
    r5.setup_dict()
    r6.setup_dict()
    r7.setup_dict()
    r8.setup_dict()
    r9.setup_dict()
    r10.setup_dict()
    r11.setup_dict()
    r12.setup_dict()
    r13.setup_dict()
    r14.setup_dict()
    r15.setup_dict()
    r16.setup_dict()
    r17.setup_dict()
    r18.setup_dict()
    r19.setup_dict()

    return [r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19]






def build_gamemap(list_room,list_road,special_location=[]):

    gamemap= Map(list_room,list_road,special_location)
    
    gamemap.build_map()
    gamemap.update_map()
    

    return gamemap


##################################
def  setup_doors():
    # block object first other later
    d1=door1('9999')
    d2=door('3413')
    d3=door2('9999')
    d4=door3('9999')
    d5=door('1292')
    d6=door('290')
    d7=door('4261')
    d8=door4('9999')
    
    d9=door('IVCCXXXV')
    d10=door('CLXV')
    d11=door6('9999')
    d12=door5('9999')
    
    d13=door('9999')
    d14=door('9999')
    d15=door7('9999')
    d16=door7('9999')

    
    
    
    d1.enter=True
    d3.enter=True
    d8.enter=True
    d4.enter=True
    d11.enter=True
    d12.enter=True
    
    d13.enter=True
    d14.enter=True
    d15.enter=True
    d16.enter=True
    
    
    d1_l=location(3,0,d1)
    d2_l=location(2,5,d2)
    d3_l=location(2,8,d3)
    d4_l=location(8,10,d4)
    d5_l=location(5,10,d5)
    d6_l=location(8,11,d6)
    d7_l=location(11,11,d7)
    d8_l=location(11,17,d8)
    d9_l=location(10,22,d9)
    d10_l=location(13,20,d10)
    d11_l=location(15,20,d11)
    d12_l=location(10,24,d12)
    d13_l=location(12,25,d13)
    d14_l=location(16,22,d14)
    d15_l=location(16,24,d15)
    d16_l=location(15,25,d16)
        
    
    
    
    d=[d1_l,d2_l,d3_l,d4_l,d5_l,d6_l,d7_l,d8_l,d9_l,d10_l,d11_l,d12_l,d13_l,d14_l,d15_l,d16_l]
    
    
    w1=breakwall()
    w2=breakwall()
    w3=breakwall()
    
    
    
    w1_l=location(3,14,w1)
    w2_l=location(15,13,w2)
    w3_l=location(16,2,w3)
    
    w=[w1_l,w2_l,w3_l]
    
    t1=tree()
    t2=tree()
    t3=tree()
    t4=tree()
    bf1=breakfloor()
    
    t1_l=location(9,14,t1)
    t2_l=location(13,14,t2)
    t3_l=location(2,13,t3)
    t4_l=location(14,2,t4)
    bf1_l=location(13,2,bf1)
    t=[t1_l,t2_l,t3_l,t4_l,bf1_l]
    
    return d+w+t
    
    

####################################
def draw_map():
    list_room=build_roomlist()
    list_road=build_roadlist()
    gm=build_gamemap(list_room,list_road,special_location=[])
    
    m=np.zeros((33,24),dtype=int)
    
    for (x,y) in gm.mapdict:
        m[y][x]=1
    print(m)
    return m







###############

# list_room=build_roomlist()
# list_road=build_roadlist()
# Map_1=build_gamemap(list_room,list_road)


def setupr1(Map_1):
    r1=Map_1.room_list[0].room[:]
    r1.remove((4,3))
    
    pic=picture()
    
    h=hammer()
    f=flashlight()

    b=bag()
    
    x1,y1=random.choice(r1)
    r1.remove((x1,y1))
    x2,y2=random.choice(r1)
    r1.remove((x2,y2))
    x3,y3=random.choice(r1)
    r1.remove((x3,y3))
    # x4,y4=random.choice(r1)
    
    
    pic_l=location(4,3,pic)

    h_l=location(x1,y1,h)
    f_l=location(x2,y2,f)
    b_l=location(x3,y3,b)
    
    
    return [pic_l,h_l,f_l,b_l]

def setupr2(Map_1):
    r2=Map_1.room_list[1].room[:]
    r2.remove((2,8))
    r2.remove((0,8))
    
    sh=shovel()
    g=goldkey()
    sb=SOSbottle()
    r=rubik()
    m=mirror()
    
    m_l=location(0,12,m)
    
    
    x1,y1=random.choice(r2)
    r2.remove((x1,y1))
    x2,y2=random.choice(r2)
    r2.remove((x2,y2))
    x3,y3=random.choice(r2)
    r2.remove((x3,y3))
    x4,y4=random.choice(r2)
    
    
    sh_l=location(x1,y1,sh)
    g_l=location(x2,y2,g)
    sb_l=location(x3,y3,sb)
    r_l=location(x4,y4,r)
    
    
    return [sh_l,g_l,sb_l,r_l,m_l]

def setupr3(Map_1):
    r3=Map_1.room_list[2].room[:]
    r3.remove((9,9))
    r3.remove((9,6))
    
    ru=ruby()
    ru_l=location(9,6,ru)
    c=calculator()
    gc=goldchest()
    gc_l=location(2,16,gc)
    
    bw=breakwall()
    bw_l=location(3,14,bw)
    
    bs=bluescroll()
    
    
    
    A=axe()
    
    
    
    b=bacon()
    
    
    
    
    x1,y1=random.choice(r3)
    r3.remove((x1,y1))
    x2,y2=random.choice(r3)
    r3.remove((x2,y2))
    x3,y3=random.choice(r3)
    # x4,y4=random.choice(r3)
    
    c_l=location(8, 12, c)
    bs_l=location(x1,y1,bs)
    A_l=location(x2,y2,A)
    b_l=location(x3,y3,b)
    # p_l=location(x4,y4,p)
    
    
    return [ru_l,gc_l,bw_l,bs_l,A_l,b_l,c_l]

def setupr4(Map_1):
    r4=Map_1.room_list[3].room[:]
    r4.remove((11,17))
    
    h=hint()
    p=panties()
    os=oldscroll()
    pp=piece_of_paper()
    c=crown()
    

    
    
    
    x1,y1=random.choice(r4)
    r4.remove((x1,y1))
    x2,y2=random.choice(r4)
    r4.remove((x2,y2))
    x3,y3=random.choice(r4)
    r4.remove((x3,y3))
    x4,y4=random.choice(r4)
    
    
    h_l=location(x1,y1,h)
    p_l=location(x2,y2,p)
    os_l=location(x3,y3,os)
    pp_l=location(x4,y4,pp)
    c_l=location(18, 29, c)
    
    return [h_l,p_l,os_l,pp_l,c_l]



###################

def setup_boss():
    # h=User('h','e',Map_1)
    
    cr=countriddle()
    ar=alanriddle()
    dr=divideriddle()
    
    Min=Minotaur(cr)
    Hyd=Hydra(ar)
    Cer=Cerberus(dr)
    
    # Min.talk(h)
    # Hyd.talk(h)
    # Cer.talk(h)
    
    Min_l=location(16,21,Min)
    Hyd_l=location(16,26,Hyd)
    Cer_l=location(11,25,Cer)
    return[Min_l,Hyd_l,Cer_l]


###############
def construct():
    
    list_room=build_roomlist()
    list_road=build_roadlist()
    Map_1=build_gamemap(list_room,list_road)
    r2=setupr2(Map_1)

    r1=setupr1(Map_1)
    r3=setupr3(Map_1)
    r4=setupr4(Map_1)
    c=setup_doors()
    b=setup_boss()
    Map_1=build_gamemap(list_room,list_road,r3+r1+c+r2+r4+b)
    return Map_1
############
def instruction():
    print('these are what u can do: ')
    print('move up: up or w ')
    print('move down: down or s ')
    print('move left: left or a ')
    print('move right: right or d ')
    print('pick up: pick or j')
    print('drop: drop or k')
    print('use: use or u')
    print('open bag: open or o')
    print('close bag: close or c')
    print('choose stuff : (object name)   ' )
    print('talk: talk or t')
    print('check location: location or l')
    print('save: save or y')
############    
def checkandexecute(user,command):    
    if command in user.list_command():
        com=user.list_command()[command]
        if com=='move up':
            user.move_up()
        elif com=='move down':
            user.move_down()
        elif com=='move left':
            user.move_left()
        elif com=='move right':
            user.move_right()
        elif com=='pick up':
            user.pickup()
        # elif com=='choose' :
        #     bf=user.onhand
        #     for i in user.stuff:
                
        #         if str(i)==command:
        #             user.choose(i)
        #     if str(bf)==str(user.onhand):
        #         if str(user.onhand)=='empty':
        #             print('there is no such thing')
        #         else:
        #             print('you already holind it')
            
        elif com=='drop':
            
            user.drop()
        elif com=='use':
            user.use()
        elif com=='open':
            user.openbag()
            obj=input('pick something: ')
            if obj=='c' or obj == 'close':
                pass
            else:
                bf=user.onhand
                str_stuff=[str(i) for i in user.stuff]
                if obj in str_stuff:
                    if str(bf)==obj:
                        print('you are holding it')
                    else:
                        for i in user.stuff:
                    
                            if str(i)==obj:
                                user.choose(i)
                else:
                    print('there is no such things')
        
        elif com=='close':
            print('there is nothing to close ... ')        
                
        elif com=='talk':
            user.talk()
        elif com=='location':
            if user.flash_light:
                (x,y)=user.get_location()
                loc=[(x,y+1),(x,y-1),(x+1,y),(x-1,y),(x-1,y+1),(x-1,y-1),(x+1,y+1),(x+1,y-1)]
                for (i,j) in loc:
                    
                    if user.Map.check_location((i,j)) and str(user.Map.mapdict[(i,j)])!='empty' :
                        print(user.Map.print_location((i,j)))
                print('you are at '+ str(user.get_location()))
            else:
                print('you are at '+ str(user.get_location()))
        elif com=='save':
            user.save(slist)

    else:
        print('what you say again')
        
def Gaming_with_Huy():
    Map=construct()
    if slist:
        print('new game: press n')
        print('continue: press c')
        a=input()
        if a=='n':
            name=str(input('please input name: '))
            age=input('please input age: ')
            user=User(name,age,Map)
            user.startgame()
            print('Hello, '+name+' . Are you ready to test your mind?')
            print('there are rooms and quizes await for you to prove yourself a genius. you are able to control the character by using these inputs.') 
            instruction()
            print('good luck and dont stop until you solve it all')
            while user.gamestatus:
                command=input('please input your command: ')
                checkandexecute(user,command)
            
        
            print('you won')
        else:
            
            for i in slist:
                print(i)
            player= input('please choose: ')
            for i in slist:
                if str(i)==player:
                    i.startgame()
                    instruction()
                    while user.gamestatus:
                        command=input('please input your command: ')
                        checkandexecute(user,command)
                    print('you won')

            
            
    else:
    
        name=str(input('please input name: '))
        age=input('please input age: ')
        user=User(name,age,Map)
        user.startgame()
        print('Hello, '+name+' . Are you ready to test your mind?')
        print('there are rooms and quizes await for you to prove yourself a genius. you are able to control the character by using these inputs.') 
        instruction()
        print('good luck and dont stop until you solve it all')
        while user.gamestatus:
            command=input('please input your command: ')
            checkandexecute(user,command)
        
    
        print('you won')
    
    
    
    
    
    
    
    
    
    
    

Gaming_with_Huy()
    
      