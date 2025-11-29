# Registers based on following
# https://shop.systemair.com/upload/assets/MODBUS_FOR_RESIDENTIAL_D24810_USER_MANUAL_EN__A007_.PDF?03eb52f3

reg_101_fan_speed_level = {
    'type': 'SINGLE',
    'coding':
        {
            0: 'Fans off',
            1: 'Fans on low speed',
            2: 'Fans on normal speed',
            3: 'Fans on high speed',
            4: 'Auto mode'
        }
}

reg_201_heater_type = {
    'type': 'SINGLE',
    'coding':
        {
            0: 'No heater',
            1: 'Water heater',
            2: 'Electrical heater',
            3: 'Other'
        }
}

reg_207_temp_lvl = {
    'type': 'SINGLE',
    'coding':
        {
            0: 'Manual summer mode',
            1: 'level 1',
            2: 'level 2',
            3: 'level 3',
            4: 'level 4',
            5: 'level 5'
        }
}

reg_220_pre_heater_type = {
    'type': 'SINGLE',
    'coding':
        {
            0: 'No preheater',
            1: 'Electrical preheater'
        }
}

reg_351_rotor_state = {
    'type': 'SINGLE',
    'coding' :
        {
            0: 'Normal',
            1: 'Rotor fault assumed',
            2: 'Rotor fault detected',
            3: 'Summer mode conditions valid',
            4: 'Summer mode',
            5: 'Waiting to go out of Manual summer mode due to temperature conditions',
            6: 'Manual summer mode',
            7: 'Rotor cleaning during summer mode',
            8: 'Rotor cleaning during manual summer mode',
            9: 'Fans off',
            10: 'Rotor cleaning during fans off',
            11: 'Rotor fault, conditions for rotor fault not valid anymore'
        }
}

reg_671_defrost_state_vr = {
    'type': 'SINGLE',
    'coding':
        {
            0: 'inactive',
            1: 'low temperature',
            2: 'defrosting'
        }
}

# detailed register descriptions
reg_701_di_all = {
    'type': 'BINARY',
    'coding':
        {
            0:  'b0 Input 1 di 1',
            1:  'b1 Input 2 di 2',
            2:  'b2 Input 3 di 3',
            3:  'b3 Input 4 (Heater on/off)',
            4:  'b4 input 5 (ext running)',
            5:  'b5 input 6 (rotor/damper) READ-ONLY!',
            6:  'b6 input 7 (home/leave)',
            7:  'b7 input 8 not used',
        }
}

reg_801_regs_alarms_all_detailed = {
    'type': 'BINARY',
    'coding' :
        {
            0: 'Filter alarm',
            1: 'Fan alarm',
            2: 'Not used',
            3: 'Rotor alarm',
            4: 'Frost alarm',
            5: 'PCU-PB alarm',
            6: 'Temperature sensor',
            7: 'Emergency larm',
            8: 'Damper alarm',
            9: 'Low SS alarm',
            10: 'Defrost alarm',
            11: 'RH sensor'
        }
}

reg_803_regs_alarms_all_detailed = {
    'type': 'BINARY',
    'coding' :
        {
            0:  'Filter alarm',
            1:  'Fan alarm',
            2:  'Rotor alarm',
            3:  'Frost alarm',
            4:  'PCU-PB alarm',
            5:  'Emergency thermostat alarm',
            6:  'Damper alarm',
            7:  'Low SS alarm',
            8:  'Defrost alarm',
            9:  'RH sensor alarm',
            10: 'Supply air sensor alarm',
            11: 'Extract air sensor alarm',
            12: 'Exhaust air/Preheater sensor alarm',
            13: 'Over temperature/Frost protection sensor alarm',
            14: 'Outdoor air sensor alarm'
        }
}

reg_501_system_type = {
    'type': 'SINGLE',
    'coding' :
        {
            0:  'VR400',
            1:  'VR700',
            2:  'VR700DK',
            3:  'VR400DE',
            4:  'VTC300',
            5:  'VTC700',
            12: 'VTR150K',
            13: 'VTR200B',
            14: 'VSR300',
            15: 'VSR500',
            16: 'VSR150',
            17: 'VTR300',
            18: 'VTR500',
            19: 'VSR300DE',
            20: 'VTC200',
            21: 'VTC100'
        }
}

reg_353_regs_system_rotor_type = {
    'type': 'SINGLE',
    'coding' :
        {
            0:  'On/Off control',
            1:  'Variable control',
        }
}

reg_751_pcu_pb_relays = {
    'type': 'BINARY',
    'coding' :
        {
            0:  'none',
            1:  'Heater on',
            2:  'Reheater on',
        }
}

reg_boolean = {
    'type' : 'BOOLEAN'
}

reg_value = {
    'type' : 'VALUE'
}

