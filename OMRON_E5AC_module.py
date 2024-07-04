# https://github.com/TurBoss/TurBoHostLink
# OMRON CompoWay/F Protocol           
# Temperature Controller E5AC
import serial
from functools import reduce
from operator import xor
import time

class Application:
    def __init__(self):
        # command break down   _typical command_    read the model number and buffer size 
        self.cmd_stx_b =  b'\x02'       # start of text
        self.cmd_0     = '01000'        # NODE:01 SubAddress:00 SID:0
        self.cmd       = '0503'         # MRC/SRC(MainRequestCode/SubRequestCode)  
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
            #print("connected to: " + self.serial_port.portstr)                       #CHG COM3 temporary,  CompoWay/F default baudrate is 38400bps 
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
        cmd_ASCII = self.cmd_0 + cmd + self.cmd_etx_b.decode()          # cmd in ASCII characters

        fcs = self.Compute_FCS( cmd_ASCII )                             # calculate cmd_ASCII XOR
        fcs_h = int(fcs,16)                                             #INS  change hex_string → integer
        bcc_b = fcs_h.to_bytes(1, byteorder='big')                      #INS  change integer    → bainary
        cmd_b = self.cmd_stx_b + cmd_ASCII.encode() + bcc_b
        
        self.Connect_Device()
        self.serial_port.write(cmd_b)
        time.sleep(0.05)                                        # Wait a minute (0.1s).    tried minimum wait time  ... about 0.05s

        #print("Receive from OMRON E5AC:")
        buf = self.serial_port.read()                           # read start of text         stx_b =  b'\x02' dummy read
        buf_full = self.serial_port.read_all()                  # b'01000005030000E5AC-TCX4A00D9\x03\x1c'                                          
        buf_full_ASCII = buf_full.decode()                      #  '01000005030000E5AC-TCX4A00D9  ' 
        buf_ASCII = buf_full_ASCII[10:]                         #   0123456789012345678901234567890
        self.serial_port.close()

        return buf_ASCII
    
    def Device_Info(self):  
        cmd       = '0503'         # read the model number and buffer size  MRC/SRC(MainRequestCode/SubRequestCode)
        buf_ASCII = self.Command_Response(cmd)          #0000E5AC-TCX4A00D9                                         
        str_ID = buf_ASCII[4:14]                        #0123456789012345678901234
        return str_ID
    
    def Device_Status(self):  
        cmd       = '0601'         # read the operating status and error status MRC/SRC(MainRequestCode/SubRequestCode)
        buf_ASCII = self.Command_Response(cmd)          #00000100                     
        str_status = buf_ASCII[0:]                     #0123456789012345678901234
        return str_status

    def Set_Communication_Write_Enable(self, bool_manual ):        
        if bool_manual == True:
            cmd = '30050001'     # Communication Write Enable       # Operation Command MRC/SRC(MainRequestCode/SubRequestCode) & Command and fuction
        else:
            cmd = '30050000'     # Communication Write Disable     
        #print (cmd)
        str_response = self.Command_Response(cmd)       #0000                                  
        return str_response
        
    def Set_Manual_Mode(self, bool_mode ):        
        if bool_mode == True:
            cmd = '30050901'     # Manual Mode                       # Operation Command MRC/SRC(MainRequestCode/SubRequestCode) & Command and fuction
        else:
            cmd = '30050900'     # Auto Mode       
        #print (cmd)
        str_response = self.Command_Response(cmd)       #0000                                  
        return str_response
     
    def Execute_Process(self, bool_exec ):        
        if bool_exec == True:
            cmd = '30050100'     # Run                              # Operation Command MRC/SRC(MainRequestCode/SubRequestCode) & Command and fuction
        else:
            cmd = '30050101'     # Stop      
        #print (cmd)
        str_response = self.Command_Response(cmd)       #0000                                  
        return str_response
    
    def Get_Temp(self):  
        cmd       = '0101C00000000001'                      # read data MRC/SRC(MainRequestCode/SubRequestCode) & Command
        #            0123456789012345
        buf_ASCII = self.Command_Response(cmd)          #000000000018                                  
        temp_h = buf_ASCII[4:12]                        #0123456789012345678901234
        temp = int(temp_h,16)
        return temp

    def Set_Output_Value(self, mv ):                                #set Manual Output Value
        mv_int = int(mv*10)
        if mv_int < 0:
            mv_int = 0
        elif mv_int > 1000:
            mv_int = 1000
        mv_int_str   = format(mv_int, '08x')
        #print (mv_int_str)                                           # .upper() change Small Characters into Large Characters 
        cmd       = '0102C10024000001'  + mv_int_str.upper()          #  write data MRC/SRC(MainRequestCode/SubRequestCode) & Command 
        str_response = self.Command_Response(cmd)       #0000                                  
        return str_response
     
    def Get_Output_Value(self):  
        cmd       = '0101C10024000001'                      # read data MRC/SRC(MainRequestCode/SubRequestCode) & Command
        #            0123456789012345
        buf_ASCII = self.Command_Response(cmd)          #000000000064                                  
        manual_value_h = buf_ASCII[4:12]                #0123456789012345678901234
        manual_value = int(manual_value_h ,16) /10.0
        return manual_value
           
    def Get_General_Value(self, v_type_str, address_str ,):  
        cmd       = '0101' + v_type_str + address_str + '000001'        # read data MRC/SRC(MainRequestCode/SubRequestCode) & Command
        buf_ASCII = self.Command_Response(cmd)          #000000000018
        status_ASCII = buf_ASCII[:4] 
        value_ASCII  = buf_ASCII[4:12]                                  
        return status_ASCII,value_ASCII
         
if __name__ == '__main__':
    OMRON_E5AC = Application()

    # usage example
    # import OMRON_E5AC_module
    #         self.OMRON_E5AC   = OMRON_E5AC_module.Application()
    #         str_ID            = OMRON_E5AC.Device_Info() 
    
