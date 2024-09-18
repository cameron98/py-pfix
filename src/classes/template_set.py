from utils import hexarr2int

class TemplateSet:

    def __init__(self, set_bytes) -> None:

        self.set_bytes = set_bytes
        self.set_id = hexarr2int(0, 2, self.set_bytes)
        self.set_length = hexarr2int(2, 4, self.set_bytes)
        self.template_id = hexarr2int(4, 6, self.set_bytes)
        self.field_count = hexarr2int(6, 8, self.set_bytes)
        self.template = {}
        print(f"Template Set received with Template ID: {self.template_id}")

    def parse(self):

        field_cursor = 0
        packet_cursor = 8

        while field_cursor < self.field_count:

            inf_elem_block = hexarr2int(packet_cursor, packet_cursor+2, self.set_bytes)
            enterprise_bit = '{0:016b}'.format(inf_elem_block)[0]
            inf_elem_id = int('{0:016b}'.format(inf_elem_block)[1:],2)
            packet_cursor += 2
            if enterprise_bit == '0':
                ent_num = False
            elif enterprise_bit == '1':
                ent_num = True
            else:
                print('ERROR - You should not be seeing this message....')
            field_len = hexarr2int(packet_cursor, packet_cursor+2, self.set_bytes)
            packet_cursor += 2
            if ent_num:
                enterprise_num = hexarr2int(packet_cursor, packet_cursor+4, self.set_bytes)
                packet_cursor = packet_cursor + 4
            else:
                enterprise_num = 0
            field_data = {
                "inf_elem_id": inf_elem_id,
                "field_len": field_len,
                "enterprise_num": enterprise_num
            }
            self.template[field_cursor] = field_data
            field_cursor += 1

        return self.template
    
    def get_data_set_len(self):

        if self.template == {}:
            raise Exception("Cannot get set length on template which has not been parsed.")
        
        length = 4
        for index in self.template:
            length += self.template[index]["field_len"]
            
        return length
            