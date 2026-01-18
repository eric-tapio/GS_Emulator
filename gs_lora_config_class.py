
MIN_ID_NUM = 1
MAX_ID_NUM = 100

VERBOSE_MODE = True

DEFAULT_FREQUENCY_IN_HZ = 434000000
DEFAULT_BANDWIDTH_IN_HZ = 125000
DEFAULT_SPREAD_FACTOR = 9
#DEFAULT_SYNC_WORD = 0x12
DEFAULT_CODING_RATE = 7
DEFAULT_OUTPUT_POWER_IN_DBM = -3 # where -3 is the lowest output power
DEFAULT_CURRENT_LIMIT_IN_MA = 80 # where 45 is the lowest current limit
DEFAULT_PREAMBLE_LENGTH = 8
DEFAULT_GAIN = 1 # Where 1 is the minimum gain

class LoraConfig():
    def __init__(self, id_num):
        if (VERBOSE_MODE):
            print(" ~ Constructing LoRa Config object w/ ID: " + str(id_num))
        
        # Validate the input
        self.validateIdInput(id_num)
        
        # Initialize Data Members 
        self.id_num = id_num

        # Populate the Database elements with default values
        self.frequency = DEFAULT_FREQUENCY_IN_HZ
        self.bandwidth = DEFAULT_BANDWIDTH_IN_HZ
        self.spread_factor = DEFAULT_SPREAD_FACTOR
        self.coding_rate = DEFAULT_CODING_RATE
        self.output_power = DEFAULT_OUTPUT_POWER_IN_DBM
        self.current_limit = DEFAULT_CURRENT_LIMIT_IN_MA
        self.preamble_length = DEFAULT_PREAMBLE_LENGTH
        self.gain = DEFAULT_GAIN


    def validateIdInput(self, id_num):
        assert(type(id_num) == int)
        assert((MIN_ID_NUM <= id_num) and (id_num <= MAX_ID_NUM))      
        return


    def print(self):
        # This method prints the objects data members 
        print(" ~ Printing LoRa Configuration ...")
        
        print("    ID Number: " + str(self.id_num))
        print("    Frequency in Hz: " + str(self.frequency))
        print("    Bandwidth Hz: " + str(self.bandwidth))
        print("    Spread Factor: " + str(self.spread_factor))
        print("    Coding Rate: " + str(self.coding_rate))
        print("    Output Power in Dbm: " + str(self.output_power))
        print("    Current Limit in mA: " + str(self.current_limit))
        print("    Preamble Length: " + str(self.preamble_length))
        print("    Gain: " + str(self.gain))
        print("")                                                 
        return


    def setIdNumber(self, id_num):
        self.id_num = id_num
        return

    def getIdNumber(self):
        return self.id_num

    def setFrequency(self, frequency):
        self.frequency = frequency
        return

    def getFrequency(self):
        return self.frequency

    def setBandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        return

    def getBandwidth(self):
        return self.bandwidth

    def setSpreadFactor(self, spread_factor):
        self.spread_factor = spread_factor
        return

    def getSpreadFactor(self):
        return self.spread_factor

    def setCodingRate(self, coding_rate):
        self.coding_rate = coding_rate
        return

    def getCodingRate(self):
        return self.coding_rate

    def setOutputPower(self, output_power):
        self.output_power = output_power
        return

    def getOutputPower(self):
        return self.output_power

    def setCurrentLimit(self, current_limit):
        self.current_limit = current_limit
        return

    def getCurrentLimit(self):
        return self.current_limit

    def setPreambleLength(self, preamble_length):
        self.preamble_length = preamble_length
        return

    def getPreambleLength(self):
        return self.preamble_length
   
    def setGain(self, gain):
        self.gain = gain
        return

    def getGain(self):
        return self.gain

    def getDefaultFrequency(self):
        return DEFAULT_FREQUENCY_IN_HZ

    def getDefaultBandwidth(self):
        return DEFAULT_BANDWIDTH_IN_HZ

    def getDefaultSpreadFactor(self):
        return DEFAULT_SPREAD_FACTOR

    def getDefaultCodingRate(self):
        return DEFAULT_CODING_RATE

    def getDefaultOutputPower(self):
        return DEFAULT_OUTPUT_POWER_IN_DBM

    def getDefaultCurrentLimit(self):
        return DEFAULT_CURRENT_LIMIT_IN_MA

    def getDefaultPreambleLength(self):
        return DEFAULT_PREAMBLE_LENGTH

    def getDefaultGain(self):
        return DEFAULT_GAIN




if __name__ == '__main__':
    print("\n ~ Exercising LoRa Config Class ...")
    id_num = 4
    LC = LoraConfig(id_num)

    # Test Constructor Defaults
    print("\n ~ Testing Default Constructor ...")
    LC.print()

    assert(LC.id_num == id_num)
    assert(LC.frequency == DEFAULT_FREQUENCY_IN_HZ)
    assert(LC.bandwidth == DEFAULT_BANDWIDTH_IN_HZ)
    assert(LC.spread_factor == DEFAULT_SPREAD_FACTOR)
    assert(LC.coding_rate == DEFAULT_CODING_RATE)
    assert(LC.output_power == DEFAULT_OUTPUT_POWER_IN_DBM)
    assert(LC.current_limit == DEFAULT_CURRENT_LIMIT_IN_MA)
    assert(LC.preamble_length == DEFAULT_PREAMBLE_LENGTH)
    assert(LC.gain == DEFAULT_GAIN)

    # Test Set/Get methods, eventhough all data members are public
    LC.output_power = 1000
    assert(LC.output_power == 1000)

    id_num = 2
    LC.setIdNumber(id_num)
    assert(LC.getIdNumber() == id_num)

    frequency = 800000
    LC.setFrequency(frequency)
    assert(LC.getFrequency() == frequency)

    bandwidth = 7654
    LC.setBandwidth(bandwidth)
    assert(LC.getBandwidth() == bandwidth)

    spread_factor = 2
    LC.setSpreadFactor(spread_factor)
    assert(LC.getSpreadFactor() == spread_factor)

    coding_rate = 10
    LC.setCodingRate(coding_rate)
    assert(LC.getCodingRate() == coding_rate)

    output_power = 2
    LC.setOutputPower(output_power)
    assert(LC.getOutputPower() == output_power)
    
    current_limit = 75
    LC.setCurrentLimit(current_limit)
    assert(LC.getCurrentLimit() == current_limit)

    preamble_length = 8
    LC.setPreambleLength(preamble_length)
    assert(LC.getPreambleLength() == preamble_length)

    gain = 0
    LC.setGain(gain)
    assert(LC.getGain() == gain)


    print(" ~ All Lora Config Tests: PASSED\n")

