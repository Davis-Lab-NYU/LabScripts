from labscript import *
from labscriptlib.CF1.connection_table import do_connectiontable
###################################################################################################
## START SEQUENCE ##
###################################################################################################
do_connectiontable()
start()
t = 0

#set piezo to 0 um
Piezo.setamp(t, 0)
t+=1e-6

laser.go_high(t)
t+= 1e-6

galvoY.constant(t, vY)

#loop over different piezo heights
for i in range(xPoints):
    pb.startLoop(t, ['outer', 1], zPoints)

    pb.startLoop(t, ['outer', 1], xPoints)
    galvoX.constant(t, Vx_offset + Vx_min + i * (Vx_max - Vx_min) / xPoints)
    t += 100e-6  # 123.4e-6#dt

    #Loop over x axis
    for j in range(zPoints):
        pb.startLoop(t, ['inner', 1, 1], zPoints)
        Piezo.setamp(t,j*(zMax/zPoints))
        t+=dt
        ctrGate.go_high(t)
        DAQCounter.acquire(numIterations=xPoints*zPoints, label='scan')
        t+=3*dt
        ctrGate.go_low(t)
        t += dt
        pb.endLoop(t, ['inner', 1, 1])
    t+=10e-6
    pb.endLoop(t, ['outer', 1])


t += 150e-6
laser.go_low(t)

#send galvo to 0
galvoX.constant(t,0)
galvoY.constant(t,0)

t+=10e-6
pb.outerLoop(0)
stop(t+1e-6)