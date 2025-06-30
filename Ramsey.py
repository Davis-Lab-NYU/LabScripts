from labscript import *
from labscriptlib.CF1.connection_table import do_connectiontable

##--------Start Pulse Sequence-----------##

do_connectiontable()
start()
t = 0

######## set up instruments ##
Piezo.setamp(t, objPiezoHeight)
######## SRS #########
SRSDDS1.setamp(t, Ramsey_SRS_amp)
SRSDDS1.setfreq(t, Ramsey_freq_c+Ramsey_freq_mod)
SRSDDS1.enable_mod(t, True) ###only turns on RF output
SRSDDS1.enable_IQ(t)

t+=1e-6
galvoX.constant(t, Vx_laser)
galvoY.constant(t, Vy_laser)


FPGA.set_start_src(t, 'external')

# add_waveform(t, label, style, freq, gain, phase, length, mode)
FPGA.add_waveform(t,'XI','const',Ramsey_freq_mod,32766,90,int(Ramsey_pi_half_pulse/2.6e-9),'oneshot') # length in clock ticks (2.6ns)
FPGA.add_waveform(t,'XQ','const',Ramsey_freq_mod,32766,0,int(Ramsey_pi_half_pulse/2.6e-9),'oneshot')
FPGA.add_waveform(t,'-XI','const',Ramsey_freq_mod,32766,270,int(Ramsey_pi_half_pulse/2.6e-9),'oneshot') # length in clock ticks (2.6ns)
FPGA.add_waveform(t,'-XQ','const',Ramsey_freq_mod,32766,180,int(Ramsey_pi_half_pulse/2.6e-9),'oneshot')
# FPGA.add_waveform(t,'I','const',Ramsey_freq_mod,0,0,int(rabi_pulse_time/2.6e-9),'oneshot') # length in clock ticks (2.6ns)

#dark
#first pi/2 pulse
FPGA.add_program(t,'ch6','XI')
FPGA.add_program(t,'ch7','XQ')

# FPGA.add_program(t+(Ramsey_pi_half_pulse/1e-9),'ch6','XI')
# FPGA.add_program(t+(Ramsey_pi_half_pulse/1e-9),'ch7','XQ')
#^ testing phase change
#second pi/2 pulse
FPGA.add_program(t+(Ramsey_pi_half_pulse/1e-9)+Ramsey_precession_time,'ch6','XI')
FPGA.add_program(t+(Ramsey_pi_half_pulse/1e-9)+Ramsey_precession_time,'ch7','XQ')


#bright sequence pulses
#first pi/2 pulse
FPGA.add_program(t+((2*Ramsey_pi_half_pulse+Ramsey_ctrGateDuration+Ramsey_pol_dur+Ramsey_AOMDelay+Ramsey_waitTime)/1e-9)+Ramsey_precession_time,'ch6','XI')
FPGA.add_program(t+((2*Ramsey_pi_half_pulse+Ramsey_ctrGateDuration+Ramsey_pol_dur+Ramsey_AOMDelay+Ramsey_waitTime)/1e-9)+Ramsey_precession_time,'ch7','XQ')

#second pi/2 pulse (-X axis) -> 180 phase shift
FPGA.add_program(t+((3*Ramsey_pi_half_pulse+Ramsey_ctrGateDuration+Ramsey_pol_dur+Ramsey_AOMDelay+Ramsey_waitTime)/1e-9)+2*Ramsey_precession_time,'ch6','-XI')
FPGA.add_program(t+((3*Ramsey_pi_half_pulse+Ramsey_ctrGateDuration+Ramsey_pol_dur+Ramsey_AOMDelay+Ramsey_waitTime)/1e-9)+2*Ramsey_precession_time,'ch7','-XQ')



MWswitch.go_high(t)

##-------Polarize and collect reference------##
t+=1e-6
laser.go_high(t)
t+=(Ramsey_pol_dur+Ramsey_AOMDelay)
ctrGate.go_high(t+Ramsey_refDelay)
add_time_marker(t,'ref detect start')
DAQCounter.acquire(numIterations=Ramsey_numIterations, label='ref')
t+=Ramsey_ctrGateDuration
ctrGate.go_low(t+Ramsey_refDelay)
t+=5e-6
laser.go_low(t)

t+= Ramsey_waitTime

FPGAtrig.go_high(t)
t += (678-24)*1e-9
FPGAtrig.go_low(t)

##-------------------------------Dark--------------------------------##
#---------Pi/2 Pulse----------##
add_time_marker(t ,'MW switch on (pi/2)')
#MWswitch.go_high(t)
t+=(Ramsey_pi_half_pulse)
add_time_marker(t ,'MW switch off (pi/2)')
#MWswitch.go_low(t)

##---------Free Precession------##
t+=((Ramsey_precession_time)*(10**(-9)))

##---------Pi/2 Pulse----------##
add_time_marker(t ,'MW switch on (pi/2)')
#MWswitch.go_high(t)
t+=(Ramsey_pi_half_pulse)
add_time_marker(t ,'MW switch off (pi/2)')
#MWswitch.go_low(t)

##------Collect Signal---------##
laser.go_high(t)
ctrGate.go_high(t+Ramsey_AOMDelay+Ramsey_sigDelay)
add_time_marker(t+Ramsey_AOMDelay,'dark sig detect start')
DAQCounter.acquire(numIterations=Ramsey_numIterations, label='sig_dark')
t+=(Ramsey_ctrGateDuration)
ctrGate.go_low(t+Ramsey_AOMDelay+Ramsey_sigDelay)


##-------------------------------Transition to Bright sequence-------------------------##
## polarization ##
t+=(Ramsey_pol_dur+Ramsey_AOMDelay)
laser.go_low(t)

t+=Ramsey_waitTime #wait for laser to turn off and ISC crossing delay

##---------Pi/2 Pulse----------##
add_time_marker(t,'MW switch on (pi/2)')
#MWswitch.go_high(t)
t+=(Ramsey_pi_half_pulse)
add_time_marker(t ,'MW switch off (pi/2)')
#MWswitch.go_low(t)

#change SRS phase here


# ##---------Free Precession------##
t+=((Ramsey_precession_time)*(10**(-9)))


#---------Pi/2 Pulse (along -x)----------##
#MWswitch.go_high(t)
t+=(Ramsey_pi_half_pulse )
#MWswitch.go_low(t)



##------Collect Signal---------##
laser.go_high(t)
ctrGate.go_high(t+Ramsey_AOMDelay+Ramsey_sigDelay)
# add_time_marker(t+Ramsey_AOMDelay,'bright sig detect start')
DAQCounter.acquire(numIterations=Ramsey_numIterations, label='sig_bright')
t+=(Ramsey_ctrGateDuration)
ctrGate.go_low(t+Ramsey_AOMDelay+Ramsey_sigDelay)




t += 5e-6
laser.go_low(t)
MWswitch.go_low(t)

pb.outerLoop(Ramsey_numIterations)

stop(t+10e-6)

#----------End Sequence-----------#