from labscript import *

from labscript_devices.PulseBlasterESRPro500 import PulseBlasterESRPro500
# from labscript_devices.ZCU111 import ZCU111, ZCU111DDS
from labscript_devices.PiezoEO import PiezoEO, PiezoEODDS
from labscript_devices.NI_DAQmx.models import NI_USB_6363  # NI_PCIe_6343

from labscript_devices.SRS384 import SRS384, SRS384DDS
from labscript_devices.FPGAAWG import FPGAAWG, FPGAAWGDDS

def do_connectiontable():
    ##### The Pulseblaster is triggering the FPGA and the NI DAQ
    PulseBlasterESRPro500(name='pb')
    ClockLine(name="pb_clockline", pseudoclock=pb.pseudoclock, connection="flag 0")
    #ClockLine(name="pb_clockline_2", pseudoclock=pb.pseudoclock, connection="flag 5") #is this just to make the code work or do we actually need flag 5?
    #setting clockline2 flag = 5 seems to make all flags output a pulse sporadically during the experiment

    DigitalOut('ctrGate', pb.direct_outputs, 'flag 1')  # counter readout
    DigitalOut('laser', pb.direct_outputs, 'flag 2')  # AOM Switch
    DigitalOut('MWswitch', pb.direct_outputs, 'flag 3')  # MW gate
    DigitalOut('FPGAtrig', pb.direct_outputs, 'flag 4')  # FPGA trigger

    ##### NI DAQ
    NI_USB_6363(name='NIDAQ',
                parent_device=pb_clockline,
                clock_terminal='/Dev2/PFI5',
                MAX_name='Dev2',
                static_AO=False,
                stop_order=-1,
                acquisition_rate=1e5
                )

    AnalogOut('galvoX', NIDAQ, 'ao0')
    AnalogOut('galvoY', NIDAQ, 'ao1')
    AnalogOut('ESRfreqMod', NIDAQ, 'ao2')
    AnalogOut('AO_3', NIDAQ, 'ao3')  # dummy; need an even number of AO
    GatedCounterIn("DAQCounter", NIDAQ, connection="ctr2", gate="PFI1")  # , numIterations = numIterations)


    ##### FPGA
    FPGAAWG(name='ZCU', parent_device=pb_clockline, com_port='COM7')
    FPGAAWGDDS('FPGA', ZCU, 'a')

    ##### FPGA
    # ZCU111(name = 'ZCU', parent_device = pb_clockline_2, com_port = 'COM5')
    # ZCU111DDS('FPGA', ZCU, 'a')

    ##### Piezo for objective
    PiezoEO(name = 'EO', parent_device = pb_clockline)
    PiezoEODDS('Piezo', EO, 'a')

    ##### SRS
    SRS384(name='SRS1', parent_device=pb_clockline, com_port='COM4')
    SRS384DDS('SRSDDS1', SRS1, 'a1')
    ##############################
    ## END Connection table ##
    ##############################


if __name__ == '__main__':
    do_connectiontable()
    # Begin issuing labscript primitives
    # start() elicits the commencement of the shot
    start()

    # Stop the experiment shot with stop()
    stop(10e-6)