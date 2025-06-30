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
SRSDDS1.setfreq(t, rabi_freqCenter + rabi_freqMod)
SRSDDS1.enable_mod(t, True) ###only turns on RF output

SRSDDS1.enable_IQ(t)

######## make laser spot point to correct location #########
t+=0.5e-6 #need this if AO are not static
galvoX.constant(t, Vx_laser)
galvoY.constant(t, Vy_laser)
#
#
#

FPGA.set_start_src(t, 'external')


FPGA.add_waveform(t,'XQ','const',100,32766,90,int(rabi_pulse_time/2.6),'oneshot') # length in clock ticks (2.6ns)
FPGA.add_waveform(t,'XI','const',100,32766,0,int(rabi_pulse_time/2.6),'oneshot')


FPGA.add_program(t,'ch6','XI')
FPGA.add_program(t,'ch7','XQ')




############################# polarize, collect ref ########################################
#
laser.go_high(t)
t+=(rabi_polDuration+rabi_AOMDelay)
ctrGate.go_high(t+Rabi_refDelay) #start reference counts
DAQCounter.acquire(numIterations=rabi_numIterations, label='ref')
t+=rabi_ctrGateDuration
ctrGate.go_low(t+Rabi_refDelay) #stop reference counts
t+=5e-6
laser.go_low(t) #laser turns off

t+=(rabi_waitTime)


FPGAtrig.go_high(t)
t += 678e-9         #delay between trig and FPGA outputs sending pulse
FPGAtrig.go_low(t)

############################# MW pulse ########################################
#t+=32e-9            #delay between FPGA pulse and SRS outputs
MWswitch.go_high(t)

#add_time_marker(t ,'MW switch on')
if rabi_pulse_time < 20:
    MWswitch.go_low(t+ 40e-9)

elif rabi_pulse_time>= 0:
    add_time_marker(t + (rabi_pulse_time)*(10**(-9)) + 24e-9,'MW switch off')
    MWswitch.go_low(t + (rabi_pulse_time)*(10**(-9))+ 24e-9 )


# ############################# collect signal ########################################

t+= (rabi_pulse_time*(10**(-9))) + 24e-9 #- ctrGateDuration



laser.go_high(t)


add_time_marker(t+rabi_AOMDelay+Rabi_sigDelay,'sig detect start')
ctrGate.go_high(t+rabi_AOMDelay+Rabi_sigDelay) #start reference counts
DAQCounter.acquire(numIterations=rabi_numIterations, label='sig1')
t+=rabi_ctrGateDuration
ctrGate.go_low(t+rabi_AOMDelay+Rabi_sigDelay) #stop reference counts
add_time_marker(t+rabi_AOMDelay+Rabi_sigDelay,'sig detect end')

t+=5e-6
laser.go_low(t)


pb.outerLoop(rabi_numIterations)
stop(t+10e-6)


##############################
## END sequence ##
##############################
#########################################################
############################################################
# ##########################################################
# ######
