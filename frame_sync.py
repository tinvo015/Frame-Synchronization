#!/usr/bin/env python
from gnuradio import gr
from gnuradio import blocks
from gnuradio import digital
import numpy

class frame_sync(gr.basic_block):
    
    def __init__(self):
        gr.basic_block.__init__(self, name="frame_sync",
            in_sig=[numpy.uint8],
            out_sig=[numpy.uint8])


    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        
        
        nitems_written = 0  # Number of items written

        out = output_items[0]
        
        barker_code = [-1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1]
        

        
        flag = False
        start = 0
        stop = 13

 
        ninput_items = len(in0)
       
        
        nitems_read = 0     # Number of items read

        
        while(stop < ninput_items):
            nitems_read = nitems_read + 1
            
            
            #Find cross correlation
            temp_array = in0[start:stop]
            temp_array = temp_array.astype(numpy.int32) * 2 - 1
            correlation = numpy.correlate(temp_array, barker_code)

                
            if (correlation[0] == 13):
                flag = True
                start = start + 13
                nitems_read = nitems_read + 13
                stop = stop + 13

            
            if (flag and len(out[:]) > start):
                out[nitems_written] = in0[start]
                nitems_written = nitems_written + 1


            start = start + 1
            stop = stop + 1
            nitems_read = nitems_read + 1 
            
                         
        self.consume_each(nitems_read)
        return nitems_written


