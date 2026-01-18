#!/usr/bin/env python

# Import modules needed for websocket connectivity
import uvicorn
import socketio
import time # used for development only
import serial
import subprocess
import time
from datetime import datetime, timezone

from FileIO import *
from gs_lora_db_class import LoraConfigDb


RUN_GS_MODE = False
GS_ID_NUM = 99

SERIAL_TERMINATOR = '\r\n'
SERIAL_PORT_TIMEOUT_IN_SEC = 3
slimsat_id_num = 1


# Construct a Config DB object
#if (RUN_GS_MODE):
if (1):
    lora_config_db = LoraConfigDb()
    lora_default_db = LoraConfigDb(1)

# Make this a dropdown instead of an input value
ALLOWED_RADIO_BANDWITDTH_IN_KHZ_VALUES = [7800, 10400, 15600, 20800, 31250, 41700, 62500, 125000, 250000, 500000] 
MIN_RADIO_FREQUENCY_IN_HZ = 137 * 1e6
MAX_RADIO_FREQUENCY_IN_HZ = 1020 * 1e6
MIN_RADIO_BANDWIDTH_IN_HZ = 7.8 * 1e3
MAX_RADIO_BANDWIDTH_IN_HZ = 500 * 1e3
MIN_RADIO_SPREAD_FACTOR = 6
MAX_RADIO_SPREAD_FACTOR = 12
MIN_BEACON_PERIOD_IN_MS = 1000
MAX_BEACON_PERIOD_IN_MS = 1000000
MIN_BUS_MODE = 0
MAX_BUS_MODE = 2
MIN_PAYLOAD_MODE = 0
MAX_PAYLOAD_MODE = 2
MIN_BUS_DATA_RECORD_PERIOD_IN_MS = 0
MAX_BUS_DATA_RECORD_PERIOD_IN_MS = 1000000

MIN_BUS_SAFE_MODE_VOLTAGE_IN_MV = 3000 # 3.0V
MAX_BUS_SAFE_MODE_VOLTAGE_IN_MV = 4000 # 4.0V

MIN_PAYLOAD_OP_PERIOD_IN_MS = 0
MAX_PAYLOAD_OP_PERIOD_IN_MS = 1000000
MIN_BUS_EPOCH_TIME_IN_S = 0
MAX_BUS_EPOCH_TIME_IN_S = 1000000
MIN_NUM_PING_MEASUREMENTS = 0
MAX_NUM_PING_MEASUREMENTS = 20

MIN_RADIO_CODING_RATE = 4
MAX_RADIO_CODING_RATE = 8
MIN_RADIO_OUTPUT_POWER_IN_DBM = -3
MAX_RADIO_OUTPUT_POWER_IN_DBM = 17
MIN_RADIO_CURRENT_LIMIT_IN_MA = 45
MAX_RADIO_CURRENT_LIMIT_IN_MA = 240
MIN_RADIO_PREAMBLE_LENGTH = 6
MAX_RADIO_PREAMBLE_LENGTH = 65535
MIN_RADIO_GAIN = 1
MAX_RADIO_GAIN = 6

# Telemetry Parsing Parameters
RESPONSE_FRAGMENT_NUMBER_INDEX = 3
RESPONSE_CMD_VAL_INDEX = 4
RESPONSE_BUS_NUM_DATA_RECS_INDEX = RESPONSE_CMD_VAL_INDEX + 3
RESPONSE_PAYLOAD_NUM_DATA_RECS_INDEX = RESPONSE_BUS_NUM_DATA_RECS_INDEX + 1
GET_REC_REC_START_NUM_INDEX = 0
GET_REC_NUM_RECS_INDEX = 1


# Command IDs
PING_BUS_COMMAND_ID = 1
GET_BUS_DB_REGISTER_VALUES_COMMAND_ID = 2
GET_BUS_DATA_COMMAND_ID = 3
GET_PAYLOAD_DATA_COMMAND_ID = 4
GET_RADIO_FREQUENCY_COMMAND_ID = 5
SET_RADIO_FREQUENCY_COMMAND_ID = 6
GET_RADIO_BANDWIDTH_COMMAND_ID = 7
SET_RADIO_BANDWIDTH_COMMAND_ID = 8
GET_RADIO_SPREAD_FACTOR_COMMAND_ID = 9
SET_RADIO_SPREAD_FACTOR_COMMAND_ID = 10
GET_RADIO_CODING_RATE_COMMAND_ID = 11
SET_RADIO_CODING_RATE_COMMAND_ID = 12
GET_RADIO_OUTPUT_POWER_COMMAND_ID = 13
SET_RADIO_OUTPUT_POWER_COMMAND_ID = 14
GET_RADIO_CURRENT_LIMIT_COMMAND_ID = 15
SET_RADIO_CURRENT_LIMIT_COMMAND_ID = 16
GET_RADIO_PREAMBLE_LENGTH_COMMAND_ID = 17
SET_RADIO_PREAMBLE_LENGTH_COMMAND_ID = 18
GET_RADIO_GAIN_COMMAND_ID = 19
SET_RADIO_GAIN_COMMAND_ID = 20
GET_RADIO_FREQUENCY_ERROR_COMMAND_ID = 21
GET_RADIO_SNR_COMMAND_ID = 22
GET_RADIO_RSSI_COMMAND_ID = 23
GET_BEACON_PERIOD_COMMAND_ID = 24
SET_BEACON_PERIOD_COMMAND_ID = 25
GET_BUS_MODE_COMMAND_ID = 26
SET_BUS_MODE_COMMAND_ID = 27
GET_BUS_EPOCH_TIME_COMMAND_ID = 28
SET_BUS_EPOCH_TIME_COMMAND_ID = 29
GET_BUS_TIME_COMMAND_ID = 30
GET_BUS_SAFE_MODE_VOLTAGE_COMMAND_ID = 31
SET_BUS_SAFE_MODE_VOLTAGE_COMMAND_ID = 32
GET_BUS_DATA_RECORD_PERIOD_COMMAND_ID = 33
SET_BUS_DATA_RECORD_PERIOD_COMMAND_ID = 34
GET_PAYLOAD_OP_PERIOD_COMMAND_ID = 35
SET_PAYLOAD_OP_PERIOD_COMMAND_ID = 36
REBOOT_COMMAND_ID = 37
GET_FLASH_REGISTER_VALUE_COMMAND_ID = 38
SET_FLASH_REGISTER_VALUE_COMMAND_ID = 39
ERASE_FLASH_CHIP_MEMORY_COMMAND_ID = 40
ERASE_FLASH_BLOCK_MEMORY_COMMAND_ID = 41
ERASE_FLASH_SECTOR_MEMORY_COMMAND_ID = 42
ERASE_BUS_DATA_FLASH_BLOCKS_COMMAND_ID = 43
ERASE_PAYLOAD_DATA_FLASH_BLOCKS_COMMAND_ID = 44
GET_GPS_POSITION_COMMAND_ID = 45
CUTDOWN_BURN_WIRE_COMMAND_ID = 46
SLIMSAT_CMD_47 = 47
SLIMSAT_CMD_48 = 48
SLIMSAT_CMD_49 = 49

PAYLOAD_CMD_1 = 50 # Ping Payload
PAYLOAD_CMD_2 = 51 # Get Payload State
PAYLOAD_CMD_3 = 52 # Get Number Measurements to Take
PAYLOAD_CMD_4 = 53 # Set Number Measurements to Take
PAYLOAD_CMD_5 = 54 # Take Round of Measurements
PAYLOAD_CMD_6 = 55 # Get Raw Measurements
PAYLOAD_CMD_7 = 56 # Get Processed Measurements
PAYLOAD_CMD_8 = 57 # Print Measurements
PAYLOAD_CMD_9 = 58 # Not Used
PAYLOAD_CMD_10 = 59 # Not Used

VERBOSE_MODE = True

TX_RX_FILE_HEADER = "Date [yyyy-dd-mm],Time [HH:MM:SS.SS],Command"

TX_CMD_OUTPUT_DIR = "Cmd_Data_Files"
TX_CMD_CAPTURE_FILENAME = "Tx_Cmd_Capture.txt"
RX_CMD_CAPTURE_FILENAME = "Rx_Cmd_Capture.txt"


GUI_BACKGROUND_TASK_REFRESH_PERIOD_IN_SEC = 0.5

background_task_started = False
ser = serial.Serial()


txCmdFileIo = FileIO()
rxCmdFileIo = FileIO()
		
# Start the Async Server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=None, log_output=False)

app = socketio.ASGIApp(sio, static_files={
    '/': 'hsssi26_gs_gui_control_web_client.html',
    '/static': 'static',
})


