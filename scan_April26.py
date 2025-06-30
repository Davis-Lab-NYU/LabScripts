from labscript import *
from labscriptlib.CF1.connection_table import do_connectiontable
###################################################################################################
## START SEQUENCE ##
###################################################################################################
do_connectiontable()
start()
t = 0
#adding SRS initialization#
# Setup SRS parameters
SRSDDS1.setamp(t, ESR_SRS_amp)          #amplitude
SRSDDS1.setfreq(t, ESR_freq_center)     #central frequency
SRSDDS1.set_sweep_dev(t, freq_dev)      #deviation of frequency sweep
SRSDDS1.enable_mod(t, True)             #enable modulation and sweep
SRSDDS1.enable_freq_sweep(t)
#SRSDDS1.enable_output(t)



Piezo.setamp(t, objPiezoHeight)
t+=1e-6

t += 1e-6
#AO_3.constant(t,0) #dummy
laser.go_high(t)

MWswitch.go_high(t)
t+= 1e-6

for i in range(xPoints):
    pb.startLoop(t, ['outer', 1], xPoints)
    galvoX.constant(t, Vx_offset+Vx_min + i*(Vx_max-Vx_min)/xPoints)
    t+=100e-6#123.4e-6#dt
    for j in range(yPoints):
        pb.startLoop(t, ['inner', 1, 1], yPoints)
        if j < yPoints / 2:
           galvoY.constant(t, Vy_offset + Vy_min + j * (Vy_max - Vy_min) / (yPoints / 2))
        else:
           galvoY.constant(t, Vy_offset + Vy_max + (Vy_max - Vy_min) - j * (Vy_max - Vy_min) / (yPoints / 2))
        #galvoY.constant(t, Vy_offset+Vy_max - j*(Vy_max-Vy_min)/(yPoints))
        t+=dt #125 us
        ctrGate.go_high(t)
        DAQCounter.acquire(numIterations=xPoints*yPoints, label='scan')
        t+=3*dt # 375 us
        ctrGate.go_low(t)
        t += dt #125 us
        pb.endLoop(t, ['inner', 1, 1])
    t+=10e-6
    pb.endLoop(t, ['outer', 1])


t += 150e-6
laser.go_low(t)
MWswitch.go_low(t)

#send galvo to 0
galvoX.constant(t,0)
galvoY.constant(t,0)

t+=10e-6
pb.outerLoop(0)
stop(t+1e-6)
##############################
## END sequence ##
##############################
#############################################################################################################################
# #######################################################
