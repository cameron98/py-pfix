import ipaddress

def hexarr2int(indexStart, indexStop, array):
    return int("".join(array[indexStart:indexStop]), 16)

def load_inf_elements(filename):
    """
    Open and parse the csv file containing all the information element ids and associated values.
    Return as a dict.
    """

    information_elements = {}

    with open(filename, 'r') as file:
        csv_data = file.readlines()

    csv_data = csv_data[1:]

    for line in csv_data:
        line = line.split(",")
        information_elements[line[0]] = {
            "name": line[1],
            "abstract_data_type": line[2],
            "data_type_semantics": line[3],
            "units": line[5]
        }

    return information_elements

def parse_packet(packet_bytearray):
    """
    Takes full packet byte array as argument. Takes packet header and parses, returning data in dict format. 
    Splits packet body into individual frames and returns a second dict containing these.
    """
    header_meta = {
        "version_number": hexarr2int(0, 2, packet_bytearray),
        "length": hexarr2int(2, 4, packet_bytearray),
        "export_time": hexarr2int(4, 8, packet_bytearray),
        "sequence_number": hexarr2int(8, 12, packet_bytearray),
        "observation_dom_id": hexarr2int(12, 16, packet_bytearray)
    }

    print(header_meta)

    packet_sets = {
        "template_sets": [],
        "data_sets": [],
        "options_template_sets": []
    }

    byte_cursor = 16
    while byte_cursor < header_meta["length"]:
        set_id = hexarr2int(byte_cursor, byte_cursor+2, packet_bytearray)
        set_length = hexarr2int(byte_cursor+2, byte_cursor+4, packet_bytearray)
        set_bytes = packet_bytearray[byte_cursor:byte_cursor+set_length]

        """
        Reference from RFC 7011

        Identifies the Set.  A value of 2 is reserved for Template Sets.
        A value of 3 is reserved for Options Template Sets.  Values from 4
        to 255 are reserved for future use.  Values 256 and above are used
        for Data Sets.  The Set ID values of 0 and 1 are not used, for
        historical reasons
        """

        if set_id == 2:
            packet_sets["template_sets"].append(set_bytes)
        elif set_id == 3:
            packet_sets["options_template_sets"].append(set_bytes)
        elif set_id >= 256:
            packet_sets["data_sets"].append(set_bytes)
        else:
            print(f"Warning: You should not be seeing this message. Invalid set ID found: {set_id}")

        byte_cursor += set_length

    return header_meta, packet_sets

def format_ip_address(ip_address):
    """
    Convert an integer to its associated IP address and return it as a string.
    """
    return format(ipaddress.ip_address(int(ip_address)))