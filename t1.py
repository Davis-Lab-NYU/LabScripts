from labscript import *
from labscriptlib.CF1.connection_table import do_connectiontable

##--------Start Pulse Sequence-----------##

do_connectiontable()
start()
t = 0

######## set up instruments ##
Piezo.setamp(t, objPiezoHeight)
######## SRS #########
SRSDDS1.setamp(t, t1_SRS_amp)
SRSDDS1.setfreq(t, t1_freq_center)
SRSDDS1.enable_mod(t, True)

t+=0.5e-6
galvoX.constant(t, Vx_laser)
galvoY.constant(t, Vy_laser)

##-------Polarize and collect reference------##
t+=1e-6
laser.go_high(t)
t+=(t1_pol_dur+t1_AOMDelay)
ctrGate.go_high(t)
add_time_marker(t,'ref detect start')
DAQCounter.acquire(numIterations=t1_numIterations, label='ref1')
t+=t1_ctrGateDuration
ctrGate.go_low(t)
laser.go_low(t)

t+=(t1_AOMDelay+300e-9) #wait for laser to turn off and ISC crossing delay- calibrate this


##---------delay time------##
t+=(t1_delay_time*(10**-6))



##------Collect Signal---------##
laser.go_high(t)
ctrGate.go_high(t+t1_AOMDelay)
add_time_marker(t+t1_AOMDelay,'sig detect start')
DAQCounter.acquire(numIterations=t1_numIterations, label='sig1')
t+=(t1_ctrGateDuration)
ctrGate.go_low(t+t1_AOMDelay)
laser.go_low(t)


## -------- pop inv-------------##

# ##-------Polarize and collect reference------##
# t+=1e-6
# laser.go_high(t)
# t+=(t1_pol_dur+t1_AOMDelay)
# ctrGate.go_high(t)
# add_time_marker(t,'ref detect start')
# DAQCounter.acquire(numIterations=t1_numIterations, label='ref2')
# t+=t1_ctrGateDuration
# ctrGate.go_low(t)
# laser.go_low(t)
#
# t+=(t1_AOMDelay+300e-9) #wait for laser to turn off and ISC crossing delay- calibrate this
#
# ##---------Pi pulse------##
# add_time_marker(t ,'MW switch on (pi)')
# MWswitch.go_high(t)
# t+=(t1_pi_pulse+24e-9)
# add_time_marker(t ,'MW switch off (pi)')
# MWswitch.go_low(t)
#
# ##---------delay time------##
# t+=(t1_delay_time*(10**-6))
#
#
#
# ##------Collect Signal---------##
# laser.go_high(t)
# ctrGate.go_high(t+t1_AOMDelay)
# add_time_marker(t+t1_AOMDelay,'sig detect start')
# DAQCounter.acquire(numIterations=t1_numIterations, label='sig2')
# t+=(t1_ctrGateDuration)
# ctrGate.go_low(t+t1_AOMDelay)
# laser.go_low(t)


t += 5e-6
pb.outerLoop(t1_numIterations)

stop(t+1e-6)

#----------End Sequence-----------#