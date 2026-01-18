from gs_lora_config_class import * #LoraConfig

VERBOSE_MODE = True

MAX_CONFIG_SIZE = 10

class LoraConfigDb():
    def __init__(self, num_configs=2):
        if (VERBOSE_MODE):
            print(" ~ Constructing LoRa Config DB object")
        
        # Validate the input
        self.validateNumConfigsInput(num_configs)
        
        # Initialize Data Members 
        self.config_object_list = []
        self.config_id_hash_list = []
        self.default_config = LoraConfig(100)

        # Construct the Object list
        for i in range(1, num_configs+1):
            config = LoraConfig(i)

            # Append the config to the DB list
            self.config_object_list.append(config)
            self.config_id_hash_list.append(i)

        print(" -> self.config_id_hash_list is: " + str(self.config_id_hash_list))


    def validateNumConfigsInput(self, num_configs):
        assert(type(num_configs) == int)
        assert((0 < num_configs) and (num_configs <= MAX_CONFIG_SIZE))
        return

    def print(self):
        # This method prints the config objects 
        for config in self.config_object_list:
            config.print()
        return

    def printConfig(self, config_num):
        # This method prints the config object 
        self.config_object_list[config_num-1].print()
        return

    def setConfigIdNumber(self, config_num, id_num):
        index = self.getConfigNumIndex(config_num)
        self.config_object_list[index].id_num = id_num
        return

    def getConfigIdNumber(self, config_num):
        index = self.getConfigNumIndex(config_num)
        return self.config_object_list[index].id_num

    def setConfigFrequency(self, config_num, frequency):
        index = self.getConfigNumIndex(config_num)
        self.config_object_list[index].frequency = frequency
        return

    def getConfigFrequency(self, config_num):
        print(" - config_num is: " + str(config_num)) 
        index = self.getConfigNumIndex(config_num)
        print(" - index is: " + str(index))
        self.config_object_list[index].print()
        return self.config_object_list[index].frequency
    
    def setConfigBandwidth(self, config_num, bandwidth):
        index = self.getConfigNumIndex(config_num)
        self.config_object_list[index].bandwidth = bandwidth
        return

    def getConfigBandwidth(self, config_num):
        index = self.getConfigNumIndex(config_num)
        return self.config_object_list[index].bandwidth

    def setConfigSpreadFactor(self, config_num, spread_factor):
        index = self.getConfigNumIndex(config_num)
        self.config_object_list[index].spread_factor = spread_factor
        return

    def getConfigSpreadFactor(self, config_num):
        index = self.getConfigNumIndex(config_num)
        return self.config_object_list[index].spread_factor

    def setConfigCodingRate(self, config_num, coding_rate):
        index = self.getConfigNumIndex(config_num)
        self.config_object_list[index].coding_rate = coding_rate
        return

    def getConfigCodingRate(self, config_num):
        index = self.getConfigNumIndex(config_num)
        return self.config_object_list[index].coding_rate

    def setConfigOutputPower(self, config_num, output_power):
        index = self.getConfigNumIndex(config_num)
        self.config_object_list[index].output_power = output_power
        return

    def getConfigOutputPower(self, config_num):
        index = self.getConfigNumIndex(config_num)
        return self.config_object_list[index].output_power

    def setConfigCurrentLimit(self, config_num, current_limit):
        index = self.getConfigNumIndex(config_num)
        self.config_object_list[index].current_limit = current_limit
        return

    def getConfigCurrentLimit(self, config_num):
        index = self.getConfigNumIndex(config_num)
        return self.config_object_list[index].current_limit

    def setConfigPreambleLength(self, config_num, preamble_length):
        index = self.getConfigNumIndex(config_num)
        self.config_object_list[index].preamble_length = preamble_length
        return

    def getConfigPreambleLength(self, config_num):
        index = self.getConfigNumIndex(config_num)
        return self.config_object_list[index].preamble_length
   
    def setConfigGain(self, config_num, gain):
        index = self.getConfigNumIndex(config_num)
        self.config_object_list[index].gain = gain
        return

    def getConfigGain(self, config_num):
        index = self.getConfigNumIndex(config_num)
        return self.config_object_list[index].gain
    
    def getConfigNumIndex(self, config_num):
        if config_num in self.config_id_hash_list:
            return self.config_id_hash_list.index(config_num)
        else:
            return None # Done so that invokes error

    def pringtConfig(self, config_num):    
        index = self.getConfigNumIndex(config_num)
        self.config_object_list[index].print()
        return


    def getConfigDefaultFrequency(self):
        return self.default_config.getDefaultFrequency()

    def getConfigDefaultBandwidth(self):
        return self.default_config.getDefaultBandwidth()

    def getConfigDefaultSpreadFactor(self):
        return self.default_config.getDefaultSpreadFactor()

    def getConfigDefaultCodingRate(self):
        return self.default_config.getDefaultCodingRate()

    def getConfigDefaultOutputPower(self):
        return self.default_config.getDefaultOutputPower()

    def getConfigDefaultCurrentLimit(self):
        return self.default_config.getDefaultCurrentLimit()

    def getConfigDefaultPreambleLength(self):
        return self.default_config.getDefaultPreambleLength()

    def getConfigDefaultGain(self):
        return self.default_config.getDefaultGain()


