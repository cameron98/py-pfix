import socket
import json
from utils import parse_packet, load_inf_elements
from os import path, makedirs
from classes.template_set import TemplateSet
from classes.data_set import DataSet

class IPFixCollector:

    def __init__(self, port, ipfix_inf_filename, buffer_max_len) -> None:
        self.port = port
        self.dataset_buffer = []
        self.templates = {}
        self.buffer_max_len = buffer_max_len
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.create_out_dir()
        self.json_outfile = open("../out/ipfix_out.json", "a")
        self.inf_element_data = load_inf_elements(ipfix_inf_filename)


    def create_out_dir(self):
        if not path.isdir('../out'):
            makedirs('../out')

    def start(self):
        self.sock.bind(('0.0.0.0', self.port))
        print(f"Listening on port {self.port}")
        while True:
            data, addr = self.sock.recvfrom(4096)
            
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
                self.templates[template_set.template_id] = template_set
            
            for set_data in packet_sets["data_sets"]:
                data_set = DataSet(set_data)
                records = data_set.parse(self.templates, self.inf_element_data)
                if records:
                    for record in records:
                        ipfix_json = json.dumps(record)
                        self.json_outfile.write(ipfix_json)
                        self.json_outfile.write('\n')
                else:
                    if len(self.dataset_buffer) >= self.buffer_max_len:
                        self.dataset_buffer.pop(0)
                    self.dataset_buffer.append(data_set)
                    print(f"DataSet received with unknown template ID {data_set.template_id}")

            for data_set in self.dataset_buffer:
                records = data_set.parse(self.templates, self.inf_element_data)
                if records:
                    for record in records:
                        ipfix_json = json.dumps(record)
                        self.json_outfile.write(ipfix_json)
                        self.json_outfile.write('\n')
                    self.dataset_buffer.remove(data_set)
        