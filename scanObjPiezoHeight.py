from labscript import *
from labscriptlib.CF1.connection_table import do_connectiontable

###################################################################################################
## START SEQUENCE ##
###################################################################################################
do_connectiontable() 
start()
t = 0 
######## set up instruments ##
Piezo.setamp(t, PiezoScanHeight)


t+=1e-6
######## make laser spot point to correct location #########
galvoX.constant(t, Vx_laser)
galvoY.constant(t, Vy_laser)  


############################# polarize, collect ref ########################################
t+=1e-6
laser.go_high(t) 
ctrGate.go_high(t) #start reference counts
DAQCounter.acquire(numIterations=100, label='ref')
t+=1e-3
ctrGate.go_low(t) #stop reference counts
laser.go_low(t) #laser turns off 



# t+=2.5e-6
pb.outerLoop(100) #
stop(t+10e-6)