"""
IP ADDRESS AND MASK
"""

def check_rules(raw_address: str) -> str:
    """
    This function cheak correct input
    """
    for i in raw_address:
        if i.isalpha():
            return 'Error'
    for w in raw_address:
        if any(w) == '/':
            return 'Missing prefix'
    data =  raw_address.split('.')
    w = data[-1].split('/')
    if int(w[0]) > 255 or int(w[1]) > 32:
        return 'Error'
    for i in data[:-1]:
        if not i.isnumeric():
            return 'Error'
    if data[-1][-2] != '/' and data[-1][-3] != '/':
        return 'Missing prefix'
    for i in data[:-1]:
        if int(i) > 255:
            return 'Error'
    
    

def get_ip_from_raw_address(raw_address: str) -> str:
    """
    This function get ip address from raw address
    >>> get_ip_from_raw_address('91.124.230.205/30')
    '91.124.230.205'
    """
    if check_rules(raw_address) == 'Error' or check_rules(raw_address) == 'Missing prefix':
        return None
    for i in raw_address:
        if i == '/':
            return raw_address[:raw_address.index(i)]

def masking(raw_address: str) -> str:
    """
    This function get mask from raw address
    >>> masking('91.124.230.205/30')
    '30'
    """
    if check_rules(raw_address) == 'Error' or check_rules(raw_address) == 'Missing prefix':
        return None
    for i in raw_address:
        if i == '/':
            new_raw = raw_address[raw_address.index(i)+1:]
    return new_raw

def get_binary_from_ip(raw_address: str) -> str:
    """
    This function convert ip address to binary format
    >>> get_binary_from_ip('91.124.230.205/30')
    '01011011.01111100.11100110.11001101'
    """
    if check_rules(raw_address) == 'Error' or check_rules(raw_address) == 'Missing prefix':
        return None
    binary = get_ip_from_raw_address(raw_address)
    data = binary.split('.')
    new_list = []
    for i in data:
        q = bin(int(i))[2:]
        new_list.append(q)
    result = ''.join((8- len(x))*'0'+ x + '.' if len(x) < 8 else x + '.' for x in new_list)[:-1]
    return result

def get_ip_from_binary(raw_address: str) -> str:
    """
    This function convert binary format to ip
    >>> get_ip_from_binary('01011011.01111100.11100110.11001101')
    '91.124.230.205'
    """
    numbers = raw_address.split('.')
    old_list = []
    for i in numbers:
        w = int(i, 2)
        old_list.append(w)
    result = ''.join(str(q) + '.' for q in old_list)[:-1]
    return result

def get_binary_mask_from_raw_address(raw_address: str) -> str:
    """
    This function gets binary mask from ip address
    >>> get_binary_mask_from_raw_address('91.124.230.205/30')
    '11111111.11111111.11111111.11111100'
    """
    if check_rules(raw_address) == 'Error' or check_rules(raw_address) == 'Missing prefix':
        return None
    for i in raw_address:
        if i == '/':
            new_raw = raw_address[raw_address.index(i)+1:]
    result = ''
    a = int(new_raw)
    b = int(new_raw)
    while b > 0:
        result += '1'
        b -= 1        
    if b == 0:
        result += '0' * (32 - a)
    return result[:8] + '.' + result[8:16] + '.' + result[16:24] + '.' + result[24:]

def get_network_address_from_raw_address(raw_address: str) -> str:
    """
    This function gets network address grom raw address
    >>> get_network_address_from_raw_address('91.124.230.205/30')
    '91.124.230.204'
    """
    if check_rules(raw_address) == 'Error' or check_rules(raw_address) == 'Missing prefix':
        return None
    prog = ''.join(get_binary_from_ip(raw_address).split('.'))
    line = masking(raw_address)
    result = prog[:int(line)] + '0'*len(prog[int(line):])
    ending = result[:8] + '.' + result[8:16] + '.' + result[16:24] + '.' + result[24:]
    return get_ip_from_binary(ending)

