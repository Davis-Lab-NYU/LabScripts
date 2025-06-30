from labscript import *
from labscriptlib.CF1.connection_table import do_connectiontable

##--------Start Pulse Sequence-----------##

do_connectiontable()
start()
t = 0

######## set up instruments ##
Piezo.setamp(t, objPiezoHeight)
######## SRS  #########
SRSDDS1.setamp(t, SE_SRS_amp)
SRSDDS1.setfreq(t, SE_freq_center)
SRSDDS1.enable_mod(t, True)

t+=1e-6
galvoX.constant(t, Vx_laser)
galvoY.constant(t, Vy_laser)

##-------Polarize and collect reference------##
t+=1e-6
laser.go_high(t)
t+=(SE_pol_dur+SE_AOMDelay)
ctrGate.go_high(t)
add_time_marker(t,'ref detect start')
DAQCounter.acquire(numIterations=SE_numIterations, label='ref')
t+=SE_ctrGateDuration
ctrGate.go_low(t)
laser.go_low(t)

t+=(SE_AOMDelay+300e-9) #wait for laser to turn off and ISC crossing delay- calibrate this

##---------Pi/2 Pulse----------##
add_time_marker(t ,'MW switch on (pi/2)')
MWswitch.go_high(t)
t+=(SE_pi_half_pulse+24e-9)
add_time_marker(t ,'MW switch off (pi/2)')
MWswitch.go_low(t)

##---------Free Precession------##
t+=((SE_precession_time/2)*(10**(-6)))

##---------Pi pulse------##
add_time_marker(t ,'MW switch on (pi)')
MWswitch.go_high(t)
t+=(SE_pi_pulse+24e-9)
add_time_marker(t ,'MW switch off (pi)')
MWswitch.go_low(t)

##---------Free Precession------##
t+=((SE_precession_time/2)*(10**(-6)))


##---------Pi/2 Pulse----------##
add_time_marker(t ,'MW switch on (pi/2)')
MWswitch.go_high(t)
t+=(SE_pi_half_pulse+24e-9)
add_time_marker(t ,'MW switch off (pi/2)')
MWswitch.go_low(t)

##------Collect Signal---------##
laser.go_high(t)
ctrGate.go_high(t+SE_AOMDelay)
add_time_marker(t+SE_AOMDelay,'sig detect start')
DAQCounter.acquire(numIterations=SE_numIterations, label='sig')
t+=(SE_ctrGateDuration)
ctrGate.go_low(t+SE_AOMDelay)
laser.go_low(t)

t += 5e-6
pb.outerLoop(SE_numIterations)

stop(t)

#----------End Sequence-----------#