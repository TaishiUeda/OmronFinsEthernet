#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2022 Taishi Ueda <taishi.ueda@gmail.com>
#
"""!datacreator
@brief Data creator for Omron FINS protocol.
"""
import struct
import binascii
import socket
from .datacreator import DataCreator as datadef


class FinsAbstruct():
    """!
    Send and receive FINS commands.
    """
    def __init__(self, src_net_addr, src_node_num, src_unit_addr=0, srv_id=0):
        """!Initializer
        @param[in] src_net_addr Source network address.
            Specify within the following ranges.
            - 0x00: Local netwotk
            - 0x01 to 0x7F: Remote netwotk (1 to 127 decimal)
        @param[in] src_node_num Source node number.
            Specify within the following ranges.
            - 0x01 to 0x7E: Node number in SYSMAC NET network (1 to 126 decimal)
            - 0x01 to 0x3E: Node number in SYSMAC LINK network (1 to 62 decimal)
            - 0xFF: Broadcast transmission
        @param[in] src_unit_addr Source unit address.
            Specify within the following ranges
            - 0x00: PC (CPU)
            - 0xFE: SYSMAC NET Link Unit or SYSMAC LINK Unit connected to network
            - 0x10 to 0x1F: CPU Bus Unit (10 + unit number in hexadecimal
            Note: The unit address for a CPU Bus Unit is 10 (hexadecimal) plus the unit number set on the front panel of the CPU Bus Unit.
        @param[in] src_id Service ID. Used to identify the processing generating the transmission.
            Set the SID to any number between 0x00 and 0xFF
        """
        self._sock = None
        self._ip_addr = "localhost"
        self._port = 9600
        self._datacreator = datadef(
                src_net_addr, src_node_num, src_unit_addr, srv_id)

    def close(self):
        if self._sock is not None:
            self._sock.close()

    def open(self, ip_addr, port=9600):
        """
        This function must be overriten by sub-classes.
        """
        return -1

    def set_destination(self, dst_net_addr, dst_node_num, dst_unit_addr=0, delay=2):
        """!
        Set destination of message.
        You have to execute this function once before 
        @param[in] dst_net_addr Destination network address.
            Specify within the following ranges.
            - 0x00: Local netwotk
            - 0x01 to 0x7F: Remote netwotk (1 to 127 decimal)
        @param[in] dst_node_num Destination node number.
            Specify within the following ranges.
            - 0x01 to 0x7E: Node number in SYSMAC NET network (1 to 126 decimal)
            - 0x01 to 0x3E: Node number in SYSMAC LINK network (1 to 62 decimal)
            - 0xFF: Broadcast transmission
        @param[in] dst_unit_addr Destination unit address.
            Specify within the following ranges
            - 0x00: PC (CPU)
            - 0xFE: SYSMAC NET Link Unit or SYSMAC LINK Unit connected to network
            - 0x10 to 0x1F: CPU Bus Unit (10 + unit number in hexadecimal
            Note: The unit address for a CPU Bus Unit is 10 (hexadecimal) plus the unit number set on the front panel of the CPU Bus Unit.
        @param[in] delay It is possible to specify the response delay of a PC in 10-ms increments.
            Selecting 0 through F in hexadecimal sets the time required for a PC to respond
            to the host computer after the PC receives a command block from the host computer.
            Example:
                If F (15 in decimal) is set, there will be a delay of 150 ms before the response is sent.
        @return bytes encoded header
        """
        return self._datacreator.set_destination(
            dst_net_addr, dst_node_num, dst_unit_addr, delay)

    def read_mem_area(self, mem_area, addr, bit, num, dtype):
        """!
        Read data from memory areas.
        @param[in] mem_area memory area type defined in the 
           FINS manual. All of the types are pronounsed in
           thisfile (datacreator.py).
        @param[in] addr address in the memory area.
        @param[in] bit Bit of the address. If the memory area type
           is not bit type, this argument is ignored.
        @param[in] num byte/word size of data to be read.
        @param[in] dtype data type of read data.
        @return (return_id, data) 
            - return_id indicates errors. 0 means no probrem.
                the others means some error and it defined in
                FINS reference manual.
            - data a value of a tuple of values. It relay on the
                data length wheather it becomes a value or a tuple.
        """
        msg = self._datacreator.command_read_mem_area(
                mem_area, addr, bit, num)
        ret_id, bin_msg = self._send_and_recv(msg)
        if ret_id < 0:
            return ret_id, None
        return self._datacreator.decode_read_data(bin_msg, dtype)

    def write_mem_area(self, mem_area, addr, bit, num, values):
        """!
        @param[in] mem_area memory area type defined in the 
           FINS manual. All of the types are pronounsed in
           thisfile (datacreator.py).
        @param[in] addr address in the memory area.
        @param[in] bit Bit of the address. If the memory area type
           is not bit type, this argument is ignored.
        @param[in] num byte/word size of data to be written.
        @param[in] values values to be written. They are defined
           as followings.
           [(value, type_of_value), ...].
           Example.
           [(5, finsudp.datadef.USHORT)]*4 means four values of
           unsigned short are written into the memory area.
        @return  return_id 0 means no probrem.
                the others means some error and it defined in
                FINS reference manual.
        """
        msg = self._datacreator.command_write_mem_area(
                mem_area, addr, bit, num, values)
        ret_id, bin_msg = self._send_and_recv(msg)
        return self._datacreator.decode_read_data(
                bin_msg, datadef.CHAR)[0]

    def _send_and_recv(self, msg):
        """
        This function must be overriten by sub-classes.
        """
        return -10, ()


class FinsUDP(FinsAbstruct):
    """!
    Send and receive FINS commands via UDP.
    """
    def __init__(self, src_net_addr, src_node_num, src_unit_addr=0, srv_id=0):
        super().__init__(src_net_addr, src_node_num, src_unit_addr, srv_id)

    def open(self, ip_addr, port):
        """!
        @param[in] ip_addr IP address of PLC
        @param[in] port port number of PLC
        @retval 0 No problem
        @retval -1 timeout
        @retval -2 socket error
        """
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._ip_addr = ip_addr
        self._port = port
        try:
            self._sock.settimeout(5)
            self._sock.connect((self._ip_addr, self._port))
        except socket.timeout:
            return -1
        except socket.error:
            return -2
        return 0

    def _send_and_recv(self, msg):
        """!
        @param[in] msg binary message to be sent
        @retval 0 No problem
        @retval -1 send timeout
        @retval -2 send socket error
        @retval -3 receive timeout
        @retval -4 receive socket error
        """
        try:
            self._sock.settimeout(1)
            self._sock.sendall(msg)
        except socket.timeout:
            return -1, None
        except socket.error:
            return -2, None
        try:
            self._sock.settimeout(1)
            res_data = self._sock.recv(4096)
        except socket.timeout:
            return -3, None
        except socket.error:
            return -4, None
        return len(res_data), res_data

    

