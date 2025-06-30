from labscript import *
from labscriptlib.CF1.connection_table import do_connectiontable

##--------Start Pulse Sequence-----------##

do_connectiontable()
start()
t = 0

######## set up instruments ##
Piezo.setamp(t, objPiezoHeight)
######## SRS #########
SRSDDS1.setamp(t, t1inv_SRS_amp)
SRSDDS1.setfreq(t, t1inv_freq_center)
SRSDDS1.enable_mod(t, True)

t+=1e-6
galvoX.constant(t, Vx_laser)
galvoY.constant(t, Vy_laser)

##-------Polarize and collect reference------##
t+=1e-6
laser.go_high(t)
t+=(t1inv_pol_dur+t1inv_AOMDelay)
ctrGate.go_high(t)
add_time_marker(t,'ref detect start')
DAQCounter.acquire(numIterations=t1_numIterations, label='ref')
t+=t1_ctrGateDuration
ctrGate.go_low(t)
laser.go_low(t)

t+=(t1inv_AOM_delay+300e-9) #wait for laser to turn off and ISC crossing delay- calibrate this

##---------Inversion Pi pulse------##
add_time_marker(t ,'MW switch on (pi/2)')
MWswitch.go_high(t)
t+=(t1_pi_pulse+24e-9)
add_time_marker(t ,'MW switch off (pi/2)')
MWswitch.go_low(t)

##---------delay time------##
t+=(t1inv_delay_time*(10**-6))

##------Collect Signal---------##
laser.go_high(t)
ctrGate.go_high(t+t1_AOMDelay)
add_time_marker(t+t1_AOMDelay,'sig detect start')
DAQCounter.acquire(numIterations=t1inv_numIterations, label='sig')
t+=(t1_ctrGateDuration)
ctrGate.go_low(t+t1_AOMDelay)
laser.go_low(t)

t += 5e-6
pb.outerLoop(0)

stop(t)

#----------End Sequence-----------#