#!/usr/bin/env python

import os
import sys
from gnuradio import gr
from gnuradio import blocks
from gnuradio import digital
from gnuradio import uhd
import string_to_list
from frame_sync import frame_sync

class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)

        ##################################################
        # Variables
        ##################################################       


        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0_0.set_clock_rate(30.72e6, uhd.ALL_MBOARDS)
        self.uhd_usrp_source_0_0.set_samp_rate(36e6)
        self.uhd_usrp_source_0_0.set_center_freq(5.42e9, 0)
        self.uhd_usrp_source_0_0.set_gain(5, 0)
        self.uhd_usrp_source_0_0.set_antenna("J1", 0)
        self.uhd_usrp_source_0_0.set_bandwidth(36e6, 0)



        self.input_unpacked_to_packed = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)

            
        self.demod = digital.gfsk_demod(
        	samples_per_symbol=2,
        	sensitivity=1.0,
        	gain_mu=0.175,
        	mu=0.5,
        	omega_relative_limit=0.005,
        	freq_error=0.0,
        	verbose=False,
        	log=False,
        ) 
        
        self.output_unpacked_to_packed = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)

        self.frame_sync = frame_sync()

        self.output_file_sink = blocks.file_sink(gr.sizeof_char*1, "output.txt", False)
        self.output_file_sink.set_unbuffered(True)
        
        ##################################################
        # Connections
        ##################################################
        self.connect(self.uhd_usrp_source_0_0, self.demod, self.frame_sync, self.output_unpacked_to_packed, self.output_file_sink)



if __name__ == '__main__':
    tb = top_block()
    tb.start()
    tb.wait()
    tb.run()
    tb.stop()

