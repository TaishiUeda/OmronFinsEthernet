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


class DataCreator():
    CHAR = 'c'
    SCHAR = 'b'
    UCHAR = 'B'
    SHORT = 'h'
    USHORT = 'H'
    INT = 'i'
    UINT = 'I'
    LONG = 'l'
    ULONG = 'L'
    LONGLONG = 'q'
    ULONGLONG = 'Q'
    FLOAT = 'f'
    DOUBLE = 'd'
    STR = 's'
    BYTES = 's'

    def __init__(self, src_net_addr=0, src_node_num=0, src_unit_addr=0, srv_id=0):
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
        self._src_net_addr = src_net_addr
        self._src_node_num = src_node_num
        self._src_unit_addr = src_unit_addr
        self._srv_id = srv_id
        self._header_bin = None
        self.set_destination(0, 0)

    def set_destination(self, dst_net_addr, dst_node_num, dst_unit_addr=0, delay=2):
        """!
        Create header data for a message according to source information and
        destination information input as arguments.
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
        self._header_bin = self._create_header(dst_node_num, dst_unit_addr, dst_net_addr, delay)

    def _convert_data2ascii(self, data):
        """!
        convert data according to format.
        @param data formatted data as a list contains tuples of (value, type, size).
            size is needed for only string;
            Example:
                [(90, DataCreator.ULONG),
                 (0, DataCreator.USHORT),
                 ('A', DataCreator.CHAR),
                 (b'Hoge', DataCreator.STR)]
        @return bytes
        """
        out_bin = b''
        for a_data in data:
            if a_data[1] == DataCreator.BYTES:
                out_bin += a_data[0]
            elif a_data[1] == DataCreator.STR:
                out_bin += a_data[0].encode('utf-8')
            else:
                out_bin += struct.pack('!'+a_data[1], a_data[0])
        return out_bin

    def convert_ascii2data(self, data, fmt):
        """!
        convert ascii data according to format.
        @param data formatted data as a list contains tuples of (type, size).
        @return tuple of values
        """
        # bin_data = binascii.a2b_hex(data)
        bin_data = data
        whole_fmt = "!"
        for a_fmt in fmt:
            if a_fmt[1] == 1:
                whole_fmt += a_fmt[0]
            else:
                whole_fmt += str(a_fmt[1]) + a_fmt[0]
        return struct.unpack(whole_fmt, bin_data)

    def _create_header(self, dst_node_num, dst_unit_addr, dst_net_addr=0, delay=2):
        fmt = [
                (b'\x80\x00\x02', DataCreator.BYTES),
                (dst_net_addr, DataCreator.UCHAR),
                (dst_node_num, DataCreator.UCHAR),
                (dst_unit_addr, DataCreator.UCHAR),
                (self._src_net_addr, DataCreator.UCHAR),
                (self._src_node_num, DataCreator.UCHAR),
                (self._src_unit_addr, DataCreator.UCHAR),
                (self._srv_id, DataCreator.UCHAR)]
        return self._convert_data2ascii(fmt)

    def command_read_mem_area(self, mem_area, addr, bit, num):
        fmt = [
                (b'\x01\x01', DataCreator.BYTES),
                (mem_area, DataCreator.UCHAR),
                (addr, DataCreator.USHORT),
                (bit, DataCreator.UCHAR),
                (num, DataCreator.USHORT)]
        return self._header_bin + self._convert_data2ascii(fmt)

    def command_write_mem_area(self, mem_area, addr, bit, num, data):
        fmt = [
                (b'\x01\x02', DataCreator.BYTES),
                (mem_area, DataCreator.UCHAR),
                (addr, DataCreator.USHORT),
                (bit, DataCreator.UCHAR),
                (num, DataCreator.USHORT)]
        if isinstance(data, list):
            if num != len(data):
                return None
            for a_data in data:
                fmt.append((a_data[0], a_data[1]))
        else:
            fmt.append((data[0], data[1]))
        return self._header_bin + self._convert_data2ascii(fmt)

    def __del__(self):
        """!Destructor
        """
        pass


if __name__ == "__main__":
    import argparse
    import sys

    
