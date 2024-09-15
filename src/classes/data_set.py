from functions import *
from math import floor as round_down

class DataSet:

    def __init__(self, set_bytes) -> None:
        self.set_bytes = set_bytes
        self.template_id = hexarr2int(0, 2, self.set_bytes)
        self.set_length = hexarr2int(2, 4, self.set_bytes)
        self.data_records = []
        print(f"Data Set received with template ID: {self.template_id}")

    def parse(self, templates, inf_element_data):
        if self.template_id not in templates:
            return False
        else:
            template = templates[self.template_id]
            set_template = template.template
            packet_cursor = 4
            data_set_len = template.get_data_set_len()
            records_in_set = round_down(self.set_length / data_set_len)
            record_count = 1            
            

            while record_count <= records_in_set:
                data_record = {}
                for index in list(set_template.keys()):
                    inf_element_id = set_template[index]["inf_elem_id"]
                    try:
                        field_name = inf_element_data[str(inf_element_id)]["name"]
                        abstract_data_type = inf_element_data[str(inf_element_id)]["abstract_data_type"]
                    except:
                        field_name = str(inf_element_id)
                        abstract_data_type = "unknown"
                    
                    data_len = set_template[index]["field_len"]
                    data = hexarr2int(packet_cursor, packet_cursor+data_len, self.set_bytes)
                    packet_cursor += data_len

                    if abstract_data_type == "ipv4Address":
                        data = format_ip_address(data)
                    elif abstract_data_type == "macAddress":
                        data = '{:012}'.format(hex(data)[2:].upper())

                    data_record[field_name] = data
                record_count += 1
                    
                self.data_records.append(data_record)

            return self.data_records