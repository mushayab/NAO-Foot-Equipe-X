import os
import time
import math
import struct
import sys

def high_low_int(high_byte, low_byte):
    return (high_byte << 8) + low_byte

def high_byte(integer):
    return integer >> 8


def low_byte(integer):
    return integer & 0xFF

class mad():
    def __init__(self):

        self.motor_last_change = 0
        
        if os.access("/sys/devices/virtual/misc/gpio/mode/gpio0", os.F_OK) :
            print ("Real creation")

            # Import modules
            from drivers.trex import TrexIO
            from drivers.razor import RazorIO
            #from drivers.hcsr04 import SonarIO
            from drivers.sonar import SonarIO
            self.trex = TrexIO(0x07)
            self.razor = RazorIO()
            #self.sonar = [SonarIO(2, 3), SonarIO(4, 5), SonarIO(6, 7), SonarIO(8, 9)] # [Arriere, Droite, Avant, Gauche]
            self.sonarBack = SonarIO("back")
            self.sonarRight = SonarIO("right")
            self.sonarFront = SonarIO("front")
            self.sonarLeft =  SonarIO("left")
            self.sonar = [self.sonarBack,self.sonarRight,self.sonarFront,self.sonarLeft] # [Arriere, Droite, Avant, Gauche]

        else :
            print ("Create virtual mad")

            from multiprocessing import Process,Manager
            import vmad.simulation as simulation
            import vmad.modules.vTrex as vTrex
            import vmad.modules.vSonar as vSonar
            import vmad.modules.vRazor as vRazor

            global simuProc,sonarDmn

            manager = Manager()
            self.ns = manager.Namespace()
            self.trex = vTrex.vTrex()
            self.razor = vRazor.vRazorIO()
            self.sonarLeft = vSonar.vSonar("left")
            #print self.sonarLeft.__dict__
            self.sonarRight = vSonar.vSonar("right")
            self.sonarFront = vSonar.vSonar ("front")
            self.sonarBack = vSonar.vSonar("back")
            self.sonar = [self.sonarBack,self.sonarRight,self.sonarFront,self.sonarLeft]
            #self.sonar = [self.sonarFront]
            self.ns.isAlive = True
            simuProc = Process(target = simulation.simulate,args = (self.ns,self.trex.package,self.trex.changeData,self.trex.changeDataEnco,self.sonarLeft,self.sonarRight,self.sonarFront,self.sonarBack,self.razor.changeCap))
            simuProc.start()
            print ("Running Simulation")
            sonarFrontDaemon = Process(target = simulation.sonarFrontDeamon, args=(self.ns, self.sonarFront,self.sonarFront.changeSonarFront))
            sonarBackDaemon = Process(target = simulation.sonarBackDeamon, args=(self.ns, self.sonarBack,self.sonarBack.changeSonarBack))
            sonarLeftDaemon = Process(target = simulation.sonarLeftDeamon, args=(self.ns, self.sonarLeft,self.sonarLeft.changeSonarLeft))
            sonarRightDaemon = Process(target = simulation.sonarRightDeamon, args=(self.ns, self.sonarRight,self.sonarRight.changeSonarRight))
            #self.sonarRight,self.sonarRight.changeSonarRight,self.sonarLeft,self.sonarLeft.changeSonarLeft))
            sonarFrontDaemon.start()
            sonarBackDaemon.start()
            sonarLeftDaemon.start()
            sonarRightDaemon.start()
            print ("Running Sonar Deamons")


    ###########################
    ##          T-REX        ##
    ###########################

    def status(self):
        '''
        Read status from trex
        Return as a byte array
        '''
        raw_status = self.trex.i2cRead()
        return struct.unpack(">cchhHhHhhhhhh", raw_status)[2:]


    def reset(self):
        '''
        Reset the trex controller to default
        Stop dc motors...
        '''
        self.trex.reset()


    def motor(self, left, right):
        '''
	print("moteurs", left, right)
	return
        Set speed of the dc motors
        left and right can have the folowing values: -255 to 255
        -255 = Full speed astern
        0 = stop
        255 = Full speed ahead
        '''
        self.motor_last_change = time.time()*1000
