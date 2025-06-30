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
SRSDDS1.setamp(t, rabi_SRSAmp)
SRSDDS1.setfreq(t, ref_freq)
SRSDDS1.enable_mod(t, True) ###only turns on RF output


######## make laser spot point to correct location #########
t+=0.5e-6 #need this if AO are not static
galvoX.constant(t, Vx_laser)
galvoY.constant(t, Vy_laser)

############################# polarize, collect ref ########################################

t+=1e-6
laser.go_high(t)
t+=rabi_polDuration+rabi_AOMDelay
ctrGate.go_high(t) #start reference counts
DAQCounter.acquire(numIterations=rabi_numIterations, label='ref')
t+=rabi_ctrGateDuration
ctrGate.go_low(t) #stop reference counts
laser.go_low(t) #laser turns off
t+=rabi_AOMDelay
############################# MW pulse ########################################

MWswitch.go_high(t) #turn on MW switch
if rabi_pulse_time < 20:
    MWswitch.go_low(t+ 40e-9)
elif rabi_pulse_time>= 0:
    add_time_marker(t + (rabi_pulse_time)*(10**(-9)) + 24e-9,'MW switch off')
    MWswitch.go_low(t + (rabi_pulse_time)*(10**(-9)) + 24e-9)




############################# collect signal ########################################
t+= (rabi_pulse_time*(10**(-9))) + 24e-9 #- ctrGateDuration

laser.go_high(t)


add_time_marker(t+rabi_AOMDelay,'sig detect start')
ctrGate.go_high(t+rabi_AOMDelay) #start reference counts
DAQCounter.acquire(numIterations=rabi_numIterations, label='sig1')
t+=rabi_ctrGateDuration
ctrGate.go_low(t+rabi_AOMDelay) #stop reference counts
add_time_marker(t+rabi_AOMDelay,'sig detect end')




# laser.go_high(t)
# ctrGate.go_high(t+rabi_AOMDelay) #start reference counts
# DAQCounter.acquire(numIterations=rabi_numIterations, label='sig1')
# ctrGate.go_low(t+rabi_AOMDelay+rabi_ctrGateDuration) #stop reference counts
# laser.go_low(t+2e-6)

t+=300e-6
laser.go_low(t)
pb.outerLoop(rabi_numIterations)
stop(t+1e-6)

##############################
## END sequence ##
##############################
####################################################################################################################################################################################