async def backgroundTask():
    """Example of how to send server generated events to clients."""
    while True:
        await sio.sleep(GUI_BACKGROUND_TASK_REFRESH_PERIOD_IN_SEC)
        if (0):
            print(" - Server: Performing background task ...")

        await peek_for_rx_response()

        await sio.emit('updateTime', {'data': ''})


@sio.on('disconnect request')
async def disconnectRequest(sid):
    if (VERBOSE_MODE):
        print(" - Server: Disconnecting Client ...")
    await sio.disconnect(sid)

    if (VERBOSE_MODE):
        print(" - Server: Disconnected")


@sio.on('connect')
async def connect(sid, environ):
    if (1):   
        print(" - Server: Client connected")
        print("    sid is: " + str(sid))
        print("    environ[HTTP_USER_AGENT] is: " + str(environ["HTTP_USER_AGENT"]))

    global background_task_started
    if not background_task_started:
        sio.start_background_task(backgroundTask)
        background_task_started = True


@sio.on('disconnect')
def disconnect(sid):
    if (0):
        print(' - Server: Client disconnected')

    return


async def handleGuiSetCommand(msg):

    # Update the GUI Tx message
    await sio.emit('updateTransmittedMsg', {'data': msg})

    datetime_str = getCurrentDatetime()
    time_str = getTimeFromDatetime(datetime_str)
    time_msg_str = time_str + ' -> ' + msg + '\n'
    datetime_str_msg_str = datetime_str + ',' + msg
    
    await sio.emit('updateMessageLog', {'data': time_msg_str})

    # Write the cmd to the Tx log file
    writeStrToTxCmdFile(datetime_str_msg_str)
    
    # Transmit the message
    response_list = transceiveMessage(msg)
    print(response_list)
    
    # Update the GUI Rx message
    datetime_response_str = datetime_str
        
    for response in response_list:
        await sio.emit('updateReceivededMsg', {'data': response})

        datetime_str = getCurrentDatetime()
        time_str = getTimeFromDatetime(datetime_str)

        time_response_str = time_str + ' -> ' + response + '\n'
        print(" ~ time_response_str is: " + str(time_response_str))
        
        datetime_response_str += ',' + response

        await sio.emit('updateMessageLog', {'data': time_response_str})
    
    # Write the cmd to the Tx log file
    writeStrToRxCmdFile(datetime_str_msg_str)
    
    return



async def handleGuiGetCommand(event_name, cmd_id, response_val_index=-1, id_num=-1):

    # Construct the message
    msg = constructSlimSatMessage(cmd_id, -1, -1, id_num)

    print(" ~ constructSlimSatMessage is: " + str(msg))
    
    # Update the GUI Tx message
    await sio.emit('updateTransmittedMsg', {'data': msg})
    
    datetime_str = getCurrentDatetime()
    time_str = getTimeFromDatetime(datetime_str)
    time_msg_str = time_str + ' -> ' + msg + '\n'
    datetime_str_msg_str = datetime_str + ',' + msg
    
    await sio.emit('updateMessageLog', {'data': time_msg_str})

    # Write the cmd to the Tx log file
    writeStrToTxCmdFile(datetime_str_msg_str)
    
    # Transmit the message
    response_list = transceiveMessage(msg)
    print(response_list)
    
    # Update the GUI Rx message
    datetime_response_str = datetime_str
        
    for response in response_list:
        await sio.emit('updateReceivededMsg', {'data': response})

        datetime_str = getCurrentDatetime()
        time_str = getTimeFromDatetime(datetime_str)

        time_response_str = time_str + ' -> ' + response + '\n'
        print(" ~ time_response_str is: " + str(time_response_str))
        
        datetime_response_str += ',' + response

        await sio.emit('updateMessageLog', {'data': time_response_str})
    
    # Write the cmd to the Tx log file
    writeStrToRxCmdFile(datetime_str_msg_str)

    if (len(response_list) > 0):
        if (response_val_index == -1):
            # Then parse the response val from the response
            #response_val = getSlimSatMessageResponseVal(response)
            print(" ~ response_list is: " + str(response_list))
            print(" ~ response_list[0] is: " + str(response_list[0]))
            response_val = getSlimSatMessageResponseVal(response_list[0])
        else:
            # Parse the response value with the given index
            #response_val = getSlimSatMessageResponseVal(response, response_val_index)
            response_val = getSlimSatMessageResponseVal(response_list[0], response_val_index)

        await sio.emit(event_name, {'data': response_val})       
        return response_list[0]
    else:
        return ""
    

