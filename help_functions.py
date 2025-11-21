

def int_to_binary(value:int)->list:
    """
    :param value: the integer that should be converted bo bit
    :return: a list with binary information as function of index
    """
    binary=[]
    while value > 0:
        binary.append(value % 2 != 0)
        value = int(value/2)
    return binary