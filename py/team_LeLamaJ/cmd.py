import time
import math
import Get_inputs 

def sign(x):
    return float(x>0.0) - float(x<0.0)

def cr_mad():
    myMad = mad_p.mad()
    myMad.motor(50,-50)
    return (myMad)

def setHeadingSimple (head):
    myMad = cr_mad()    
    time.sleep(2)
    errMax=10
    headOk=False

    while headOk != True:        
        headMes=myMad.getAngles()[0]
        headErr=headMes-head
        
        if abs(headErr)<errMax:
            headOk=True
            myMad.motor(0,0)
	    #myMad.motor(1,1)
            #myMad.ns.isAlive=False
            

        else:
            time.sleep(0.1)
                                             
def setHeading(head):
    myMad = cr_mad()
    headOk=False    
    errMax=10
    
    while headOk != True:        
        headMes=myMad.getAngles()[0]
        headErr=headMes-head
        
        if headErr > 180:
            headErr=headErr -180
            time.sleep(0.1)
            
        if headErr< -180:
            headErr=headErr +180
            time.sleep(0.1)
            
        if headErr >= 0:
            myMad.motor(-50,50)
            
        else:
            myMad.motor(50,-50)
            
        if abs(headErr)< errMax:
            headOk=True
            myMad.motor(0,0)
	    #myMad.motor(1,1)
            #myMad.ns.isAlive=False


        else :
            
             time.sleep(0.1)
                          
                         
def setHeadingProp(head,alpha):
    myMad = cr_mad()
    headOk=False    
    errMax=10
    
    while headOk != True:
        headMes=myMad.getAngles()[0]
        headErr=headMes-head
        v=alpha*abs(headErr)
       
        if abs(headErr) > 180:
            headErr = headErr-180
            
        if headErr >= 0:
            myMad.motor(-50-v,50+v)
            
        else:
            myMad.motor(50+v,-50-v)
            
        if abs(headErr)< errMax:
            headOk=True
            myMad.motor(0,0)
	    #myMad.motor(1,1)
            #myMad.ns.isAlive=False

        else :
            
             time.sleep(0.1)
                 

                 
#def goLineHeading (head,speed,duration):
#    myMad = mad_p.mad()
#    v=head+speed
#    t=time.time()
#    while time.time()-t < duration:
#        myMad.motor(v,v)
#        time.sleep(0.1)
#    myMad.motor(1,1)
#    myMad.ns.isAlive=False
    
def goLineHeading (mad_p,head,speed,duration):
    
    myMad = mad_p  
    headOk=False
    errMax=10
    errMax=errMax*3.14/180.0
    print ('errMax')
    
    while headOk != True:
        
        headMes=myMad.getAngles()[0]
        headErr=headMes-head
        headErr=headErr*3.14/180.0
        
        if math.cos(headErr)>0:
            cmd=50*sign(math.sin(headErr))
            myMad.motor(cmd,-cmd)
            time.sleep(0.1)
        else:
            cmd=250*sign(math.sin(headErr))
            myMad.motor(cmd,-cmd)
            time.sleep(0.1)
              
        if abs(headErr)< errMax:
            print ('Cap OK')
            t=time.time()
            while time.time()-t < duration:
                myMad.motor(speed,speed)
                time.sleep(0.1)
                
            headOk=True
            myMad.motor(1,1)
            myMad.ns.isAlive=False

        else :
            
             time.sleep(0.1)
    
    
def goLineOdo (speed, duration):
    myMad = mad_p.mad()
    headOk=False
    errMax=10
    while headOk != True:
        
         headMes_left , headMes_right = myMad.encoder()
        
         dif=headMes_left-headMes_right
         if dif < 0:
            headMes_left=headMes_right
         if dif > 0:   
             headMes_right= headMes_left
            
         if dif ==0:
            
            t=time.time()
            while time.time()-t < duration:

                myMad.motor(speed,speed)
                print ('dif')
                time.sleep(0.1)
            headOk=True
            myMad.motor(1,1)
            myMad.ns.isAlive=False
        




def mini_son(mad_p):
    myMad = mad_p
    dis=myMad.getSonars()
    c=0
    d=dis[0]
    for i in range (0,len(dis)):
        if dis[i]<d and dis[i]!=-1:
            d,c=dis[i],i
    return c

    
    
    
