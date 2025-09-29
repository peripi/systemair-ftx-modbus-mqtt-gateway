# Format
# "Register name" : [address, scaling, include, R/RW, mqqt-topic]
reg_101_fan_speed_level = {
    0: 'Fans off',
    1: 'Fans on low speed',
    2: 'Fans on normal speed',
    3: 'Fans on high speed',
    4: 'Auto mode'
}

reg_201_heater_type = {
    0: 'No heater',
    1: 'Water heater',
    2: 'Electrical heater',
    3: 'Other'
}

reg_207_temp_lvl = {
    0: 'Manual summer mode',
    1: 'level 1',
    2: 'level 2',
    3: 'level 3',
    4: 'level 4',
    5: 'level 5'
}

reg_220_pre_heater_type = {
    0: 'No preheater',
    1: 'Electrical preheater'
}

reg_351_rotor_state = {
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

reg_671_defrost_state_vr = {
    0: 'inactive',
    1: 'low temperature',
    2: 'defrosting'
}

# detailed register descriptions
reg_701_di_all = {
    0:  'b0 Input 1 di 1',
    1:  'b1 Input 2 di 2',
    2:  'b2 Input 3 di 3',
    3:  'b3 Input 4 (Heater on/off)',
    4:  'b4 input 5 (ext running)',
    5:  'b5 input 6 (rotor/damper)',
    6:  'b6 input 7 (home/leave)',
    7:  'b7 input 8 not used',
    8:  'b8 coil 11201: input 1', # unsure of these
    9:  'b9 coil 11202: input 2', # unsure of these
    10: 'b10 coil 11203: input 3', # unsure of these
    11: 'b11 coil 11204: input 4', # unsure of these
    12: 'b12 coil 11205: input 5', # unsure of these
    13: 'b13 coil 11206: input 6', # unsure of these
    14: 'b14 coil 11207: input 7', # unsure of these
    15: 'b15 ' # unsure of these
}

# register_headers = ['mqtt_topic', 'mbAddr', 'scaling', 'include', 'read_write', 'binary_coded']

# list based on the system air naming convention and modbus register address.
system_air_registers = {
    "headers" : ['sys_air_reg_name', 'mqtt_topic', 'mbAddr', 'scaling', 'include', 'read_write', 'binary_coded'],
    "registers" : [
        ["REG_FAN_SPEED_LEVEL", "FAN_SPEED_LEVEL", 101, 1, True, 'RW', reg_101_fan_speed_level],  # 0: Fans off,1: Fans on low speed,2: Fans on normal speed,3: Fans on high speed,4: Auto mode
        ["REG_FAN_SF_FLOW_NOM", "FAN_SPEED_AIR_SUPPLY_NOM", 104, 1, True, 'RW'],  # Supply air fan speed for nominal speed
        ["REG_FAN_EF_FLOW_NOM", "FAN_SPEED_AIR_EXTRACT_NOM", 105, 1, True, 'RW'],  # Extract air fan speed for nominal speed
        ["REG_FAN_SF_PWM", "AIR_FAN_SUPPLY_VOLTAGE", 109, 10, True, 'R'],  # Supply air fan speed 0..10V
        ["REG_FAN_EF_PWM", "AIR_FAN_EXTRACT_VOLTAGE", 110, 10, True, 'R'],  # Extract air fan speed 0..10V

        ["REG_FAN_SPEED_LEVEL", "FAN_SPEED_LEVEL", 101, 1, True, 'RW', reg_101_fan_speed_level],  # 0: Fans off,1: Fans on low speed,2: Fans on normal speed,3: Fans on high speed,4: Auto mode
        ["REG_FAN_SF_FLOW_NOM", "FAN_SPEED_AIR_SUPPLY_NOM", 104, 1, True, 'RW'],  # Supply air fan speed for nominal speed
        ["REG_FAN_EF_FLOW_NOM", "FAN_SPEED_AIR_EXTRACT_NOM", 105, 1, True, 'RW'],  # Extract air fan speed for nominal speed
        ["REG_FAN_SF_PWM", "AIR_FAN_SUPPLY_VOLTAGE", 109, 10, True, 'R'],  # Supply air fan speed 0..10V
        ["REG_FAN_EF_PWM", "AIR_FAN_EXTRACT_VOLTAGE", 110, 10, True, 'R'],  # Extract air fan speed 0..10V

        ["REG_HC_HEATER_TYPE", "HEATER_TYPE", 201, 1, True, 'RW', reg_201_heater_type],  # 0: no heater, 1: Water heater, 2: Electrical heater, 3: Other
        ["REG_HC_TEMP_LVL", 'TEMP_REFERENCE_LEVEL', 207, 1, True, 'RW', reg_207_temp_lvl],  # Temperature set point level: 0: Manual summer mode. 1..5 Temp level
        ["REG_HC_TEMP_SP", 'TEMP_REFERENCE', 208, 10, True, 'R'],  # Read . Temperature set point.
        ["REG_HC_TEMP_IN1", 'TEMP_SUPPLY_AIR', 214, 10, True, 'R'],  # Temperature. Supply air
        ["REG_HC_TEMP_IN2", 'TEMP_EXTRACT_AIR', 215, 10, True, 'R'],  # Temperature. Extract air

        ["REG_HC_TEMP_IN3", 'TEMP_EXHAUST_AIR', 216, 10, True, 'R'],  # Temperature. Exhaust air
        ["REG_HC_TEMP_IN4", 'TEMP_FROST_HEAT_PROT', 217, 10, True, 'R'],  # Temperature. Over heating/frost protection
        ["REG_HC_TEMP_IN5", 'TEMP_OUTDOOR_AIR', 218, 10, True, 'R'],  # Temperature. Outdoor air
        ["REG_HC_PREHEATER_TYPE", 'PREHEATER_TYPE', 220, 1, True, 'RW', reg_220_pre_heater_type],  # 0: No preheater, 1: Electrical preheater
        ["REG_DAMPER_PWM", 'DAMPER_PWM', 301, 1, True, 'R'],  # Output value for exchanger. Unsure of meaning. 0-100, correspond to 0 to 10V.

        ["REG_ROTOR_STATE", 'ROTOR_STATE', 351, 1, True, 'R', reg_351_rotor_state],  # 0..11 State for the rotor control state machine. 0: Normal
        ["REG_SYSTEM_ROTOR_TYPE", 'SYSTEM_ROTOR_TYPE', 353, 1, True, 'RW'],  # Indicates the type of rotor control: 0: On/off control, 1: Variable control
        ["REG_FILTER_DAYS", 'FILTER_OPERATION_TIME', 602, 1, True, 'RW'],  # Elapsed days since last filter replacement

        ["REG_DEFR_STATE_VR", 'DEFROST_STATE', 671, 1, True, 'R', reg_671_defrost_state_vr],  # State of defrosting state machine. 0: Inactive. 1: Low temperature. 2: Defrosting
        ["REG_DI_ALL", 'STATUS_DI', 701, 1, True, 'R', reg_701_di_all],  # Activation of functions connected to digital inputs
        ["REG_PCU_PB_RELAYS", 'PCB_RELAYS_STATUS', 711, 1, True, 'R'],  # 1-prepeater on, 2 reheater on, 3 both.

        ["REG_ALARMS_ALL", 'ACTIVE_ALARMS_WORD', 801, 1, True, 'R'],  # Active alarms
        ["REG_ALARMS_RELAY_ACTIVE",'ALARM_IS_ACTIVE', 802, 1, True, 'R'],  # Alarm relay
        ["REG_ALARMS_ALL_DETAILED", 'text', 803, 1, True, 'R']  # All alarm flags, including temperature, sensor status flags.
    ]
}

#dictionary with mqtt-topic as key
def registers()->dict:
    """
        returns register as dict, with mqtt topic as key element
    :return:
    """
    regs = {}
    headers = system_air_registers.get('headers')
    for sys_air_register in system_air_registers.get('registers'):
        entry = []
        for i in range(len(sys_air_register)):
            entry.append({headers[i]:sys_air_register[i]})
        regs[sys_air_register[1]] = entry
    return regs

if __name__ == "__main__":
    register = registers()
        #mqtt_regs[headers[1]] = [].append({headers[i]:register[i]}) for i in range(len(headers))

tet = 12