if __name__ == '__main__':
    print("\n ~ Exercising LoRa Config DB Class ...")
    LC_Db = LoraConfigDb()

    # Test Initialized Mode
    print("\n ~ Testing Default Constructor ...")
    LC_Db.pringtConfig(1)

    assert(LC_Db.getConfigIdNumber(1) == 1)
    assert(LC_Db.getConfigFrequency(1) == DEFAULT_FREQUENCY_IN_HZ)
    assert(LC_Db.getConfigBandwidth(1) == DEFAULT_BANDWIDTH_IN_HZ)
    assert(LC_Db.getConfigSpreadFactor(1) == DEFAULT_SPREAD_FACTOR)
    assert(LC_Db.getConfigCodingRate(1) == DEFAULT_CODING_RATE)
    assert(LC_Db.getConfigOutputPower(1) == DEFAULT_OUTPUT_POWER_IN_DBM)
    assert(LC_Db.getConfigCurrentLimit(1) == DEFAULT_CURRENT_LIMIT_IN_MA)
    assert(LC_Db.getConfigPreambleLength(1) == DEFAULT_PREAMBLE_LENGTH)
    assert(LC_Db.getConfigGain(1) == DEFAULT_GAIN)

    id_num = 2
    LC_Db.setConfigIdNumber(1, id_num)
    assert(LC_Db.getConfigIdNumber(1) == id_num)

    frequency = 800000
    LC_Db.setConfigFrequency(1, frequency)
    assert(LC_Db.getConfigFrequency(1) == frequency)

    bandwidth = 7654
    LC_Db.setConfigBandwidth(1, bandwidth)
    assert(LC_Db.getConfigBandwidth(1) == bandwidth)

    spread_factor = 2
    LC_Db.setConfigSpreadFactor(1, spread_factor)
    assert(LC_Db.getConfigSpreadFactor(1) == spread_factor)

    coding_rate = 10
    LC_Db.setConfigCodingRate(1, coding_rate)
    assert(LC_Db.getConfigCodingRate(1) == coding_rate)

    output_power = 2
    LC_Db.setConfigOutputPower(1, output_power)
    assert(LC_Db.getConfigOutputPower(1) == output_power)
    
    current_limit = 75
    LC_Db.setConfigCurrentLimit(1, current_limit)
    assert(LC_Db.getConfigCurrentLimit(1) == current_limit)

    preamble_length = 8
    LC_Db.setConfigPreambleLength(1, preamble_length)
    assert(LC_Db.getConfigPreambleLength(1) == preamble_length)

    gain = 0
    LC_Db.setConfigGain(1, gain)
    assert(LC_Db.getConfigGain(1) == gain)

    

    print("\n ~ Exercising LoRa Config DB Class ...")
    LC_Db = LoraConfigDb(4)

    # Test Initialized Mode
    print("\n ~ Testing Default Constructor ...")
    LC_Db.pringtConfig(3)

    #print(LC_Db.getConfigDefaultFrequency())

    print(" ~ All Lora Config DB Tests: PASSED\n")