#S/C LoRa
@sio.on('setScFrequency')
async def setScFrequency(sid=None, msg={}):
    # setScFrequency button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScFrequency Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])


    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        frequency = int(msg["data"]);

        if ((frequency >= MIN_RADIO_FREQUENCY_IN_HZ) & (frequency <= MAX_RADIO_FREQUENCY_IN_HZ)):
            msg = constructSlimSatMessage(SET_RADIO_FREQUENCY_COMMAND_ID, frequency)

            await handleGuiSetCommand(msg)

            if (RUN_GS_MODE):
                await setGsFrequency(None, {"data": frequency})
                #msg = constructSlimSatMessage(SET_RADIO_FREQUENCY_COMMAND_ID, frequency, -1, GS_ID_NUM)    
                #await handleGuiSetCommand(msg)

        else:
            print(" ~ Ignoring invalid Frequency ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getScFrequency')
async def getScFrequency(sid=None):
    # getScFrequency button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScFrequency Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScFrequency', GET_RADIO_FREQUENCY_COMMAND_ID)

    return


@sio.on('setScBandwidth')
async def setScBandwidth(sid=None, msg={}):
    # setScBandwidth button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScBandwidth Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        bandwidth = int(msg["data"]);

        if ((bandwidth >= MIN_RADIO_BANDWIDTH_IN_HZ) & (bandwidth <= MAX_RADIO_BANDWIDTH_IN_HZ)):
            if (bandwidth in ALLOWED_RADIO_BANDWITDTH_IN_KHZ_VALUES):
                msg = constructSlimSatMessage(SET_RADIO_BANDWIDTH_COMMAND_ID, bandwidth)

                await handleGuiSetCommand(msg)

                if (RUN_GS_MODE):
                    await setGsBandwidth(None, {"data": bandwidth})
                    #msg = constructSlimSatMessage(SET_RADIO_BANDWIDTH_COMMAND_ID, bandwidth, -1, GS_ID_NUM)    
                    #await handleGuiSetCommand(msg)
                    
            else:
                print("\n ~ Ignoring invalid Bandwidth ...")
                print("\n ~ Valid Bandwidth Values are:")
                print(ALLOWED_RADIO_BANDWITDTH_IN_KHZ_VALUES)
        else:
            print(" ~ Ignoring invalid Bandwidth ...")

    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getScBandwidth')
async def getScBandwidth(sid=None):
    # getScBandwidth button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScBandwidth Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScBandwidth', GET_RADIO_BANDWIDTH_COMMAND_ID)
    
    return
    
    
@sio.on('setScSpreadFactor')
async def setScSpreadFactor(sid=None, msg={}):
    # setScSpreadFactor button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScSpreadFactor Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        spread_factor = int(msg["data"]);

        if ((spread_factor >= MIN_RADIO_SPREAD_FACTOR) & (spread_factor <= MAX_RADIO_SPREAD_FACTOR)):
            msg = constructSlimSatMessage(SET_RADIO_SPREAD_FACTOR_COMMAND_ID, spread_factor)

            await handleGuiSetCommand(msg)

            if (RUN_GS_MODE):
                await setGsSpreadFactor(None, {"data": spread_factor})
                #msg = constructSlimSatMessage(SET_RADIO_SPREAD_FACTOR_COMMAND_ID, spread_factor, -1, GS_ID_NUM)    
                #await handleGuiSetCommand(msg)
               
        else:
            print(" ~ Ignoring invalid Spread Factor ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getScSpreadFactor')
async def getScSpreadFactor(sid=None):
    # getScSpreadFactor button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScSpreadFactor Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScSpreadFactor', GET_RADIO_SPREAD_FACTOR_COMMAND_ID)
    
    return
    

@sio.on('setScCodingRate')
async def setScCodingRate(sid=None, msg={}):
    # setScCodingRate button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScCodingRate Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        coding_rate = int(msg["data"]);

        if ((coding_rate >= MIN_RADIO_CODING_RATE) & (coding_rate <= MAX_RADIO_CODING_RATE)):
            msg = constructSlimSatMessage(SET_RADIO_CODING_RATE_COMMAND_ID, coding_rate)

            await handleGuiSetCommand(msg)

            if (RUN_GS_MODE):
                await setGsCodingRate(None, {"data": coding_rate})
                #msg = constructSlimSatMessage(SET_RADIO_CODING_RATE_COMMAND_ID, coding_rate, -1, GS_ID_NUM)    
                #await handleGuiSetCommand(msg)
                
        else:
            print(" ~ Ignoring invalid Coding Rate ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getScCodingRate')
async def getScCodingRate(sid=None):
    # getScCodingRate button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScCodingRate Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScCodingRate', GET_RADIO_CODING_RATE_COMMAND_ID)
    
    return


@sio.on('setScOutputPower')
async def setScOutputPower(sid=None, msg={}):
    # setScOutputPower button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScOutputPower Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        output_power = int(msg["data"]);

        if ((output_power >= MIN_RADIO_OUTPUT_POWER_IN_DBM) & (output_power <= MAX_RADIO_OUTPUT_POWER_IN_DBM)):
            msg = constructSlimSatMessage(SET_RADIO_OUTPUT_POWER_COMMAND_ID, output_power)
                
            await handleGuiSetCommand(msg)

            if (RUN_GS_MODE):
                await setGsOutputPower(None, {"data": output_power})
                #msg = constructSlimSatMessage(SET_RADIO_OUTPUT_POWER_COMMAND_ID, output_power, -1, GS_ID_NUM)    
                #await handleGuiSetCommand(msg)
        
        else:
            print(" ~ Ignoring invalid Output Power ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getScOutputPower')
async def getScOutputPower(sid=None):
    # getScOutputPower button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScOutputPower Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScOutputPower', GET_RADIO_OUTPUT_POWER_COMMAND_ID)
    
    return


@sio.on('setScCurrentLimit')
async def setScCurrentLimit(sid=None, msg={}):
    # setScCurrentLimit button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScCurrentLimit Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        current_limit = int(msg["data"]);

        if ((current_limit >= MIN_RADIO_CURRENT_LIMIT_IN_MA) & (current_limit <= MAX_RADIO_CURRENT_LIMIT_IN_MA)):
            msg = constructSlimSatMessage(SET_RADIO_CURRENT_LIMIT_COMMAND_ID, current_limit)

            await handleGuiSetCommand(msg)

            if (RUN_GS_MODE):
                await setGsCurrentLimit(None, {"data": current_limit})
                #msg = constructSlimSatMessage(SET_RADIO_CURRENT_LIMIT_COMMAND_ID, current_limit, -1, GS_ID_NUM)    
                #await handleGuiSetCommand(msg)
                
        else:
            print(" ~ Ignoring invalid Current Limit ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getScCurrentLimit')
async def getScCurrentLimit(sid=None):
    # getScCurrentLimit button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScCurrentLimit Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScCurrentLimit', GET_RADIO_CURRENT_LIMIT_COMMAND_ID)
    
    return


@sio.on('setScPreambleLength')
async def setScPreambleLength(sid=None, msg={}):
    # setScPreambleLength button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScPreambleLength Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        preamble_length = int(msg["data"]);

        if ((preamble_length >= MIN_RADIO_PREAMBLE_LENGTH) & (preamble_length <= MAX_RADIO_PREAMBLE_LENGTH)):
            msg = constructSlimSatMessage(SET_RADIO_PREAMBLE_LENGTH_COMMAND_ID, preamble_length)

            await handleGuiSetCommand(msg)

            if (RUN_GS_MODE):
                await setGsPreambleLength(None, {"data": preamble_length})
                #msg = constructSlimSatMessage(SET_RADIO_PREAMBLE_LENGTH_COMMAND_ID, preamble_length, -1, GS_ID_NUM)    
                #await handleGuiSetCommand(msg)
                
        else:
            print(" ~ Ignoring invalid Preamble Length ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getScPreambleLength')
async def getScPreambleLength(sid=None):
    # getScPreambleLength button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScPreambleLength Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScPreambleLength', GET_RADIO_PREAMBLE_LENGTH_COMMAND_ID)
    
    return



@sio.on('getScFrequencyError')
async def getScFrequencyError(sid=None):
    # getScFrequencyError button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScFrequencyError Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScFrequencyError', GET_RADIO_FREQUENCY_ERROR_COMMAND_ID)
    
    return


@sio.on('setScGain')
async def setScGain(sid=None, msg={}):
    # setScGain button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScGain Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        gain = int(msg["data"]);

        if ((gain >= MIN_RADIO_GAIN) & (gain <= MAX_RADIO_GAIN)):
            msg = constructSlimSatMessage(SET_RADIO_GAIN_COMMAND_ID, gain)

            await handleGuiSetCommand(msg)

            if (RUN_GS_MODE):
                await setGsGain(None, {"data": gain})
                #msg = constructSlimSatMessage(SET_RADIO_GAIN_COMMAND_ID, gain, -1, GS_ID_NUM)    
                #await handleGuiSetCommand(msg)
                
        else:
            print(" ~ Ignoring invalid Gain ...")
    else:
        print(" ~ Ignoring invalid input ...")

    return


@sio.on('getScGain')
async def getScGain(sid=None):
    # getScGain button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScGain Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScGain', GET_RADIO_GAIN_COMMAND_ID)
    
    return


@sio.on('getScSnr')
async def getScSnr(sid=None):
    # getScSnr button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScSnr Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScSnr', GET_RADIO_SNR_COMMAND_ID)
    
    return


@sio.on('getScRssi')
async def getScRssi(sid=None):
    # getScRssi button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScRssi Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScRssi', GET_RADIO_RSSI_COMMAND_ID)
        
    return



#GS LoRa
@sio.on('setGsFrequency')
async def setGsFrequency(sid=None, msg={}):
    # setGsFrequency button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setGsFrequency Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])


    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        frequency = int(msg["data"]);

        if ((frequency >= MIN_RADIO_FREQUENCY_IN_HZ) & (frequency <= MAX_RADIO_FREQUENCY_IN_HZ)):
            msg = constructSlimSatMessage(SET_RADIO_FREQUENCY_COMMAND_ID, frequency, -1, GS_ID_NUM)

            await handleGuiSetCommand(msg)

            # Then update the GS config for the Sat ID num
            lora_config_db.setConfigFrequency(slimsat_id_num, frequency)

        else:
            print(" ~ Ignoring invalid Frequency ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getGsFrequency')
async def getGsFrequency(sid=None):
    # getGsFrequency button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getGsFrequency Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateGsFrequency', GET_RADIO_FREQUENCY_COMMAND_ID, -1, GS_ID_NUM) 

    return


@sio.on('setGsBandwidth')
async def setGsBandwidth(sid=None, msg={}):
    # setGsBandwidth button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setGsBandwidth Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        bandwidth = int(msg["data"]);

        if ((bandwidth >= MIN_RADIO_BANDWIDTH_IN_HZ) & (bandwidth <= MAX_RADIO_BANDWIDTH_IN_HZ)):
            if (bandwidth in ALLOWED_RADIO_BANDWITDTH_IN_KHZ_VALUES):
                msg = constructSlimSatMessage(SET_RADIO_BANDWIDTH_COMMAND_ID, bandwidth, -1, GS_ID_NUM)

                await handleGuiSetCommand(msg)
                
                # Then update the GS config for the Sat ID num
                lora_config_db.setConfigBandwidth(slimsat_id_num, bandwidth)
            
            else:
                print("\n ~ Ignoring invalid Bandwidth ...")
                print("\n ~ Valid Bandwidth Values are:")
                print(ALLOWED_RADIO_BANDWITDTH_IN_KHZ_VALUES)
        else:
            print(" ~ Ignoring invalid Bandwidth ...")

    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getGsBandwidth')
async def getGsBandwidth(sid=None):
    # getGsBandwidth button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getGsBandwidth Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateGsBandwidth', GET_RADIO_BANDWIDTH_COMMAND_ID, -1, GS_ID_NUM)
    
    return
    
    
@sio.on('setGsSpreadFactor')
async def setGsSpreadFactor(sid=None, msg={}):
    # setGsSpreadFactor button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setGsSpreadFactor Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        spread_factor = int(msg["data"]);

        if ((spread_factor >= MIN_RADIO_SPREAD_FACTOR) & (spread_factor <= MAX_RADIO_SPREAD_FACTOR)):
            msg = constructSlimSatMessage(SET_RADIO_SPREAD_FACTOR_COMMAND_ID, spread_factor, -1, GS_ID_NUM) 

            await handleGuiSetCommand(msg)

            # Then update the GS config for the Sat ID num
            lora_config_db.setConfigSpreadFactor(slimsat_id_num, spread_factor)
            
        else:
            print(" ~ Ignoring invalid Spread Factor ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getGsSpreadFactor')
async def getGsSpreadFactor(sid=None):
    # getGsSpreadFactor button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getGsSpreadFactor Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateGsSpreadFactor', GET_RADIO_SPREAD_FACTOR_COMMAND_ID, -1, GS_ID_NUM)
    
    return
    

@sio.on('setGsCodingRate')
async def setGsCodingRate(sid=None, msg={}):
    # setGsCodingRate button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setGsCodingRate Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        coding_rate = int(msg["data"]);

        if ((coding_rate >= MIN_RADIO_CODING_RATE) & (coding_rate <= MAX_RADIO_CODING_RATE)):
            msg = constructSlimSatMessage(SET_RADIO_CODING_RATE_COMMAND_ID, coding_rate, -1, GS_ID_NUM)

            await handleGuiSetCommand(msg)

            # Then update the GS config for the Sat ID num
            lora_config_db.setConfigCodingRate(slimsat_id_num, coding_rate)
                
        else:
            print(" ~ Ignoring invalid Coding Rate ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getGsCodingRate')
async def getGsCodingRate(sid=None):
    # getGsCodingRate button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getGsCodingRate Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateGsCodingRate', GET_RADIO_CODING_RATE_COMMAND_ID, -1, GS_ID_NUM)
    
    return


@sio.on('setGsOutputPower')
async def setGsOutputPower(sid=None, msg={}):
    # setGsOutputPower button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setGsOutputPower Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        output_power = int(msg["data"]);

        if ((output_power >= MIN_RADIO_OUTPUT_POWER_IN_DBM) & (output_power <= MAX_RADIO_OUTPUT_POWER_IN_DBM)):
            msg = constructSlimSatMessage(SET_RADIO_OUTPUT_POWER_COMMAND_ID, output_power, -1, GS_ID_NUM)
                
            await handleGuiSetCommand(msg)

            # Then update the GS config for the Sat ID num
            lora_config_db.setConfigOutputPower(slimsat_id_num, output_power)
            
        else:
            print(" ~ Ignoring invalid Output Power ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getGsOutputPower')
async def getGsOutputPower(sid=None):
    # getGsOutputPower button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getGsOutputPower Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateGsOutputPower', GET_RADIO_OUTPUT_POWER_COMMAND_ID, -1, GS_ID_NUM)
    
    return


@sio.on('setGsCurrentLimit')
async def setGsCurrentLimit(sid=None, msg={}):
    # setGsCurrentLimit button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setGsCurrentLimit Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        current_limit = int(msg["data"]);

        if ((current_limit >= MIN_RADIO_CURRENT_LIMIT_IN_MA) & (current_limit <= MAX_RADIO_CURRENT_LIMIT_IN_MA)):
            msg = constructSlimSatMessage(SET_RADIO_CURRENT_LIMIT_COMMAND_ID, current_limit, -1, GS_ID_NUM)  

            await handleGuiSetCommand(msg)

            # Then update the GS config for the Sat ID num
            lora_config_db.setConfigCurrentLimit(slimsat_id_num, current_limit)
                
        else:
            print(" ~ Ignoring invalid Current Limit ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getGsCurrentLimit')
async def getGsCurrentLimit(sid=None):
    # getGsCurrentLimit button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getGsCurrentLimit Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateGsCurrentLimit', GET_RADIO_CURRENT_LIMIT_COMMAND_ID, -1, GS_ID_NUM)
    
    return


@sio.on('setGsPreambleLength')
async def setGsPreambleLength(sid=None, msg={}):
    # setGsPreambleLength button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setGsPreambleLength Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        preamble_length = int(msg["data"]);

        if ((preamble_length >= MIN_RADIO_PREAMBLE_LENGTH) & (preamble_length <= MAX_RADIO_PREAMBLE_LENGTH)):
            msg = constructSlimSatMessage(SET_RADIO_PREAMBLE_LENGTH_COMMAND_ID, preamble_length, -1, GS_ID_NUM)

            await handleGuiSetCommand(msg)

            # Then update the GS config for the Sat ID num
            lora_config_db.setConfigPreambleLength(slimsat_id_num, preamble_length)
                
        else:
            print(" ~ Ignoring invalid Preamble Length ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getGsPreambleLength')
async def getGsPreambleLength(sid=None):
    # getGsPreambleLength button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getGsPreambleLength Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateGsPreambleLength', GET_RADIO_PREAMBLE_LENGTH_COMMAND_ID, -1, GS_ID_NUM)
    
    return



@sio.on('getGsFrequencyError')
async def getGsFrequencyError(sid=None):
    # getGsFrequencyError button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getGsFrequencyError Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateGsFrequencyError', GET_RADIO_FREQUENCY_ERROR_COMMAND_ID, -1, GS_ID_NUM)
    
    return


@sio.on('setGsGain')
async def setGsGain(sid=None, msg={}):
    # setGsGain button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setGsGain Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        gain = int(msg["data"]);

        if ((gain >= MIN_RADIO_GAIN) & (gain <= MAX_RADIO_GAIN)):
            msg = constructSlimSatMessage(SET_RADIO_GAIN_COMMAND_ID, gain, -1, GS_ID_NUM) 

            await handleGuiSetCommand(msg)

            # Then update the GS config for the Sat ID num
            lora_config_db.setConfigGain(slimsat_id_num, gain)

        else:
            print(" ~ Ignoring invalid Gain ...")
    else:
        print(" ~ Ignoring invalid input ...")

    return


@sio.on('getGsGain')
async def getGsGain(sid=None):
    # getGsGain button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getGsGain Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateGsGain', GET_RADIO_GAIN_COMMAND_ID, -1, GS_ID_NUM)
    
    return


@sio.on('getGsSnr')
async def getGsSnr(sid=None):
    # getGsSnr button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getGsSnr Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateGsSnr', GET_RADIO_SNR_COMMAND_ID, -1, GS_ID_NUM)
    
    return


@sio.on('getGsRssi')
async def getGsRssi(sid=None):
    # getGsRssi button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getGsRssi Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateGsRssi', GET_RADIO_RSSI_COMMAND_ID, -1, GS_ID_NUM)
        
    return


@sio.on('getScPing')
async def getScPing(sid):
    # getScPing button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScPing Button Asserted.  Handling ...")

    msg = constructSlimSatMessage(PING_BUS_COMMAND_ID)

    await handleGuiSetCommand(msg)

    return


@sio.on('getScDbRegisterValues')
async def getScDbRegisterValues(sid):
    # getScDbRegisterValues button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScDbRegisterValues Button Asserted.  Handling ...")

    response = await handleGuiGetCommand('updateNumScBusDataRecs', GET_BUS_DB_REGISTER_VALUES_COMMAND_ID, RESPONSE_BUS_NUM_DATA_RECS_INDEX)

    print(" ~ response is: " + str(response))
    
    # Update the Number of Pl Rec Numbers
    await updateNumPlBusDataRecs(response)

    return


async def updateNumPlBusDataRecs(response):
    # Parse the response value with the given index
    response_val = getSlimSatMessageResponseVal(response, RESPONSE_PAYLOAD_NUM_DATA_RECS_INDEX)

    await sio.emit('updateNumPlBusDataRecs', {'data': response_val})
        
    return


@sio.on('getScDataRecords')
async def getScDataRecords(sid=None, msg={}):
    # getScDataRecords button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScDataRecords Button Asserted.  Handling ...")

    # Validate the input
    cmd_arg_list = getCmdArgsFromListInputMsgData(msg["data"])

    print(" ~ len(cmd_arg_list) is: " + str(len(cmd_arg_list)))
    print(" ~ cmd_arg_list is: " + str(cmd_arg_list))

    cmd_val = cmd_arg_list[GET_REC_REC_START_NUM_INDEX]
    optnl_cmd_arg = cmd_arg_list[GET_REC_NUM_RECS_INDEX]

    print(" ~ cmd_val is: " + str(cmd_val))
    print(" ~ optnl_cmd_arg is: " + str(optnl_cmd_arg))
        
    # Validate the input
    msg = constructSlimSatMessage(GET_BUS_DATA_COMMAND_ID, cmd_val, optnl_cmd_arg)

    await handleGuiSetCommand(msg)
 
    return


@sio.on('getPlDataRecords')
async def getPlDataRecords(sid=None, msg={}):
    # getPlDataRecords button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getPlDataRecords Button Asserted.  Handling ...")

    # Validate the input
    cmd_arg_list = getCmdArgsFromListInputMsgData(msg["data"])

    print(" ~ len(cmd_arg_list) is: " + str(len(cmd_arg_list)))
    print(" ~ cmd_arg_list is: " + str(cmd_arg_list))

    cmd_val = cmd_arg_list[GET_REC_REC_START_NUM_INDEX]
    optnl_cmd_arg = cmd_arg_list[GET_REC_NUM_RECS_INDEX]

    print(" ~ cmd_val is: " + str(cmd_val))
    print(" ~ optnl_cmd_arg is: " + str(optnl_cmd_arg))
        
    # Validate the input
    msg = constructSlimSatMessage(GET_PAYLOAD_DATA_COMMAND_ID, cmd_val, optnl_cmd_arg)

    await handleGuiSetCommand(msg)
 
    return


@sio.on('setScBeaconPeriod')
async def setScBeaconPeriod(sid=None, msg={}):
    # setScBeaconPeriod button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScBeaconPeriod Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        beacon_period = int(msg["data"]);

        if ((beacon_period >= MIN_BEACON_PERIOD_IN_MS) & (beacon_period <= MAX_BEACON_PERIOD_IN_MS)):
            msg = constructSlimSatMessage(SET_BEACON_PERIOD_COMMAND_ID, beacon_period)

            await handleGuiSetCommand(msg)
        
        else:
            print(" ~ Ignoring invalid Beacon Period ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getScBeaconPeriod')
async def getScBeaconPeriod(sid=None):
    # getScBeaconPeriod button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScBeaconPeriod Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScBeaconPeriod', GET_BEACON_PERIOD_COMMAND_ID)
        
    return


@sio.on('setScBusMode')
async def setScBusMode(sid=None, msg={}):
    # setScBusMode button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScBusMode Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        sc_bus_mode = int(msg["data"]);

        if ((sc_bus_mode >= MIN_BUS_MODE) & (sc_bus_mode <= MAX_BUS_MODE)):
            msg = constructSlimSatMessage(SET_BUS_MODE_COMMAND_ID, sc_bus_mode)

            await handleGuiSetCommand(msg)
        
        else:
            print(" ~ Ignoring invalid SC Bus Mode ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getScBusMode')
async def getScBusMode(sid=None):
    # getScBusMode button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScBusMode Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScBusMode', GET_BUS_MODE_COMMAND_ID)
    
    return


@sio.on('setScBusEpoch')
async def setScBusEpoch(sid=None, msg={}):
    # setScBusEpoch button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScBusEpoch Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the inputSET_BUS_SAFE_MODE_VOLTAGE_COMMAND_ID
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        epoch_time = int(msg["data"]);

        if ((epoch_time >= MIN_BUS_EPOCH_TIME_IN_S) & (epoch_time <= MAX_BUS_EPOCH_TIME_IN_S)):
            msg = constructSlimSatMessage(SET_BUS_EPOCH_TIME_COMMAND_ID, epoch_time)

            await handleGuiSetCommand(msg)
        
        else:
            print(" ~ Ignoring invalid SC Bus Epoch Time ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getScBusEpoch')
async def getScBusEpoch(sid=None):
    # getScBusEpoch button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScBusEpoch Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScBusEpoch', GET_BUS_EPOCH_TIME_COMMAND_ID)
    
    return


@sio.on('getScBusTime')
async def getScBusTime(sid=None):
    # getScBusTime button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScBusTime Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScBusTime', GET_BUS_TIME_COMMAND_ID)

    return


@sio.on('getScBusData')
async def getScBusData(sid=None):
    # getScBusData button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScBusData Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScBusData', GET_BUS_DATA_COMMAND_ID)
    
    return


@sio.on('setScBusSafeModeVoltage')
async def setScBusSafeModeVoltage(sid=None, msg={}):
    # setScBusSafeModeVoltage button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScBusSafeModeVoltage Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        voltage_in_mv = int(msg["data"]);

        if ((voltage_in_mv >= MIN_BUS_SAFE_MODE_VOLTAGE_IN_MV) & (voltage_in_mv <= MAX_BUS_SAFE_MODE_VOLTAGE_IN_MV)):
            msg = constructSlimSatMessage(SET_BUS_SAFE_MODE_VOLTAGE_COMMAND_ID, voltage_in_mv)

            await handleGuiSetCommand(msg)
        
        else:
            print(" ~ Ignoring invalid Bus Safe-Mode Voltage ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getScBusSafeModeVoltage')
async def getScBusSafeModeVoltage(sid=None):
    # getScBusSafeModeVoltage button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScBusSafeModeVoltage Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScBusSafeModeVoltage', GET_BUS_SAFE_MODE_VOLTAGE_COMMAND_ID)

    return


@sio.on('setScBusDataRecordPeriod')
async def setScBusDataRecordPeriod(sid=None, msg={}):
    # setScBusDataRecordPeriod button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScBusDataRecordPeriod Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        record_period = int(msg["data"]);

        if ((record_period >= MIN_BUS_DATA_RECORD_PERIOD_IN_MS) & (record_period <= MAX_BUS_DATA_RECORD_PERIOD_IN_MS)):
            msg = constructSlimSatMessage(SET_BUS_DATA_RECORD_PERIOD_COMMAND_ID, record_period)

            await handleGuiSetCommand(msg)
        
        else:
            print(" ~ Ignoring invalid Bus Record Period ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return


@sio.on('getScBusDataRecordPeriod')
async def getScBusDataRecordPeriod(sid=None):
    # getScBusDataRecordPeriod button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScBusDataRecordPeriod Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScBusDataRecordPeriod', GET_BUS_DATA_RECORD_PERIOD_COMMAND_ID)

    return


@sio.on('setScPayloadOpPeriod')
async def setScPayloadOpPeriod(sid=None, msg={}):
    # setScPayloadOpPeriod button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setScPayloadOpPeriod Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        payload_op_period = int(msg["data"]);

        if ((payload_op_period >= MIN_PAYLOAD_OP_PERIOD_IN_MS) & (payload_op_period <= MAX_PAYLOAD_OP_PERIOD_IN_MS)):
            msg = constructSlimSatMessage(SET_PAYLOAD_OP_PERIOD_COMMAND_ID, payload_op_period)

            await handleGuiSetCommand(msg)
        
        else:
            print(" ~ Ignoring invalid Payload Op Period ...")
    else:
        print(" ~ Ignoring invalid input ...")
        
    return



@sio.on('getScPayloadOpPeriod')
async def getScPayloadOpPeriod(sid=None):
    # SgetScPayloadOpPeriod button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScPayloadOpPeriod Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScPayloadOpPeriod', GET_PAYLOAD_OP_PERIOD_COMMAND_ID)

    return


@sio.on('getScGpsPosition')
async def getScGpsPosition(sid=None):
    # getScGpsPosition button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScGpsPosition Button Asserted.  Handling ...")

    msg = constructSlimSatMessage(GET_GPS_POSITION_COMMAND_ID)

    await handleGuiSetCommand(msg)

    return


@sio.on('performScCutdown')
async def performScCutdown(sid=None):
    # performScCutdown button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ performScCutdown Button Asserted.  Handling ...")

    msg = constructSlimSatMessage(CUTDOWN_BURN_WIRE_COMMAND_ID)

    await handleGuiSetCommand(msg)
        
    return


@sio.on('performScReboot')
async def performScReboot(sid=None):
    # performScReboot button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ performScReboot Button Asserted.  Handling ...")

    msg = constructSlimSatMessage(REBOOT_COMMAND_ID)

    await handleGuiSetCommand(msg)
    
    return


@sio.on('performScFlashChipErase')
async def performScFlashChipErase(sid=None):
    # performScFlashChipErase button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ performScFlashChipErase Button Asserted.  Handling ...")

    msg = constructSlimSatMessage(ERASE_FLASH_CHIP_MEMORY_COMMAND_ID)

    await handleGuiSetCommand(msg)
    
    return


@sio.on('getAllScTelemetry')
async def getAllScTelemetry(sid):
    # get All SC Bus Telemetry
    
    if (VERBOSE_MODE):
        print(" ~ getAllScTelemetry Button Asserted.  Handling ...")

    await getScFrequency()
    await getScBandwidth()
    await getScSpreadFactor()
    await getScCodingRate()
    await getScOutputPower()
    await getScCurrentLimit()
    await getScPreambleLength()
    await getScGain()
    await getScFrequencyError()
    await getScSnr()
    await getScRssi()

    await getScBeaconPeriod()
    await getScBusMode()
    await getScBusEpoch()
    await getScBusTime()
    await getScPayloadOpPeriod()
    await getScBusSafeModeVoltage()
    await getScBusDataRecordPeriod()

    return



@sio.on('getGsAllLoraTelemetry')
async def getGsAllLoraTelemetry(sid=None):
    # get All GS Lora Telemetry
    
    if (VERBOSE_MODE):
        print(" ~ getGsAllLoraTelemetry Button Asserted.  Handling ...")

    await getGsFrequency()
    await getGsBandwidth()
    await getGsSpreadFactor()
    await getGsCodingRate()
    await getGsOutputPower()
    await getGsCurrentLimit()
    await getGsPreambleLength()
    await getGsGain()
    await getGsFrequencyError()
    await getGsSnr()
    await getGsRssi()
    
    return


@sio.on('setGsAllLoraDefaults')
async def setGsAllLoraDefaults(sid=None):
    # get All GS Lora Paramaters to Default Values
    
    if (VERBOSE_MODE):
        print(" ~ setGsAllLoraDefaultParamaters Button Asserted.  Handling ...")

    default_frequency = lora_default_db.getConfigDefaultFrequency()
    default_bandwitdth = lora_default_db.getConfigDefaultBandwidth()
    default_spread_factor = lora_default_db.getConfigDefaultSpreadFactor()
    default_codig_rate = lora_default_db.getConfigDefaultCodingRate()
    default_output_power = lora_default_db.getConfigDefaultOutputPower()
    default_current_limit = lora_default_db.getConfigDefaultCurrentLimit()
    print(" ~ default_current_limit is: " + str(default_current_limit))
    default_preamble_length = lora_default_db.getConfigDefaultPreambleLength()
    default_gain = lora_default_db.getConfigDefaultGain()
    
    await setGsFrequency(None, {"data": default_frequency})
    await setGsBandwidth(None, {"data": default_bandwitdth})
    await setGsSpreadFactor(None, {"data": default_spread_factor})
    await setGsCodingRate(None, {"data": default_codig_rate})
    await setGsOutputPower(None, {"data": default_output_power})
    await setGsCurrentLimit(None, {"data": default_current_limit})
    await setGsPreambleLength(None, {"data": default_preamble_length})
    await setGsGain(None, {"data": default_gain})

    return


async def updateGsAllLoraParameters():
    if (VERBOSE_MODE):
        print(" ~ Updating Gs All LoRa Parameters ...")
        print("     SlimSat ID is now: " + str(slimsat_id_num))
        
    frequency = lora_config_db.getConfigFrequency(slimsat_id_num)
    bandwitdth = lora_config_db.getConfigBandwidth(slimsat_id_num)
    spread_factor = lora_config_db.getConfigSpreadFactor(slimsat_id_num)
    codig_rate = lora_config_db.getConfigCodingRate(slimsat_id_num)
    output_power = lora_config_db.getConfigOutputPower(slimsat_id_num)
    current_limit = lora_config_db.getConfigCurrentLimit(slimsat_id_num)
    preamble_length = lora_config_db.getConfigPreambleLength(slimsat_id_num)
    gain = lora_config_db.getConfigGain(slimsat_id_num)
    
    await setGsFrequency(None, {"data": frequency})
    await setGsBandwidth(None, {"data": bandwitdth})
    await setGsSpreadFactor(None, {"data": spread_factor})
    await setGsCodingRate(None, {"data": codig_rate})
    await setGsOutputPower(None, {"data": output_power})
    await setGsCurrentLimit(None, {"data": current_limit})
    await setGsPreambleLength(None, {"data": preamble_length})
    await setGsGain(None, {"data": gain})

    return


@sio.on('getScPayloadMode')
async def getScPayloadMode(sid):
    # getScPayloadMode button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScPayloadMode Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScPayloadMode', GET_PAYLOAD_MODE_COMMAND_ID)
        
    return


@sio.on('getScPayloadData')
async def getScPayloadData(sid):
    # getScPayloadData button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getScPayloadData Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScPayloadData', GET_PAYLOAD_DATA_COMMAND_ID)
    
    return


@sio.on('plPingPayload')
async def plPingPayload(sid):
    # plPingPayload button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ plPingPayload Button Asserted.  Handling ...")

    await handleGuiGetCommand('updateScPayloadData', PAYLOAD_CMD_1)
    
    return


@sio.on('setPlNumberOfMeas')
async def setPlNumberOfMeas(sid=None, msg={}):
    # setPlNumberOfMeas button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ setPlNumberOfMeas Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])

    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        num_ping_measurements = int(msg["data"]);

        if ((num_ping_measurements >= MIN_NUM_PING_MEASUREMENTS) & (num_ping_measurements <= MAX_NUM_PING_MEASUREMENTS)):
            msg = constructSlimSatMessage(PAYLOAD_CMD_4, num_ping_measurements)

            await handleGuiSetCommand(msg)
    
        else:
            print(" ~ Ignoring invalid Number Payload Ping Measurements ...")
    else:
        print(" ~ Ignoring invalid input ...")

    return



@sio.on('setScNumber')
async def setScNumber(sid, msg):
    # setScNumber button asserted.
    global slimsat_id_num
    
    if (VERBOSE_MODE):
        print(" ~ setScNumber Button Asserted.  Handling ...")
        print("     Msg is: ")
        print(msg["data"])
        
    # Validate the input
    input_is_valid = integerInputMsgDataIsValid(msg["data"])

    if (input_is_valid):
        # Set the slimsat number
        slimsat_id_num = int(msg["data"]);
        print(" ~ Slimsat id num is: " + str(slimsat_id_num))

        # Send all LoRa commands to the GS to set the config based on the SC Num
        await updateGsAllLoraParameters()
        await getGsAllLoraTelemetry()
        
    else:
        print(" ~ Ignoring invalid input ...")

    return


def integerInputMsgDataIsValid(msg_data):
    # This method validates input provided, which is exptected to be an integer, such as that by a text box

    try:
        integer_input = int(msg_data)
        return True
            
    except ValueError:
        return False


def getCmdArgsFromListInputMsgData(msg_data):

    assert(type(msg_data) == list)

    cmd_arg_list = []
    
    try:
        for data in msg_data:
            if (integerInputMsgDataIsValid(data)):
                # Then append the value to the cmd arg list
                cmd_arg_list.append(int(data))
            elif (len(data) == 0):
                # Then append -1 to the cmd arg list since it represents an empty string
                cmd_arg_list.append(-1)
            else:
                print(" ~ Unhandled case in getCmdArgsFromListInputMsgData encountered!")

        return cmd_arg_list
    
    except ValueError:
        return []   


@sio.on('getPlNumberOfMeas')
async def getPlNumberOfMeas(sid):
    # getPlNumberOfMeas button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getPlNumberOfMeas Button Asserted.  Handling ...")

    await handleGuiGetCommand('updatePlNumberOfMeas', PAYLOAD_CMD_3)
    
    return


@sio.on('takePlRoundOfMeas')
async def takePlRoundOfMeas(sid):
    # takePlRoundOfMeas button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ takePlRoundOfMeas Button Asserted.  Handling ...")

    await sio.emit('updateActionOutputMsg', {'data': "Success"})
    await sio.emit('updateTransmittedMsg', {'data': "$SomeTxMsg*AB"})
    await sio.emit('updateReceivededMsg', {'data': "$TheRxdMsg*AB"})
    await sio.emit('updateReceivededPayloadResponse', {'data': "0,1,2,3"})
    
    return


@sio.on('getPlRawMeas')
async def getPlRawMeas(sid):
    # getPlRawMeas button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getPlRawMeas Button Asserted.  Handling ...")

    await sio.emit('updateActionOutputMsg', {'data': "More Success"})
    await sio.emit('updateTransmittedMsg', {'data': "$SomeOtherTxMsg*CD"})
    await sio.emit('updateReceivededMsg', {'data': "$TheNextRxdMsg*CD"})
    await sio.emit('updateReceivededPayloadResponse', {'data': "4,5,6,7"})
            
    return   


@sio.on('getPlProcessedMeas')
async def getPlProcessedMeas(sid):
    # getPlProcessedMeas button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getPlProcessedMeas Button Asserted.  Handling ...")

    await sio.emit('updateActionOutputMsg', {'data': "Maybe Success"})
    await sio.emit('updateTransmittedMsg', {'data': "$SomeMoreTxMsg*EF"})
    await sio.emit('updateReceivededMsg', {'data': "$RxdMsg*EF"})
    await sio.emit('updateReceivededPayloadResponse', {'data': "8,5,19"})
    
    return


@sio.on('getPlTbd1')
async def getPlTbd1(sid):
    # getPlTbd1 button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getPlTbd1 Button Asserted.  Handling ...")

    await sio.emit('updateActionOutputMsg', {'data': "TBD1 Success"})
    await sio.emit('updateTransmittedMsg', {'data': "$SomeMoreTxMsg*AC"})
    await sio.emit('updateReceivededMsg', {'data': "$RxdMsg*AC"})
    await sio.emit('updateReceivededPayloadResponse', {'data': "0,0,0"})
    
    return


@sio.on('getPlTbd2')
async def getPlTbd2(sid):
    # getPlTbd2 button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getPlTbd2 Button Asserted.  Handling ...")

    await sio.emit('updateActionOutputMsg', {'data': "TBD2 Success"})
    await sio.emit('updateTransmittedMsg', {'data': "$SomeMoreTxMsg*AC"})
    await sio.emit('updateReceivededMsg', {'data': "$RxdMsg*AC"})
    await sio.emit('updateReceivededPayloadResponse', {'data': "0,0,0"})
    
    return


@sio.on('getPlTbd3')
async def getPlTbd3(sid):
    # getPlTbd3 button asserted. As a result, transmit Command Message
    
    if (VERBOSE_MODE):
        print(" ~ getPlTbd3 Button Asserted.  Handling ...")

    await sio.emit('updateActionOutputMsg', {'data': "TBD3 Success"})
    await sio.emit('updateTransmittedMsg', {'data': "$SomeMoreTxMsg*AC"})
    await sio.emit('updateReceivededMsg', {'data': "$RxdMsg*AC"})
    await sio.emit('updateReceivededPayloadResponse', {'data': "0,0,0"})
    
    return


@sio.on('getAvailSerialPorts')
async def getAvailSerialPorts(sid):
    # Scan for available Serial Ports
    
    if (VERBOSE_MODE):
        print(" ~ Scanning for available serial ports ...")

    result = subprocess.run(['python', '-m', 'serial.tools.list_ports'], capture_output=True, text=True)
    print(f"Stdout:\n{result.stdout}")
    print(f"Stderr:\n{result.stderr}")
    print(f"Return code: {result.returncode}")


    if (len(result.stdout) == 0):
        print(" ~ Stdout is empty")

    if (result.stderr == "no ports found"):
        print(" ~ Stderr is empty")

    substring = "no ports found"

    if substring in result.stderr:
        print(f'"{result.stderr}" contains "{substring}"')

    if (len(result.stdout) == 0):
        await sio.emit('updateSerialPortDropdown', {'data': 'None'})
    else:
        com_port_list = result.stdout.split()
        #await sio.emit('updateSerialPortDropdown', {'data': result.stdout})
        await sio.emit('updateSerialPortDropdown', {'data': com_port_list})
         
    return


@sio.on('openSerialPort')
def openSerialPort(sid, msg):
    # openSerialPort
    
    global ser

    # Open FileIO
    openFileIO()
    
    if (VERBOSE_MODE):
        print(" ~ Opening serial port ...")
        print("     Msg is: ")
        print(msg["data"])
        print(type(msg["data"]))
        print(len(msg["data"]))
        print(len(msg["data"][0].split()))
        print(msg["data"][0].split())

    port_list = msg["data"][0].split()
    port = port_list[0]
    data_rate = int(msg["data"][1])
    print(port)
    print(data_rate)
    print(" ~ Opening Serial Port: " + port + " @ " + str(data_rate) + " bps")
    #ser = serial.Serial(port, data_rate, timeout=1)  # open serial port
    

    try:
        ser = serial.Serial(port, data_rate, timeout=SERIAL_PORT_TIMEOUT_IN_SEC) 
        print(f"Serial port {ser.name} opened successfully.")
        print(ser)
        
        # You can perform read/write operations here
        #ser.write(b"Hello from PySerial!\n")
        #time.sleep(0.1) # Give some time for data to be sent
        #response = ser.readline().decode().strip()
        #if response:
        #    print(f"Received: {response}")

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        ser = None # Set ser to None if port couldn't be opened

    
@sio.on('closeSerialPort')
def closeSerialPort(sid):
    global ser

    # Close FileIO
    closeFileIO()
    
    if ser and ser.is_open:
        ser.close()
        print(f"Serial port {ser.name} closed.")
    else:
        print("Serial port was not opened or already closed.")
        

def getDataFromMsg(message):
    # This ordinary function is used to extract the data from the dictionary message received
    if (VERBOSE_MODE):
        print(" - Getting Data from Message ...")
    
    assert(type(message) == dict)
    assert('data' in message.keys())
    return message['data']


def performStartUpInitialization():
    # This ordinary function is used to perform start up initialization required before the server starts
    # These values will then be set upon client connection
    if (VERBOSE_MODE):
        print(" - Performing Start-up Initialization ...")


def transmitMessage(str_cmd):
    tx_cmd(str_cmd)

    return


def receiveMessages():
    str_response = rx_response()

    return str_response


def transceiveMessage(str_cmd):

    tx_cmd(str_cmd)

    # Best time to flush the buffer is right before a read operation
    # Clear any old input data before reading response
    ser.flushInput()
        
    str_response = rx_response()

    return str_response


def encode_cmd(str_cmd):
    str_cmd = str_cmd + SERIAL_TERMINATOR
    bin_cmd = str_cmd.encode('utf-8')

    return bin_cmd


def tx_cmd(str_cmd):
    global ser
    
    bin_cmd = encode_cmd(str_cmd)

    try:
        # Clear any old input data before sending a command
        ser.flushInput()

        # Send a command
        ser.write(bin_cmd)

        # Wait for the data to be sent out
        ser.flush()
        
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    
    return


async def handle_received_msg(msg):
    print(" ~ Handling Rx'd Response ...")

    if ("BEACON" in msg):

        await sio.emit('updateReceivededBeaconResponse', {'data': msg})

        datetime_str = getCurrentDatetime()
        time_str = getTimeFromDatetime(datetime_str)
        time_msg_str = time_str + ' -> ' + msg + '\n'
        datetime_str_msg_str = datetime_str + ',' + msg
        
        await sio.emit('updateMessageLog', {'data': time_msg_str})

        # Write the cmd to the Rx log file
        writeStrToRxCmdFile(datetime_str_msg_str)

    elif (msg[0] == '$'):
        datetime_str = getCurrentDatetime()
        time_str = getTimeFromDatetime(datetime_str)
        time_msg_str = time_str + ' -> ' + msg + '\n'
        datetime_str_msg_str = datetime_str + ',' + msg
        
        await sio.emit('updateMessageLog', {'data': time_msg_str})

        # Write the cmd to the Rx log file
        writeStrToRxCmdFile(datetime_str_msg_str)
    else:
        print(" ~ Unhandled Received Msg: " + msg)

    return


async def peek_for_rx_response():
    global ser

    #print(" ~ Peeking for Rx Response ...")

    if (ser.is_open):
        if (ser.in_waiting > 0):
            # Data is available, read it
            msg = ser.read(ser.in_waiting) # Read all available bytes

            msg_str = msg.decode('utf-8').strip()

            if (1):
                print(f" ~ Received: {msg_str}")

            await handle_received_msg(msg_str)

            return
            #return msg_str
        else:
            #print(" ~ No data available yet ...")
            return

    else:
        #print(" ~ Serial not open, Continuing ...")
        return


def rx_response():
    global ser
    #response_str = ""
    msg_count = 0
    response_list = []
    
    try:

        # Example of reading with timeout
        while True:
            # Read a line, will return on newline or after 1 second
            # This is bytes, then use decode to transform to string
            response = ser.readline()
            
            if not response:
                # If line is empty, the read operation timed out and no data was received
                print(" ~ Timeout occurred: No more data received.")
                break
            else:
                # Data was received
                if (0):
                    print(f"Received data: {response.decode('utf-8').rstrip()}")
                response_list.append(response.decode('utf-8').rstrip())
                msg_count += 1
                
        #print(" ~ response_str is: " + str(response_str))
        print(" ~ response_list is: " + str(response_list))
        print(" ~ msg count is: " + str(msg_count))
        
        # Read the response
        #while (ser.in_waiting > 0):
        #for i in range(10):
        #   if (ser.in_waiting > 0):
        #        response += ser.readline()
        #response = ser.readline()
        #print(f"Response: {response.decode().strip()}")
        
        #response_2 = ser.readline()
        #if (len(response_2) >0):
        #    print(f"Response_2: {response_2.decode().strip()}")
            

        # Clear any old input data before sending a command
        #ser.flushInput()

        #return response.decode('utf-8')
        #return response.decode('utf-8')
        #return response_list[0]
        return response_list

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")


def transmitMessage(msg):
    global ser
    
    print(" ~ Transmitting Message to the Serial Port ...")

    transceive_msg(msg)
    transceive_msg(cmd_2)
    
    if (ser and ser.is_open):
        print(" ~ Ser and Ser.is open is: True ...")
        ser.write(msg.encode('utf-8'))
        #ser.write(b'$GS01,6,438123456*1B')
        data = ser.readline()
        print(data.decode('utf-8'))
        #print(" ~ Message written to Serial Port ...")
        #writeStrToTxCmdFile(msg)
        #print(" ~ Message written File ...")
    else:
        print(" ~ Warning: Ser and Ser.is open is: NOT True ...")
        
    return 0



##def serialReceiveMessage():
##
##    msg = getNextMsg()
##
##    return msg
    
    
def getNextMsg():

    print(" ~ Getting next command message from Serial Port ...")
    
    global ser

    valid_cmd_not_rxd = True
    read_iteration_count = 0

    while (valid_cmd_not_rxd):
        
        if (ser and ser.is_open): 
            #msg_bytes = ser.read(100)# read up to one hundred bytes, or as much is in the buffer

            msg_bytes = ser.read_until(expected=b'\n') # '\n' newline (expected=b'\r') cr --> Looks like it is '\r\n'

            if (len(msg_bytes) > 0):
                print(f"Received data: {msg_bytes.decode('utf-8')}")
                msg = msg_bytes.decode("utf-8")
            else:
                print(f"Received data: Empty Msg, Ignoring ...")
                continue
        else:
            print(" ~ Warning: Ser and Ser.is open is: NOT True ...")

        print(type(msg)) # .decode("utf-8")
        print(msg)

        if ("$S01G" in msg):
            if ("BEACON" in msg):
                valid_cmd_not_rxd = True
            else:    
                valid_cmd_not_rxd = False
        else:
            valid_cmd_not_rxd = True

        read_iteration_count += 1
        
        print(" ~ Read Iteration is: " + str(read_iteration_count))

        if (read_iteration_count <= 10):
            break
            print(" ~ Breaking out of loop ...")
    #writeStrToRxCmdFile(msg)
    
    return msg


def constructSlimSatMessage(cmd_id, cmd_val=-1, optnl_cmd_arg=-1, id_num=-1):

    print(" ~ Constructing SlimSat Message ...")

    if (id_num == -1):
        # Then use the slimsat_id_num
        sat_id_num = slimsat_id_num
    else:
        # Use the id num provided
        sat_id_num = id_num
    
    print(" ~ Slimsat id num is: " + str(sat_id_num))

    #if (len(cmd_val) > 0):
    if ((cmd_val == -1) and (optnl_cmd_arg == -1)):
        message_payload = f"GS{sat_id_num:02d},{cmd_id}"
    elif ((cmd_val != -1) and (optnl_cmd_arg == -1)):
        message_payload = f"GS{sat_id_num:02d},{cmd_id},{cmd_val}"
    elif ((cmd_val != -1) and (optnl_cmd_arg != -1)):
        message_payload = f"GS{sat_id_num:02d},{cmd_id},{cmd_val},{optnl_cmd_arg}"
        
    checksum = computeXorChecksumValue(message_payload)
    
    message = f"${message_payload}*{checksum:02X}"

    print(message)

    return message


def getSlimSatMessageResponseVal(msg, response_val_index=RESPONSE_CMD_VAL_INDEX):

    print(" ~ Getting SlimSat Cmd Val ...")
    
    #msg = "$S01G,A,5,919123456*AB"

    exp_msg_header = f"$S{slimsat_id_num:02d}G"
    exp_msg_response_char = 'A'

    # Bug to fix. Parsing of of the cmd val index will only succeed if the message is a ack msg.
    # So implement a guard. Otherwise all bets are off
    #['$S01G', 'N', '0', '1', '0*6A\r\n']

    # Sometimes stuff happens
    if (len(msg) > 0):
    
        # Parse the token values
        msg_parm_list = msg.split(',')
        print(" ~ Parsing response ...")
        print(msg_parm_list)

        # Verify that the msg starts with the expected start character
        start_char = msg_parm_list[0][0]
        if (start_char == '$'):
            #assert(msg_parm_list[0] == exp_msg_header)
            #assert(msg_parm_list[1] == 'A')
            #assert(int(msg_parm_list[2]) == cmd_id)

            ack_status = msg_parm_list[1][0]
            if (ack_status == 'A'):
                # Then the response value can be parsed from the response. Otherwise, not
                # Validate the input
                msg_data = msg_parm_list[RESPONSE_FRAGMENT_NUMBER_INDEX].split(',')[0]
                input_is_valid = integerInputMsgDataIsValid(msg_data)

                if (input_is_valid):
                    fragment_number = int(msg_data)

                    if (fragment_number == 1):
                        response_val_str = msg_parm_list[response_val_index].split('*')[0]
                        print(response_val_str)

                        # Search for a decimal in the str
                        if '.' in response_val_str:
                            # Then parse the cmd val as a float
                            response_val = float(response_val_str)
                        else:
                            # Then parse the cmd val as an int
                            response_val = int(response_val_str)
                        
                        print(response_val)

                        return response_val

                    else:
                        return -1
                else:
                    return -1
            else:
                return -1
        else:
            return -1
    else:
        return -1


def computeXorChecksumValue(msg):
    xor_val = 0;

    print(" ~ Computing Checksum ...")
    print(" ~ msg is: " + msg)

    for char in msg:
        xor_val = xor_val ^ ord(char)


    #print(" ~ Running Compute Checksum ...")
    #msg = "$GS01,6,438123456*1B"
    #checksum = computeXorChecksumValue("GS01,6,438123456")
    #print(" ~ Checksum is: " + str(hex(checksum)).upper())

    #hex_string = f"{checksum:X}"
    #print(hex_string)

    #hex_string_alt = "{:X}".format(checksum)
    #print(hex_string_alt)

    return xor_val;


def openFileIO():

    print(" ~ Opening and initializing FileIO ...")

    global txCmdFileIo, rxCmdFileIo
    
    txCmdFileIo.createDirs(TX_CMD_OUTPUT_DIR)
    txCmdFileIo.appendFileAndAddFileHeader(TX_CMD_OUTPUT_DIR, TX_CMD_CAPTURE_FILENAME, TX_RX_FILE_HEADER)
    rxCmdFileIo.appendFileAndAddFileHeader(TX_CMD_OUTPUT_DIR, RX_CMD_CAPTURE_FILENAME, TX_RX_FILE_HEADER)

    return
    

def writeStrToTxCmdFile(msg_str):

    global txCmdFileIo
    print(" ~ Writing message to Tx Cmd File ...")

    #date_time_str = getDatetime()
    #str_to_write = date_time_str + ',' + msg_str
    #print(type(str_to_write))
    #print(" ~ Msg to write: " + str_to_write)
    
    txCmdFileIo.print()
    txCmdFileIo.writeStrToFile(msg_str)

    return


def writeStrToRxCmdFile(msg_str):

    global rxCmdFileIo
    print(" ~ Writing message to Rx Cmd File ...")

    #date_time_str = getCurrentDatetime()
    #str_to_write = date_time_str + ',' + msg_str
    #print(" ~ Msg to write: " + str_to_write)
    
    rxCmdFileIo.writeStrToFile(msg_str)

    return


def closeFileIO():

    print(" ~ Closing FileIO ...")

    global txCmdFileIo, rxCmdFileIo
    
    txCmdFileIo.closeFile()
    rxCmdFileIo.closeFile()

    return


def getTimeFromDatetime(datetime_str):

    print(" ~ Getting time from Datetime string ...")
    datetime_list = datetime_str.split(',')
    print(datetime_list)
    time_str = datetime_list[1]
    print(time_str)
    
    return time_str

    
def getCurrentDatetime():
    
    print(" ~ Getting Datetime ...")

    current_datetime = datetime.now()
    datetime_str = str(current_datetime)
    print(current_datetime)
    datetime_str = datetime_str.replace(" ",',')
    print(datetime_str)

    return datetime_str


if __name__ == '__main__':
    print("\n ~ CAPE-Twiggs SlimSat GS Web Server ...")

    #uvicorn.run(app, host='127.0.0.1', port=5000)
    #uvicorn.run(app, host='192.168.0.101', port=8050)
    #uvicorn.run(app, host='127.0.0.1', port=8000, log_level='error')
    USE_LOCALHOST_IP = True
    
    if (USE_LOCALHOST_IP):
        #uvicorn.run(app, host='127.0.0.1', port=8000, log_level='error')
        uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')
    else:
        uvicorn.run(app, host='192.168.0.101', port=8080, log_level='error')
    
    # Uvicorn logging options: 'critical', 'error', 'warning', 'info', 'debug', 'trace'. Default: 'info'.