# list based on the system air naming convention and modbus register address.
system_air_registers = {
    "headers" : ['sys_air_reg_name', 'mqtt_topic', 'mb_addr', 'scaling', 'include', 'read_write', 'binary_coded', 'test_value'],
    "registers" : [
        # 0: Fans off,1: Fans on low speed,2: Fans on normal speed,3: Fans on high speed,4: Auto mode
        ["REG_FAN_SPEED_LEVEL", "FAN_SPEED_LEVEL", 101, 1, True, 'RW', reg_101_fan_speed_level, 2],  # 0: Fans off,1: Fans on low speed,2: Fans on normal speed,3: Fans on high speed,4: Auto mode
        ["REG_FAN_SF_FLOW_LOW", "FAN_SPEED_AIR_SUPPLY_LOW", 102, 1, True, 'RW', reg_value, 1],
        ["REG_FAN_EF_FLOW_LOW", "FAN_SPEED_AIR_EXTRACT_LOW", 103, 1, True, 'RW', reg_value, 2],
        ["REG_FAN_SF_FLOW_NOM", "FAN_SPEED_AIR_SUPPLY_NOM", 104, 1, True, 'RW', reg_value, 1],  # Supply air fan speed for nominal speed
        ["REG_FAN_EF_FLOW_NOM", "FAN_SPEED_AIR_EXTRACT_NOM", 105, 1, True, 'RW', reg_value, 2],  # Extract air fan speed for nominal speed
        ["REG_FAN_SF_FLOW_HIGH", "FAN_SPEED_AIR_SUPPLY_HIGH", 106, 1, True, 'RW', reg_value, 1],
        ["REG_FAN_EF_FLOW_HIGH", "FAN_SPEED_AIR_EXTRACT_HIGH", 107, 1, True, 'RW', reg_value, 2],
        ["REG_FAN_SF_PWM", "AIR_FAN_SUPPLY_VOLTAGE", 109, 10, True, 'R', reg_value, 35],  # Supply air fan speed 0..10V
        ["REG_FAN_EF_PWM", "AIR_FAN_EXTRACT_VOLTAGE", 110, 10, True, 'R', reg_value, 38],  # Extract air fan speed 0..10V

        ["REG_HC_HEATER_TYPE", "HEATER_TYPE", 201, 1, True, 'RW', reg_201_heater_type, 2],  # 0: no heater, 1: Water heater, 2: Electrical heater, 3: Other
        ["REG_HC_FPS_LEVEL", "FROST_PROT_TEMP_REF", 206, 10, True, 'RW', reg_value, 7], # frost protection level. Allowed values: 70, 80, 90, 100, 110, 120 = 7, 8, 9, 10, 11, 12°C
        ["REG_HC_TEMP_LVL", 'TEMP_REFERENCE_LEVEL', 207, 1, True, 'RW', reg_207_temp_lvl, 4],  # Temperature set point level: 0: Manual summer mode. 1..5 Temp level
        ["REG_HC_TEMP_SP", 'TEMP_REFERENCE', 208, 10, True, 'R', reg_value, 184],  # Read . Temperature set point.

        ["REG_HC_TEMP_IN1", 'TEMP_SUPPLY_AIR', 214, 10, True, 'R', reg_value, 192],  # Temperature. Supply air
        ["REG_HC_TEMP_IN2", 'TEMP_EXTRACT_AIR', 215, 10, True, 'R', reg_value, 215],  # Temperature. Extract air
        ["REG_HC_TEMP_IN3", 'TEMP_EXHAUST_AIR', 216, 10, True, 'R', reg_value, 51],  # Temperature. Exhaust air
        ["REG_HC_TEMP_IN4", 'TEMP_FROST_HEAT_PROT', 217, 10, True, 'R', reg_value, 190],  # Temperature. Over heating/frost protection
        ["REG_HC_TEMP_IN5", 'TEMP_OUTDOOR_AIR', 218, 10, True, 'R', reg_value, 23],  # Temperature. Outdoor air

        ["REG_HC_PREHEATER_TYPE", 'PREHEATER_TYPE', 220, 1, True, 'RW', reg_220_pre_heater_type, 0],  # 0: No preheater, 1: Electrical preheater
        ["REG_DAMPER_PWM", 'DAMPER_VOLTAGE', 301, 10, True, 'R', reg_value, 38],  # Output value for exchanger. Unsure of meaning. 0-100, correspond to 0 to 10V.
        ["REG_ROTOR_STATE", 'ROTOR_STATE', 351, 1, True, 'R', reg_351_rotor_state, 0],  # 0..11 State for the rotor control state machine. 0: Normal
        ["REG_ROTOR_RELAY_ACTIVE", 'ROTOR_RELAY_STATE', 352, 1, True, 'R', reg_boolean, 0],
        ["REG_SYSTEM_ROTOR_TYPE", 'SYSTEM_ROTOR_TYPE', 353, 1, True, 'RW', reg_353_regs_system_rotor_type, 0],  # Indicates the type of rotor control: 0: On/off control, 1: Variable control

        ["REG_SYSTEM_TYPE", 'FTX_MODELL_VERSION', 501, 1, True, 'R', reg_501_system_type, 0],
        ["REG_SYSTEM_PROG_V_HIGH", 'REG_SYSTEM_PROG_V_HIGH', 502, 1, True, 'R', reg_value, 0],
        ["REG_SYSTEM_PROG_V_MID", 'REG_SYSTEM_PROG_V_MID', 503, 1, True, 'R', reg_value, 0],
        ["REG_SYSTEM_PROG_V_LOW", 'REG_SYSTEM_PROG_V_LOW', 504, 1, True, 'R', reg_value, 0],
        ["REG_SYSTEM_BOOT_PROG_V_HIGH", 'REG_SYSTEM_BOOT_PROG_V_HIGH', 505, 1, True, 'R', reg_value, 0],
        ["REG_SYSTEM_BOOT_PROG_V_MID", 'REG_SYSTEM_BOOT_PROG_V_MID', 506, 1, True, 'R', reg_value, 0],
        ["REG_SYSTEM_BOOT_PROG_V_LOW", 'REG_SYSTEM_BOOT_PROG_V_LOW', 507, 1, True, 'R', reg_value, 0],

        ["REG_FILTER_DAYS", 'FILTER_OPERATION_DAYS', 602, 1, True, 'RW', reg_value, 157],  # Elapsed days since last filter replacement

        ["REG_DEFR_STATE_VR", 'DEFROST_STATE', 671, 1, True, 'R', reg_671_defrost_state_vr, 1],  # State of defrosting state machine. 0: Inactive. 1: Low temperature. 2: Defrosting
        ["REG_DEFR_MODE_VR", 'REG_DEFR_MODE_VR', 672, 1, True, 'RW', reg_value, 1],
        ["REG_DI_ALL", 'STATUS_DI', 701, 1, True, 'R', reg_701_di_all, 5],  # Activation of functions connected to digital inputs
        ["REG_PCU_PB_RELAYS", 'PCB_RELAYS_STATUS', 751, 1, True, 'R', reg_751_pcu_pb_relays, 0],  # 1-prepeater on, 2 reheater on, 3 both.

        ["REG_ALARMS_ALL", 'ACTIVE_ALARMS_WORD', 801, 1, True, 'R', reg_801_regs_alarms_all_detailed, 256],  # Active alarms
        ["REG_ALARMS_RELAY_ACTIVE",'ALARM_IS_ACTIVE', 802, 1, True, 'R', reg_boolean, 0],  # Alarm relay
        ["REG_ALARMS_ALL_DETAILED", 'ALARMS_ALL_DETAILED', 803, 1, True, 'R', reg_803_regs_alarms_all_detailed, 1234]  # All alarm flags, including temperature, sensor status flags.
    ]
}

