from classes.server import IPFixCollector
#Config Variables
port = 5000
ipfix_inf_filename = 'ipfix-information-elements.csv'
dataset_buffer_max_len = 100


if __name__ == "__main__":

    print("---Starting Server---")

    server = IPFixCollector(port=port, ipfix_inf_filename=ipfix_inf_filename, buffer_max_len=dataset_buffer_max_len)
    server.start()
        