def get_broadcast_address_from_raw_address(raw_address: str) -> str:
    """
    This function gets broadcats address from eaw address
    >>> get_broadcast_address_from_raw_address('91.124.230.205/30')
    '91.124.230.207'
    """
    if check_rules(raw_address) == 'Error' or check_rules(raw_address) == 'Missing prefix':
        return None
    prog = ''.join(get_binary_from_ip(raw_address).split('.'))
    line = masking(raw_address)
    result = prog[:int(line)] + '1'*len(prog[int(line):])
    ending = result[:8] + '.' + result[8:16] + '.' + result[16:24] + '.' + result[24:]
    return get_ip_from_binary(ending)

def get_first_usable_ip_address_from_raw_address(raw_address: str) -> str:
    """
    This function gets first unable ip address from raw address
    >>> get_first_usable_ip_address_from_raw_address('91.124.230.205/30')
    '91.124.230.205'
    """
    if check_rules(raw_address) == 'Error' or check_rules(raw_address) == 'Missing prefix':
        return None
    data = get_network_address_from_raw_address(raw_address).split('.')
    new_data = int(data[-1]) + 1
    data[-1] = str(new_data)
    finish = ''.join(i + '.' for i in data)[:-1]
    return finish

def get_penultimate_usable_ip_address_from_raw_address(raw_address: str) -> str:
    """
    This function gets penultimate usable ip address from raw address
    >>> get_penultimate_usable_ip_address_from_raw_address('91.124.230.205/30')
    '91.124.230.205'
    """
    if check_rules(raw_address) == 'Error' or check_rules(raw_address) == 'Missing prefix':
        return None
    data = get_broadcast_address_from_raw_address(raw_address).split('.')
    new_data = int(data[-1]) - 2
    data[-1] = str(new_data)
    finish = ''.join(i + '.' for i in data)[:-1]
    return finish

def get_number_of_usable_hosts_from_raw_address(raw_address: str) -> int:
    """
    This function gets number of usable hosts from raw address
    >>> get_number_of_usable_hosts_from_raw_address('91.124.230.205/30')
    2
    """
    if check_rules(raw_address) == 'Error' or check_rules(raw_address) == 'Missing prefix':
        return None
    return 2**(32 - int(masking(raw_address))) - 2

def get_ip_class_from_raw_address(raw_address: str) -> str:
    """
    This function get ip class from raw address
    >>> get_ip_class_from_raw_address('91.124.230.205/30')
    'A'
    """
    if check_rules(raw_address) == 'Error' or check_rules(raw_address) == 'Missing prefix':
        return None
    data = raw_address.split('.')
    if 0<int(data[0])<=126:
        return 'A'
    if 128 <= int(data[0]) <= 191:
        return 'B'
    if 192 <= int(data[0]) <= 223:
        return 'C'
    if 224 <= int(data[0]) <= 239:
        return 'D'
    if 240 <= int(data[0]) <= 247:
        return 'E'

def check_private_ip_address_from_raw_address(raw_address: str) -> bool:
    """
    This function check is ip address private
    >>> check_private_ip_address_from_raw_address('91.124.230.205/30')
    False
    """
    if check_rules(raw_address) == 'Error' or check_rules(raw_address) == 'Missing prefix':
        return None
    data = raw_address.split('.')
    if int(data[0]) == 10:
        return True
    if int(data[0]) == 172:
        if 16 <= int(data[1]) <= 31:
            return True
    if int(data[0]) == 192:
        if int(data[1]) == 168:
            return True
    return False

if __name__ == "__main__":
    raw_address = str(input())
    if check_rules(raw_address) == None:
        print(  f'IP address:  {get_ip_from_raw_address(raw_address)}','\n',
        f'Network Address:  {get_network_address_from_raw_address(raw_address)}','\n',
        f'Broadcast Address: {get_broadcast_address_from_raw_address(raw_address)}','\n',
        f'Binary Subnet Mask: {get_binary_mask_from_raw_address(raw_address)}','\n',
        f'First usable host IP: {get_first_usable_ip_address_from_raw_address(raw_address)}','\n',
        f'Penultimate usable host IP: {get_penultimate_usable_ip_address_from_raw_address(raw_address)}','\n',
        f'Number of usable Hosts: {get_number_of_usable_hosts_from_raw_address(raw_address)}','\n',
        f'IP class: {get_ip_class_from_raw_address(raw_address)}','\n',
        f'IP type private: {check_private_ip_address_from_raw_address(raw_address)}')
    else:
        print(check_rules(raw_address))