# registers used during debugging
test_registers = {
    "headers" : ['sys_air_reg_name', 'mqtt_topic', 'mb_addr', 'scaling', 'include', 'read_write', 'binary_coded', 'test_value'],
    "registers" : [
        ["REG_FAN_SPEED_LEVEL", "debug_1", 101, 1, True, 'RW', reg_101_fan_speed_level, 2],
        ["REG_FAN_SPEED_LEVEL", "debug_2", 102, 1, True, 'RW', reg_101_fan_speed_level, 2],
        ["REG_FAN_SPEED_LEVEL", "debug_3", 103, 1, True, 'RW', reg_101_fan_speed_level, 2],
        ["REG_FAN_SF_FLOW_NOM", "debug_4", 104, 1, True, 'RW', reg_value, 1],  # Supply air fan speed for nominal speed
        ["REG_FAN_EF_FLOW_NOM", "debug_5", 105, 1, True, 'RW', reg_value, 2],  # Extract air fan speed for nominal speed
        ["REG_FAN_SPEED_LEVEL", "debug_6", 106, 1, True, 'RW', reg_101_fan_speed_level, 2],
        ["REG_FAN_SPEED_LEVEL", "debug_7", 107, 1, True, 'RW', reg_101_fan_speed_level, 2],
        ["REG_FAN_SPEED_LEVEL", "debug_8", 108, 1, True, 'RW', reg_101_fan_speed_level, 2],
        ["REG_FAN_SF_PWM", "debug_9", 109, 10, True, 'R', reg_value, 35],  # Supply air fan speed 0..10V
        ["REG_FAN_EF_PWM", "debug_10", 110, 10, True, 'R', reg_value, 38],  # Extract air fan speed 0..10V
    ]
}

#dictionary with mqtt-topic as key
def registers()->dict:
    """
        returns register as dict, with mqtt topic as key element
    :return:
    """
    source_registers = system_air_registers
    regs = {}
    headers = source_registers.get('headers')
    for register in source_registers.get('registers'):
        entry = {}
        for i in range(len(register)):
            if isinstance(register[i], str):
                entry[headers[i]] = register[i].lower()
            else:
                entry[headers[i]] = register[i]
        regs[entry.get('mqtt_topic')] = entry
    return regs

if __name__ == "__main__":
    register = registers()
