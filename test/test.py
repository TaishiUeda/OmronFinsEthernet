#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Taishi Ueda <taishi.ueda@gmail.com>
#
# Distributed under terms of the MIT license.
import unittest
import time
import os
import sys
from fins import udp
import fins
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from omronfins.datacreator import DataCreator


class TestCase0(unittest.TestCase):
    """!
    # Test for cmronfins
    ## Test cases
    - [x] test01: create header from destination info and source info.
    - [x] test02: create memory area read command
    - [x] test03: check if the command code in response
        is corespondance to sent message.
    - [x] test04: convert text data in resnpose msg
    - [ ] test05: create command to write mem area
    """
    def setUp(self):
        self.data_creator = DataCreator(
                src_net_addr=1,
                src_node_num=1,
                src_unit_addr=0,
                srv_id=0)
    
    def test01(self):
        header = self.data_creator._create_header(
                dst_net_addr=0,
                dst_node_num=239,
                dst_unit_addr=11)
        self.assertEqual(header, b'80000200ef0b00020000')
    
    def test02(self):
        self.data_creator.set_destination(
                dst_net_addr=0,
                dst_node_num=239,
                dst_unit_addr=11)
        data = self.data_creator.command_read_mem_area(
                90, 0, 0, 1)
        self.assertEqual(data, b'80000200ef0b0002000001015a0000000001')
        
    def test03(self):
        self.data_creator.set_destination(
                dst_net_addr=0,
                dst_node_num=239,
                dst_unit_addr=11)
        test_response = b'80000200ef0b0002000001015a5a29'
        is_to_me = self.data_creator.is_response_to_me(test_response)
        self.assertTrue(is_to_me)

    def test04(self):
        test_response = b'80000200ef0b00020000010101010001'
        fmt = [(DataCreator.BYTES, 10),
               (DataCreator.USHORT, 3)]
        data = self.data_creator._convert_ascii2data(
                test_response, fmt)
        self.assertEqual(data[1:], (257, 257, 1))

    def test05(self):
        self.data_creator.set_destination(
                dst_net_addr=0x0,
                dst_node_num=0x2,
                dst_unit_addr=0x12)
        data = self.data_creator.command_write_mem_area(
                90, 0, 0, 1, (5, DataCreator.USHORT))
        print(data)

    def test06(self):
        ret = self.data_creator.open("192.168.2.13", 9600)
        self.assertEqual(ret, 0)
        self.data_creator.set_destination(
                dst_net_addr=1,
                dst_node_num=2,
                dst_unit_addr=0)
        comm = self.data_creator.command_read_mem_area(0xA0, 500, 0, 1)
        print(comm)
        data = self.data_creator.exec_read_mem_area(0xA0, 500, 0, 1)
        print(data)
        res = self.data_creator._convert_ascii2data(
            data[1], [(DataCreator.CHAR, 14)])
        print(res)
        ret = self.data_creator.close()

    def test07(self):
        fins_instance = udp.UDPFinsConnection()
        fins_instance.connect('192.168.2.13')
        #i don't know what i had to write in this fields
        fins_instance.dest_node_add= 0x01
        #i don't know what i had to write in this fields
        fins_instance.srce_node_add= 0x02
         
        mem_area = fins_instance.memory_area_read(b'\xA0')
        print(mem_area)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
