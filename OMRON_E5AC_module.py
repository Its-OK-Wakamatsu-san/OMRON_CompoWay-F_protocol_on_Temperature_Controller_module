# https://github.com/TurBoss/TurBoHostLink
# OMRON CompoWay/F Protocol           
# Temperature Controller E5AC
import serial
import time
from functools import reduce
from operator import xor

class Application:
    def __init__(self):
        # command break down 
        self.cmd_stx_b =  b'\x02'       # start of text
        self.cmd_0     = '01000'        # NODE:01 SubAddress:00 SID:0
        self.cmd       = '0503'         # MRC/SRC(MainRequestCode/SubRequestCode)  typical comand 
        self.cmd_etx_b =  b'\x03'       # end of text 

    def Connect_Device(self):
        try:
            self.serial_port = serial.Serial(
                port='COM3',\
                baudrate=38400,\
                parity=serial.PARITY_EVEN,\
                stopbits=serial.STOPBITS_TWO,\
                bytesize=serial.SEVENBITS,\
                timeout=0 )
            #print("connected to: " + self.serial_port.portstr)                       #CHG COM15 -> COM3 temporary  CompoWay/F default baudrate is 38400bps 
            setting = self.serial_port.get_settings()
            #print("Serial Setting is : ",setting)
        except:
            print('Error: OMRON_E5AC not Found ') 
        return
    
    # FCS                      copy from  https://github.com/TurBoss/TurBoHostLink
    def Compute_FCS(self, msg):
        return format(reduce(xor, map(ord, msg)), '01x')                #CHG 'x' → '01x'. Output is string.
    
    # write Command & read E5AC buffer
    def Command_Response(self, cmd):
        cmd_ASCII = self.cmd_0 + cmd + self.cmd_etx_b.decode()          # cmd in ASCII character

        fcs = self.Compute_FCS( cmd_ASCII )                             # calculate cmd_ASCII XOR
        fcs_h = int(fcs,16)                                             #INS  change hex_string → integer
        bcc_b = fcs_h.to_bytes(1, byteorder='big')                      #INS  change integer    → bainary
        cmd_b = self.cmd_stx_b + cmd_ASCII.encode() + bcc_b
        
        self.Connect_Device()
        self.serial_port.write(cmd_b)
        time.sleep(0.05)                                        # Wait a minute (0.1s).    tried minimum wait time  ... about 0.05s

        #print("Receive from OMRON E5AC:")
        buf = self.serial_port.read()                           # read start of text         stx_b =  b'\x02'
        buf_full = self.serial_port.read_all()                  # b'01000005030000E5AC-TCX4A00D9\x03\x1c'                        
        #                                                       #   0123456789012345678901234567890
        buf_full_ASCII = buf_full.decode()                      #  '01000005030000E5AC-TCX4A00D9  ' 
        buf_ASCII = buf_full_ASCII[10:]

        self.serial_port.close()

        return buf_ASCII
    
    def Device_Info(self):  
        cmd       = '0503'         # MRC/SRC(MainRequestCode/SubRequestCode)
        buf_ASCII = self.Command_Response(cmd)              #0000E5AC-TCX4A00D9                                         
        str_ID = buf_ASCII[4:14]                            #0123456789012345678901234
        return str_ID
    
    def Device_Status(self):  
        cmd       = '0601'         # MRC/SRC(MainRequestCode/SubRequestCode)
        buf_ASCII = self.Command_Response(cmd)              #00000100                     
        str_status = buf_ASCII[4:8]                         #0123456789012345678901234
        return str_status

    def Get_Temp(self):  
        cmd       = '0101C00000000001'         # MRC/SRC(MainRequestCode/SubRequestCode) & Command
        #            0123456789012345
        buf_ASCII = self.Command_Response(cmd)              #000000000018                                  
        temp_h = buf_ASCII[4:12]                            #0123456789012345678901234
        temp = int(temp_h,16)
        return temp
    
if __name__ == '__main__':
    OMRON_E5AC = Application()

    # usage example
    # import OMRON_E5AC_module
    #         self.OMRON_E5AC   = OMRON_E5AC_module.Application()
    #         str_ID            = OMRON_E5AC.Device_Info() 

    # Check Start Time
    time_A    = time.time()

    str_ID = OMRON_E5AC.Device_Info()
    print("Device_Info = ", str_ID)

    str_status = OMRON_E5AC.Device_Status()
    print("Device_Status =", str_status)
    
    temp_Present_Value = OMRON_E5AC.Get_Temp()
    print("Temp_PV (°C) =", temp_Present_Value)

    # Check Start Time
    time_B     = time.time()
    turn_around_time = (time_B - time_A)
    print('Turn_around_time:', turn_around_time)