#def obstcleAVoid(speed,coef):
#    myMad = mad_p.mad()
#    
#    myMad.motor(speed,speed)
#    head=headMes=myMad.getAngles()[0]
#    duration=30
#    goLineHeading (myMad,head,speed,duration)
#    
#    t=time.time()
#    
#    while time.time()-t < 30:
#        
#        time.sleep(0.1)
#        
#        dis= myMad.getSonars()
#        print ('dis')
#
#        dis_dev = dis[mini_son(myMad)]
#        
#        print ('dis_dev')
#        
#        
#        if mini_son(myMad)==0:
#            if dis_dev <=7:
#                time.sleep(1)
#                myMad.motor(speed+coef,speed)
#                time.sleep(0.1)
#        if mini_son(myMad)==1:
#            if dis_dev <=7:
#                time.sleep(1)
#                myMad.motor(speed+coef,speed)
#                time.sleep(0.1)
#        if mini_son(myMad)==2:
#            if dis_dev <=7:
#                time.sleep(1)                
#                myMad.motor(speed+coef,speed)
#                time.sleep(0.1)
#                
#        if mini_son(myMad)==3:
#            if dis_dev <=7:
#                time.sleep(1)
#                myMad.motor(speed+coef,speed)
#                time.sleep(0.1)
        
##        if dis_dev <=10:
##            myMad.motor(speed+coef,speed-coef)
##            time.sleep(3)
##           myMad.motor(speed,speed)





#def obstcleAVoid():
#    myMad = mad_p.mad()
#    a = myMad.getSonars()
#    print ('a')
##    right=a[4]
##    avant=a[3]
##    deriere=a[1]
##    left=a[2]
##    if right < left:
##        myMad.motor(0,0)
##        time.sleep(0.3)
##        myMad.motor(240,-240)
##        time.sleep(0.14)
##    elif left < right:
##        myMad.motor(0,0)
##        time.sleep(0.3)
##        myMad.motor(-240,240)
##        time.sleep(0.14)
##    else:
##        myMad.motor(0,0)
##        time.sleep(0.3)
##        myMad.motor(-240,240)
##        time.sleep(0.3)
#        





def obstcleAVoid2():
    
    
    myMad = mad_p.mad() 
    # test sonar
    myMad.motor(-60,-60)    
    for i in range(4):
        print ('i','myMad.getSonars()')
        time.sleep(0.25)

    # go forward until wall
    frontDist = myMad.getSonars()[2]
    print ('frontDist')
    while (frontDist == -1) or (frontDist > 40.0):
        frontDist = myMad.getSonars()[2]
        print ('frontDist')
        time.sleep(0.25)
    
    # put the robot to heading to East
    myMad.motor(45,-45)
    turnOn = True
    while turnOn:
        head = myMad.getAngles()[0]
        print ('head')
        if (head > 87) and (head < 93):
            turnOn=False
        else:
            time.sleep(0.5)

    myMad.motor(-100,-100)    
     # go forward until wall
    snrs = myMad.getSonars()
    frontDist = snrs[2]
    k=0.2
    while (frontDist == -1.0) or (frontDist > 40.0):
        snrs = myMad.getSonars()
        frontDist = snrs[2]
        rDist = snrs[1]
        print ('rDist')
        if rDist != -1.0:
            err = 30.0-rDist
            myMad.motor(-100+k*err,-100-k*err)
        time.sleep(0.25)
 
    myMad.motor(0,0)
    
    # wait 5 s before closing
    time.sleep(5.0)

    try:
        # end of simulation
        myMad.ns.isAlive=False
    
        # wait 1s to cleanly the end of simulation
        time.sleep(1)
    except:
        pass




    
    
def goCurveOdo (speedTan, radius, sign, duration):
    myMad = mad_p.mad()
    t=time.time()
#    myMad.motor(speedTan,speedTan)
    if abs(sign)==1:
        while time.time()-t < duration:
#             headMes_left , headMes_right = myMad.encoder()  
#             dif=headMes_left-headMes_right
             if sign>0:
                 myMad.motor(-sign*speedTan*radius,sign*speedTan)
             else:
                 myMad.motor(-sign*speedTan,sign*speedTan**radius)
        myMad.motor(1,1)
        myMad.ns.isAlive=False
    else: 
        while time.time()-t < duration:
            if sign >0:
                sign=1
                myMad.motor(-sign*speedTan*radius,sign*speedTan)
            else:
                sign=-1
                myMad.motor(-sign*speedTan,sign*speedTan**radius)
        myMad.motor(1,1)
        myMad.ns.isAlive=False
    
    
#mini_son()   
    
#goCurveOdo (60, 50, 1, 5)   
#obstcleAVoid2()
    
myMad = mad_p.mad()
#myMad.motor(50,50)
#
#while True:
#    dis = myMad.getSonars()
#    print ('dis')
#    time.sleep(1)
    
    

#goLineOdo (100, 8)

goLineHeading(myMad,-50,-100,7)


#goLineHeading (40,100,10)