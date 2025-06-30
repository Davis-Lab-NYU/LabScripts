from labscript import *
from labscriptlib.CF1.connection_table import do_connectiontable
###################################################################################################
## START SEQUENCE ##
###################################################################################################
do_connectiontable()
start()
t = 0
Piezo.setamp(t, objPiezoHeight)
t+=1e-6

#anaout_3.constant(t,0) #dummy
laser.go_high(t)
t+= 500e-6


galvoY.constant(t, y_ctr)
t += res_dt
for i in range(num_points):
    pb.startLoop(t, ['outer', 1], num_points)


    galvoX.constant(t, x_min + i * (x_max - x_min) / num_points)

    t += res_dt
    ctrGate.go_high(t)
    DAQCounter.acquire(numIterations=num_points, label='x_scan')
    t += 3 * res_dt
    ctrGate.go_low(t)
    t += res_dt

    pb.endLoop(t, ['outer', 1])


galvoX.constant(t, x_ctr)
t += res_dt

for i in range(num_points):
    pb.startLoop(t, ['outer2', 1], num_points)

    galvoY.constant(t, y_min + i * (y_max - y_min) / num_points)

    t += res_dt
    ctrGate.go_high(t)
    DAQCounter.acquire(numIterations=num_points, label='y_scan')
    t += 3 * res_dt
    ctrGate.go_low(t)
    t += res_dt
    pb.endLoop(t, ['outer2', 1])

t += 150e-6
laser.go_low(t)

#send galvo to 0
galvoX.constant(t,0)
galvoY.constant(t,0)

t+=10e-6
pb.outerLoop(0)
stop(t+1e-6)