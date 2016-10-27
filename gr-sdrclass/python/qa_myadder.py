#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from myadder import myadder

class qa_myadder (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        # set up fg
	##################################################
	# Blocks
	##################################################
	self.vec_source_1 = blocks.vector_source_f((1,1,1,1,1), False, 1, [])
	self.vec_source_0 = blocks.vector_source_f((1,2,3,4,5), False, 1, [])
	self.my_sink = blocks.vector_sink_f(1)
	self.myadd = myadder()

	##################################################
	# Connections
	##################################################
	self.tb.connect((self.myadd, 0), (self.my_sink, 0))    
	self.tb.connect((self.vec_source_0, 0), (self.myadd, 0))    
	self.tb.connect((self.vec_source_1, 0), (self.myadd, 1))    

        self.tb.run ()
        expected = (2,3,4,5,6)
        # check data
        self.assertFloatTuplesAlmostEqual(expected,self.my_sink.data())


if __name__ == '__main__':
    gr_unittest.run(qa_myadder, "qa_myadder.xml")
