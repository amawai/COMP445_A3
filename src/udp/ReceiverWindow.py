from .Packet import Packet

class ReceiverWindow:
    def __init__(self, max_seq_num):
        
        self.max_seq_num = max_seq_num
        self.window_size = int(self.max_seq_num / 2)
        self.current_seq_start = 0
        self.current_seq_end =(self.current_seq_start + self.window_size -1) % self.max_seq_num
        #self.data_index = 0
        self.window =  self.window_size * [None]
        self.complete = False
        self.got_last_pkt = False
        self.buffer = []
  
    def get_all_window_data(self):
        return [packet for packet in self.window]
    
            
    def slide(self,ack_num):
        buffer_length = len(self.buffer)
        temp_buffer_size = buffer_length
        #append acked packet in buffer
        for p in self.window:
            if p is not None:
                #first_index_in_window = buffer_length % self.max_seq_num
                if p.seq_num == ack_num:
                    self.buffer.append(p)
                    break
                if p.seq_num  < ack_num or p.seq_num  < ack_num + self.max_seq_num:
                    self.buffer.append(p)

        #delete from window    
        delete_window_element_index = buffer_length - temp_buffer_size
        while delete_window_element_index >0:
            self.window[0].pop
            delete_window_element_index -=1    
        while len(self.window) < 5:
            self.window.append(None)

        
                    



    # def return_current_seq_start(self):
    #     for p in self.window:
    #         if p is not None:
    #             self.current_seq_start = p.seq_num
    #             return self.current_seq_start

