class Window:
    def __init__(self, data, max_seq_num):
        self.data = data
        self.max_seq_num = max_seq_num
        self.window_size = int(self.max_seq_num / 2)
        self.current_seq_start = 0
        self.data_index = 0
        self.window = [packet for packet in self.data[0 : min(len(self.data), self.window_size)]]
        self.complete = False
  
    def get_all_window_data(self):
        return [packet for packet in self.window]

    def get_window_data(self, seq_num):
        converted_index = (self.current_seq_start - seq_num) % self.window_size
        return self.window[converted_index]

    def slide_window(self, ack_seq_num):
        print('received ACK', ack_seq_num)
        if self.data_index == len(self.data):
            self.complete = True
        elif ack_seq_num in self.valid_sequence_nums():
            num_frames_to_slide = ((ack_seq_num - self.current_seq_start) % self.max_seq_num) + 1
            next_current_seq = (self.current_seq_start + num_frames_to_slide) % self.max_seq_num 
            new_data_index = min(len(self.data), self.data_index + num_frames_to_slide)
            self.current_seq_start = next_current_seq
            self.window = [packet for packet in self.data[self.data_index : new_data_index + 1]]
            self.data_index = new_data_index

    def valid_sequence_nums(self):
        return [num % self.max_seq_num for num in range(self.current_seq_start, self.current_seq_start + self.window_size)]