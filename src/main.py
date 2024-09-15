import socket
from functions import *
from classes.template_set import TemplateSet
from classes.data_set import DataSet
import json

#Config Variables
port = 5000
ipfix_inf_filename = 'ipfix-information-elements.csv'
dataset_buffer_max_len = 100

#Program Storage
templates = {}
inf_element_data = load_inf_elements(ipfix_inf_filename)
dataset_buffer = []

if __name__ == "__main__":

    print("---Starting Server---")

    #Create server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))
    print(f"Listening on port {port}")


    json_outfile = open("../out/ipfix_out.json", "w+")
  
    #Loop to listen to input from socket server
    while True:
        data, addr = sock.recvfrom(4096)
        
        data = list(data.hex())
        packet_data = []
        a = 0
        while a < len(data):
            packet_data.append("".join(data[a:a+2]))
            a += 2
        
        #Split the packet into header data,  data sets, template sets and option template sets
        packet_header_data, packet_sets = parse_packet(packet_data)

        for set_data in packet_sets["template_sets"]:
            template_set = TemplateSet(set_data)
            template_set.parse()
            templates[template_set.template_id] = template_set
        
        for set_data in packet_sets["data_sets"]:
            data_set = DataSet(set_data)
            records = data_set.parse(templates, inf_element_data)
            if records:
                for record in records:
                    ipfix_json = json.dumps(record)
                    json_outfile.write(ipfix_json)
                    json_outfile.write('\n')
            else:
                if len(dataset_buffer) >= 100:
                    dataset_buffer.pop(0)
                dataset_buffer.append(data_set)
                print(f"DataSet received with unknown template ID {data_set.template_id}")

        for data_set in dataset_buffer:
            records = data_set.parse(templates, inf_element_data)
            if records:
                for record in records:
                    ipfix_json = json.dumps(record)
                    json_outfile.write(ipfix_json)
                    json_outfile.write('\n')
                dataset_buffer.remove(data_set)

        