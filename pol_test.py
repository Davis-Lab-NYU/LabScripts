from labscript import *
from labscriptlib.CF1.connection_table import do_connectiontable
###################################################################################################
## START SEQUENCE ##
###################################################################################################
do_connectiontable()
start()
t = 0
######## set up instruments ##
Piezo.setamp(t, objPiezoHeight)
######## SRS and FPGA #########
SRSDDS1.setamp(t, test_SRSAmp)
SRSDDS1.setfreq(t, test_freqCenter + test_freqMod)
SRSDDS1.enable_mod(t, True) ###only turns on RF output


######## make laser spot point to correct location #########
t+=0.5e-6 #need this if AO are not static
galvoX.constant(t, Vx_laser)
galvoY.constant(t, Vy_laser)



############################# polarize, collect ref ########################################

laser.go_high(t)
t+=test_polDuration*1e-6
ctrGate.go_high(t) #start reference counts
DAQCounter.acquire(numIterations=test_numIterations, label='ref')
t+=test_ctrGateDuration
ctrGate.go_low(t) #stop reference counts
laser.go_low(t) #laser turns off

t+=(test_AOMDelay+300e-9)



############################# MW pulse ########################################
MWswitch.go_high(t) #turn on MW switch
t+= (test_pi_time)*(10**(-9)) + 24e-9
MWswitch.go_low(t)


# ############################# collect signal ########################################



laser.go_high(t)
laser.go_low(t+2e-6)

add_time_marker(t+test_AOMDelay,'sig detect start')
ctrGate.go_high(t+test_AOMDelay) #start reference counts
DAQCounter.acquire(numIterations=test_numIterations, label='sig')
t+=test_ctrGateDuration
ctrGate.go_low(t+test_AOMDelay) #stop reference counts
add_time_marker(t+test_AOMDelay,'sig detect end')
t+=5e-6



pb.outerLoop(test_numIterations)
stop(t+1e-6)


##############################
## END sequence ##
##############################
#########################################################
############################################################
# ##########################################################
# ######
