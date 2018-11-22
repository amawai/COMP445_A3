MAX_PAYLOAD_SIZE = 10

class DataConverter:
    @staticmethod
    def convert_data_to_packets(data):
        return [data[i:i+MAX_PAYLOAD_SIZE] for i in range(0, len(data.encode()), MAX_PAYLOAD_SIZE)] 