#        print("moteur",left,right)
#        return
        try : lsign = left / abs(left)
        except ZeroDivisionError, e : lsign = 1

        try : rsign = right / abs(right)
        except ZeroDivisionError, e : rsign = 1

        left, right = lsign * min(abs(left), 255), rsign * min(abs(right), 255)

        left = int(left)
        right = int(right)
        # set left motor speed
        self.trex.package['lm_speed_high_byte'] = high_byte(left)
        self.trex.package['lm_speed_low_byte'] = low_byte(left)
        # set right motor speed
        self.trex.package['rm_speed_high_byte'] = high_byte(right)
        self.trex.package['rm_speed_low_byte'] = low_byte(right)
        # write the 27 bytes in package on the i2C bus
        self.trex.i2cWrite()  
        st = "speed set: left=%d, right=%d, [%d,%d,%d,%d]"%(left,right,self.trex.package['lm_speed_high_byte'],self.trex.package['lm_speed_low_byte'],self.trex.package['rm_speed_high_byte'],self.trex.package['rm_speed_low_byte']) 
        #os.system('echo "%s" >> sim.log'%(st))


    def servo(self, servo, position):
        '''
        Set servo position
        Servo = 1 to 6
        Position = Typically the servo position should be a value between 1000 and 2000 although it will vary depending on the servos used
        '''
        servo = str(servo)
        position = int(position)
        self.trex.package['servo_' + servo + '_high_byte'] = high_byte(position)
        self.trex.package['servo_' + servo + '_low_byte'] = low_byte(position)
        self.trex.i2cWrite()

    def encoder(self):
        status=struct.unpack(">BBhhHhHhhhhhh",self.trex.i2cRead())
        leftEnco = status[4]
        rightEnco = status[6]
        return leftEnco,rightEnco
        



    def getAngles(self):
        '''
        Return angles measured by the Razor (yaw/pitch/roll calculated automatically from the 9-axis data).
        '''
        return struct.unpack('fff', self.razor.getAngles())

    def getSensorData(self):
        """
            Output SENSOR data of all 9 axes in text format.
            One frame consist of three 3x3 float values = 36 bytes. Order is: acc x/y/z, mag x/y/z, gyr x/y/z.
        """
        return struct.unpack('fffffffff', self.razor.getRawSensorData())

    def getCalibratedSensorData(self):
        """
            Output CALIBRATED SENSOR data of all 9 axes in text format.
            One frame consist of three 3x3 float values = 36 bytes. Order is: acc x/y/z, mag x/y/z, gyr x/y/z.
        """
        return struct.unpack('fffffffff', self.razor.getCalibratedSensorData())

    ###########################
    ##     Sonar HC-SR04     ##
    ###########################

    def getSonars(self):
        '''
        Return angles measured by the Razor (calculated automatically from the 9-axis data).
        '''
        dist = [s.dist() for s in self.sonar]
        #for name, val in zip(["Sonar " + i + " : " for i in ["arriere", "droite", "avant", "gauche"]], dist) :
        #    if val == -1 : print name + "range <= 5 cm"
        #    else : print name + "%.1f" % val
        return dist

if __name__ == "__main__":
    # insert your test code here , example :
    myMad = mad()
    time.sleep(2)
    # test motor commands and measure encoders
    print "encoders ",myMad.encoder()
    myMad.motor(-100,-100)   #forward
    time.sleep(1)
    print "encoders ",myMad.encoder()
    time.sleep(1)
    print "encoders ",myMad.encoder()
    myMad.motor(-50,50) # turn  right
    time.sleep(1)
    myMad.motor(50,-50) # turn  left
    time.sleep(1)
        
    # test sonar
    myMad.motor(-60,-60)    
    for i in range(4):
        print i,myMad.getSonars()
        time.sleep(0.25)

    # go forward until wall
    frontDist = myMad.getSonars()[2]
    print frontDist
    while (frontDist == -1) or (frontDist > 40.0):
        frontDist = myMad.getSonars()[2]
        print frontDist
        time.sleep(0.25)
  
    
    # put the robot to heading to East
    myMad.motor(45,-45)
    turnOn = True
    while turnOn:
        head = myMad.getAngles()[0]
        print head
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
        print rDist
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
