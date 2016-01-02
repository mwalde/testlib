

class test_cfg:
    def __init__(self, write_to_radio = True,       # write board.conf to radio
                       prompt_user = True,          # display user prompts. False auto mode
                       use_LabJack = True,          # LabJack installed
                       use_database = True,         # write to database
                       use_csvlogs  = False,        # write csv log files
                       TxPowerTest = False,         # run TxPowerTest
                       PowerEVMTest = False,         # run power evm test
                       RxSenseTest = False,
                       RxSymEVM = False,
                       power = False,               # power or power range
                       freq  = False,               # frequency, freq list, or freq range
                       FPGA145 = False,
                       csv_logname = False,         # list csv log files to use
                       tx_freq_list = False,        # override the tx freq list
                       rx_freq_list = False         # override the rx freq list
                       ):
        self.write_to_radio = write_to_radio
        self.prompt_user = prompt_user
        self.use_LabJack = use_LabJack
        self.use_database = use_database
        self.use_csvlogs = use_csvlogs
        self.TxPowerTest = TxPowerTest
        self.PowerEVMTest = PowerEVMTest
        self.RxSenseTest = RxSenseTest
        self.RxSymEVM = RxSymEVM
        self.power = power
        self.freq = freq
        self.FPGA145 = FPGA145
        self.csv_logname = csv_logname
        self.tx_freq_list = tx_freq_list
        self.rx_freq_list = rx_freq_list
        
        