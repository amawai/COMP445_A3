from DataConverter import DataConverter

#Window will have as data a list of Packets
#TODO: TIMEOUTS, and where to put the Window
#TODO: where to send these things
#TODO: What are the relevance of frames
#TODO: Three way handshake
class Window:
    def __init__(self, data, max_seq_num):
        self.data = data
        self.data_index = 0
        self.current_seq_num = 0
        self.max_seq_num = max_seq_num
        #deal with even and odd numbers later
        self.window_size = int(max_seq_num / 2)
        self.window_start = 0
        self.window_end = int(self.window_size)
        self.window = [None for i in range(self.max_seq_num)]
        self.populate_window(self.window_size)
    
    def get_all_window_data(self):
        return self.window

    def get_window_data(self, index):
        return self.window[index]

    def slide_window(self, slide_num):
        self.window_start = (self.window_start + slide_num) % self.max_seq_num
        self.window_end = (self.window_end + slide_num) % self.max_seq_num
        self.populate_window(slide_num)
        #TODO: When all data is sent, notify that it is complete

    def populate_window(self, number_of_windows):
        data = self.data
        for i in range(0, number_of_windows):
            if (self.data_index < len(data)):
                window_data = data[self.data_index]
                window_data.set_seq_num(self.current_seq_num)
                self.window[self.current_seq_num] = window_data
                self.increase_current_seq_num()
                self.increase_data_index()
            else:
                self.window[self.current_seq_num] = None
    
    def increase_current_seq_num(self):
        self.current_seq_num = (self.current_seq_num + 1) % self.max_seq_num

    def increase_data_index(self):
        self.data_index += 1


data = ["data0", "data1", "data2", "data3", "data4", "data5", "datalol", "data7"]
window = Window(data, 4)
print(window.get_all_window_data())
print('SLINDING BY 2')
window.slide_window(2)
print(window.get_all_window_data())
print('SLINDING BY 2')
window.slide_window(2)
print(window.get_all_window_data())
print('SLINDING BY 1')
window.slide_window(1)
print(window.get_all_window_data())


window.slide_window(2)
print(window.get_all_window_data())