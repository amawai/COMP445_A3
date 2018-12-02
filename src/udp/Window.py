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
        return [packet for packet in self.window if packet.seq_num in self.valid_sequence_nums()]

    def get_window_data(self, seq_num):
        if seq_num in self.valid_sequence_nums():
            for packet in self.window:
                if packet.seq_num == seq_num:
                    return packet
        return None

    #Returns finished frames
    def slide_window(self, ack_seq_num):
        if ack_seq_num in self.valid_sequence_nums():
            num_frames_to_slide = ((ack_seq_num - self.current_seq_start) % self.max_seq_num) + 1
            finished_frames = [num % self.max_seq_num for num in range(self.current_seq_start, self.current_seq_start + num_frames_to_slide)]
            next_current_seq = (self.current_seq_start + num_frames_to_slide) % self.max_seq_num 
            new_data_index = min(len(self.data), self.data_index + num_frames_to_slide)
            self.current_seq_start = next_current_seq
            self.window = [packet for packet in self.data[self.data_index : new_data_index + 1]]
            self.data_index = new_data_index
            return finished_frames
        if self.data_index == len(self.data):
            self.complete = True
        return []

    def valid_sequence_nums(self):
        all_valid_sequence_nums = [num % self.max_seq_num for num in range(self.current_seq_start, self.current_seq_start + self.window_size)]
        valid_window_length = len(self.data[self.data_index : min(self.data_index + self.window_size, len(self.data))])
        return all_valid_sequence_nums[:valid_window_length]