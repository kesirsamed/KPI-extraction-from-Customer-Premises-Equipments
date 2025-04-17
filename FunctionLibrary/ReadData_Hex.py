import struct
import FunctionLibrary.kpi_list as kpi_list

Command = "a180"
value_id_list = kpi_list.set_kpi_params()

def match_response(command, sample):

    packet_start_idx = []
    for i in range(len(sample)):
        if command == sample[i:i+4]:
            packet_start_idx.append(i)
    # print("----------------")
    # print("----------------")
    # print(f"80a1 start: {packet_start_idx}")
    # print("----------------")
    return packet_start_idx

def parse_frame_5gnr(message):
    # value_id_list = {"0D": "LTE Serving RSRP","61":"Cell_ID", "62":"ARFCN", "63":"FREQ", "65":"SSB IDX", "66":"SS RSRP", "67":"SS RSRQ", "97":"PHY PDSCH TP","98":"MAC DL TP", "A0":"RRC CUR STATE"}

    empty_field = message[:32]
    time_stamp = bytearray.fromhex(message[32:66]).decode()
    data_count = int(message[66:68], 16)

    #print("    Time stamp: " + time_stamp)
    for idx in range(data_count):
        parameter_report = message[68+idx*10:68+(idx+1)*10]

        value_id = parameter_report[:2]
        value = parameter_report[2:]
        value_float = struct.unpack('f', bytes.fromhex(value))[0]

        kpi_parameter_list = {value_id_list.get(value_id.upper()): value_float}

        #print(f"# {idx+1} {value_id_list.get(value_id.upper())}, Value = {value_float}")

    return kpi_parameter_list


def parse_frame(message):

    kpi_parameter_list = {}
    empty_field = message[:32]
    time_stamp = bytearray.fromhex(message[32:66]).decode()
    data_count = int(message[66:68],16)

    #print("    Time stamp: " + time_stamp)

    four_params_array = ['00', '01', '0e', '10', '12', '14', '68', '69']
    two_params_array = ['18', '1b', '1c', '1d', '6b', '70', '71', '72', '73']
    kpi_message = message[68:]
    count_idx = 0
    while count_idx<data_count:
        value_id = kpi_message[:2]
        kpi_message = kpi_message[2:]
        value_float = []
        if value_id in four_params_array:
            for i in range(4):
                value_float.append(struct.unpack('f', bytes.fromhex(kpi_message[i * 8:(i + 1) * 8]))[0])
            kpi_parameter_list[value_id_list.get(value_id.upper())] = value_float
            kpi_message = kpi_message[32:]
        elif value_id in two_params_array:
            for i in range(2):
                value_float.append(struct.unpack('f', bytes.fromhex(kpi_message[i * 8:(i + 1) * 8]))[0])
            kpi_parameter_list[value_id_list.get(value_id.upper())] = value_float
            kpi_message = kpi_message[16:]
        else:
            value_float = (struct.unpack('f', bytes.fromhex(kpi_message[0:8]))[0])
            kpi_parameter_list[value_id_list.get(value_id.upper())] = value_float
            kpi_message = kpi_message[8:]
        count_idx += 1
        #print(f"# {count_idx-1} {value_id_list.get(value_id.upper())}, {value_float}")

    return kpi_parameter_list

def mixed_to_full_hex(binary_data):
    if not isinstance(binary_data, (bytes, bytearray)):
        raise ValueError("Input must be a bytes or bytearray object.")
    # Convert each byte to a two-character hexadecimal representation
    result = "".join(f"{byte:02x}" for byte in binary_data)
    return result


def main(sample_text_lte):
    """
    sample_text_lte: received data from socket
    gen_type: connected cell network, LTE or 5GNR
    
    """

    full_hex = mixed_to_full_hex(sample_text_lte)

    frame_begin = match_response(Command, full_hex)

    if len(frame_begin) == 1:
        i=0
        frame_80a1 = full_hex[frame_begin[i]+4:]
        temp = parse_frame(frame_80a1)
    elif len(frame_begin) > 1:
        for idx in range(len(frame_begin)-1):
           # print(" Frame IDX" + str(idx))
            frame_80a1 = full_hex[frame_begin[idx]+4:frame_begin[idx+1]-1]
            temp = parse_frame(frame_80a1)
           # print("------------")
       # print(" Frame IDX" + str(idx+1))
        frame_80a1 = full_hex[frame_begin[-1]+4:]
        temp = parse_frame(frame_80a1)
    else:
        #print("80A1 frame does not exist...")
        return 0

    return temp