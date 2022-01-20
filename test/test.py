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
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from omronfins.datacreator import DataCreator
from omronfins.finsudp import FinsUDP


class TestCase0(unittest.TestCase):
    """!
    # Test for cmronfins
    ## Test cases
    - [x] test01: create header from destination info and source info.
    - [x] test02: create memory area read command
    - [x] test03: convert text data in resnpose msg
    - [x] test04: create command to write mem area
    """
    def setUp(self):
        self.data_creator = DataCreator(
                src_net_addr=0,
                src_node_num=170,
                src_unit_addr=0,
                srv_id=0)
    
    def test01(self):
        header = self.data_creator._create_header(
                dst_net_addr=0,
                dst_node_num=239,
                dst_unit_addr=11)
        self.assertEqual(header, b'\x80\x00\x02\x00\xef\x0b\x00\xaa\x00\x00')
    
    def test02(self):
        self.data_creator.set_destination(
                dst_net_addr=0,
                dst_node_num=239,
                dst_unit_addr=11)
        data = self.data_creator.command_read_mem_area(
                90, 0, 0, 1)
        self.assertEqual(data, b'\x80\x00\x02\x00\xef\x0b\x00\xaa\x00\x00\x01\x01Z\x00\x00\x00\x00\x01')
        
    def test03(self):
        test_response = b'\x80\x00\x02\x00\xef\x0b\x00\xaa\x00\x00\x01\x01\x00\x00\x00\x01'
        fmt = [(DataCreator.BYTES, 12),
               (DataCreator.USHORT, 2)]
        data = self.data_creator.convert_ascii2data(
                test_response, fmt)
        self.assertEqual(data[1:], (0, 1))

    def test04(self):
        self.data_creator.set_destination(
                dst_net_addr=0x0,
                dst_node_num=0x2,
                dst_unit_addr=0x12)
        data = self.data_creator.command_write_mem_area(
                90, 0, 0, 1, (5, DataCreator.USHORT))
        self.assertEqual(
                data, b'\x80\x00\x02\x00\x02\x12\x00\xaa\x00\x00\x01\x02Z\x00\x00\x00\x00\x01\x00\x05')

    def test05(self):
        self.data_creator.set_destination(
                dst_net_addr=0,
                dst_node_num=13,
                dst_unit_addr=0)
        comm = self.data_creator.command_read_mem_area(0xA0, 500, 0, 1)
        self.assertEqual(
                comm, b'\x80\x00\x02\x00\r\x00\x00\xaa\x00\x00\x01\x01\xa0\x01\xf4\x00\x00\x01')

    def tearDown(self):
        pass

class TestCase1(unittest.TestCase):
    """!
    # Tester for FinsUDP.
    This test can work with real PLC.
    - [x] test01: reading words from a memory.
    - [x] test02: writing word to a memory.
    - [x] test03: reading bits from a memory.
    """
    def setUp(self):
        self.fins = FinsUDP(0, 170)
        ret = self.fins.open('192.168.2.13', 9600)
        self.assertEqual(ret, 0)
        self.fins.set_destination(
                dst_net_addr=0,
                dst_node_num=13,
                dst_unit_addr=0)

    def test01(self):
        ret = self.fins.read_mem_area(0xA0, 500, 0, 4)
        self.assertEqual(ret[0], 0)

    def test02(self):
        ret = self.fins.write_mem_area(
                0xA0, 500, 0, 4, [(0, DataCreator.USHORT)]*4)
        ret, value1 = self.fins.read_mem_area(0xA0, 500, 0, 4)
        ret = self.fins.write_mem_area(
                0xA0, 500, 0, 4, [(3, DataCreator.USHORT)]*4)
        ret, value2 = self.fins.read_mem_area(0xA0, 500, 0, 4)
        self.assertEqual(value2, (3, 3, 3, 3))
        
    def test03(self):
        ret = self.fins.read_mem_area(0x20, 500, 0, 2)
        print(ret)
        self.assertEqual(ret[0], 0)

    def tearDown(self):
        self.fins.close()

if __name__ == '__main__':
    unittest.main()
