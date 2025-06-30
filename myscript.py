from labscript import *
from labscriptlib.CF1.connection_table import do_connectiontable

#--------------------------Start Experiment--------------------------#
do_connectiontable()

start()
t = 0

#--------------------------Initialize Devices------------------------#

# Set Piezo height
Piezo.setamp(t,objPiezoHeight)

t+=1e-6

# Point laser at ensemble
galvoX.constant(t,Vx_laser)
galvoY.constant(t,Vy_laser)
AO_3.constant(t,0) #dummy

# Setup SRS parameters
SRSDDS1.setamp(t, ESR_SRS_amp)          #amplitude
SRSDDS1.setfreq(t, ESR_freq_center)     #central frequency
SRSDDS1.set_sweep_dev(t, freq_dev)      #deviation of frequency sweep
SRSDDS1.enable_mod(t, True)             #enable modulation and sweep
SRSDDS1.enable_freq_sweep(t)

# Turn laser and MW switch on
laser.go_high(t)
MWswitch.go_high(t)

#--------------------------Sweep through frequencies -----------------------#
for i in range(ESR_numIterations):
    pb.startLoop(t, ['outer', 1], ESR_numIterations)

    #set modulation frequency
    #ESRfreqMod.constant(t, .5)
    t += ESR_dt

    for j in range(ESR_numPoints):
        pb.startLoop(t, ['inner', 1, 1], ESR_numPoints)

        c = 0

        # if j < ESR_numPoints / 2:
        #     c = -1 + 2 * j / (ESR_numPoints / 2 - 1)
        #     ESRfreqMod.constant(t,c)
        #     #ESRfreqMod.constant(t, -1 + 2 * j / (ESR_numPoints / 2 - 1))
        # else:
        #     #ESRfreqMod.constant(t, 3 - 2 * j / (ESR_numPoints / 2 - 1))
        #     c = 3 - 2 * j / (ESR_numPoints / 2 - 1)
        #     ESRfreqMod.constant(t, c)

        #-----begin counting------#
        ctrGate.go_high(t)
        DAQCounter.acquire(numIterations=ESR_numIterations * (ESR_numPoints), label='ctrIn')
        t += 3 * ESR_dt
        ctrGate.go_low(t)
        # -----end counting------#

        t += ESR_dt
        pb.endLoop(t, ['inner', 1, 1])
    ESRfreqMod.constant(t, 0)
    t += 123.4e-6  # 10e-3#300e-6#500e-6
    pb.endLoop(t, ['outer', 1])

# Turn laser and MW switch off
laser.go_low(t)
MWswitch.go_low(t)

t += 10e-6
pb.outerLoop(0)
stop(t)