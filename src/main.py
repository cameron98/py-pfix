import socket
from functions import *
from classes.template_set import TemplateSet
from classes.data_set import DataSet

#Config Variables
port = 5000
ipfix_inf_filename = 'ipfix-information-elements.csv'

#Program Storage
templates = {}
ipfix_data_records = []
inf_element_data = load_inf_elements(ipfix_inf_filename)

if __name__ == "__main__":

    print("---Starting Server---")

    #Create server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))
    print(f"Listening on port {port}")

    #Loop to listen to input from socket server
    while True:
        data, addr = sock.recvfrom(4096)

        #Save data to file for debug
        with open('binary_out', 'wb') as file:
            file.write(data)
        
        data = list(data.hex())
        packet_data = []
        a = 0
        while a < len(data):
            packet_data.append("".join(data[a:a+2]))
            a += 2
        
        # print(packet_data)

        #Split the packet into header data,  data sets, template sets and option template sets
        packet_header_data, packet_sets = parse_packet(packet_data)

        for set_data in packet_sets["template_sets"]:
            template_set = TemplateSet(set_data)
            template_set.parse()
            templates[template_set.template_id] = template_set
        for set_data in packet_sets["data_sets"]:
            data_set = DataSet(set_data)
            record = data_set.parse(templates, inf_element_data)
            if record:
                ipfix_data_records.append(record)
            pass
        
        print(ipfix_data_records)

        