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
    """!datacreator
    @brief Data creator for Omron FINS protocol.
    """
    ## type indicator for struct
    BIT = ('B', 1)  # The bit is imput as a unsigned char in fins protocol
    CHAR = ('c', 1)
    SCHAR = ('b', 1)
    UCHAR = ('B', 1)
    SHORT = ('h', 2)
    USHORT = ('H', 2)
    INT = ('i', 4)
    UINT = ('I', 4)
    LONG = ('l', 4)
    ULONG = ('L', 4)
    LONGLONG = ('q', 8)
    ULONGLONG = ('Q', 8)
    FLOAT = ('f', 4)
    DOUBLE = ('d', 8)
    STR = ('s', 1)
    BYTES = ('p', 1)
    ## Memory type definition. 
    ## First element of each tuples is type definition according to the fins manual.
    ## Second is size of one element of data.
    CIO_BIT = (0x30, 1)
    WR_BIT = (0x31, 1)
    HR_BIT = (0x32, 1)
    AR_BIT = (0x33, 1)
    CIO_FORCE_BIT = (0x70, 1)
    WR_FORCE_BIT = (0x71, 1)
    HR_FORCE_BIT = (0x72, 1)
    CIO_WORD = (0xb0, 2)
    WR_WORD = (0xb1, 2)
    HR_WORD = (0xb2, 2)
    AR_WORD = (0xb3, 2)
    CIO_FORCE_WORD = (0xf0, 4)
    WR_FORCE_WORD = (0xf1 , 4)
    HR_FORCE_WORD = (0xf2 , 4)
    TIM_FLG = (0x09, 1)
    TIM_FORCE_FLG = (0x49, 1)
    TIM_CURRENT = (0x89, 2)
    DM_BIT = (0x02, 1)
    DM_WORD = (0x82, 1)
    EM0_BIT = (0x20, 1)
    EM1_BIT = (0x21, 1)
    EM2_BIT = (0x22, 1)
    EM3_BIT = (0x23, 1)
    EM4_BIT = (0x24, 1)
    EM5_BIT = (0x25, 1)
    EM6_BIT = (0x26, 1)
    EM7_BIT = (0x27, 1)
    EM8_BIT = (0x28, 1)
    EM9_BIT = (0x29, 1)
    EMA_BIT = (0x2a, 1)
    EMB_BIT = (0x2b, 1)
    EMC_BIT = (0x2c, 1)
    EMD_BIT = (0x2d, 1)
    EME_BIT = (0x2e, 1)
    EMF_BIT = (0x2f, 1)
    EM10_BIT = (0xe0, 1)
    EM11_BIT = (0xe1, 1)
    EM12_BIT = (0xe2, 1)
    EM13_BIT = (0xe3, 1)
    EM14_BIT = (0xe4, 1)
    EM15_BIT = (0xe5, 1)
    EM16_BIT = (0xe6, 1)
    EM17_BIT = (0xe7, 1)
    EM18_BIT = (0xe8, 1)
    EM0_WORD = (0xa0, 2)
    EM1_WORD = (0xa1, 2)
    EM2_WORD = (0xa2, 2)
    EM3_WORD = (0xa3, 2)
    EM4_WORD = (0xa4, 2)
    EM5_WORD = (0xa5, 2)
    EM6_WORD = (0xa6, 2)
    EM7_WORD = (0xa7, 2)
    EM8_WORD = (0xa8, 2)
    EM9_WORD = (0xa9, 2)
    EMA_WORD = (0xaa, 2)
    EMB_WORD = (0xab, 2)
    EMC_WORD = (0xac, 2)
    EMD_WORD = (0xad, 2)
    EME_WORD = (0xae, 2)
    EMF_WORD = (0xaf, 2)
    EM10_WORD = (0x60, 2)
    EM11_WORD = (0x61, 2)
    EM12_WORD = (0x62, 2)
    EM13_WORD = (0x63, 2)
    EM14_WORD = (0x64, 2)
    EM15_WORD = (0x65, 2)
    EM16_WORD = (0x66, 2)
    EM17_WORD = (0x67, 2)
    EM_CURRENT_BIT = (0x0a, 1)
    EM_CURRENT_WORD = (0x98, 2)
    EM_CURRENT_BUNK_NUM = (0xbc, 2)
    TK_BIT = (0x06, 1)
    TK_STATUS = (0x46, 1)
    IR = (0xdc, 4)
    DR = (0xbc, 2)
    CLOCK = (0x07, 1)

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
                data_bin = a_data[0]
            elif a_data[1] == DataCreator.STR:
                data_bin = a_data[0][::-1].encode('utf-8')
            else:
                data_bin = struct.pack('!'+a_data[1][0], a_data[0])
            data_size = len(data_bin)
            # If the data is loger than 16bit 1element,
            # it must be swapped to be read correctory by PLC
            if data_size > 2 and a_data[1] != DataCreator.BYTES:
                # set length dividable by two
                if data_size%2 != 0:
                    data_inv = b'\x00' + data_bin
                    data_size += 1
                else:
                    data_inv = data_bin
                ushorts = struct.unpack(
                        '!'+str(data_size//2)+'H', data_inv)
                ushorts_swapped = ushorts[::-1]
                data_bin = struct.pack(
                        '!'+str(data_size//2)+'H', *ushorts_swapped)
            out_bin += data_bin
        return out_bin

    def decode_read_data(self, data, dtype):
        """! Decode received data.
        @param[in] data bytes data received.
        @param[in] dtype type of data. If received data is longer than
           the input data type, then tuple of values as the data type
           will be returned.
        """
        ret_id = struct.unpack('!H', data[12:14])[0]
        if len(data) < 14:
            return ret_id, None
        values = data[14:]
        if dtype == DataCreator.STR or dtype[1] > 2:
            num_elem = len(values)//2
            ushorts = struct.unpack("!"+str(num_elem)+'H', values)
            ushorts_swapped = ushorts[::-1]
            data_bin = struct.pack('!'+str(num_elem)+'H', *ushorts_swapped)
        else:
            data_bin = values
        num_elem = len(data_bin)//dtype[1]
        unpacked = struct.unpack("!"+str(num_elem)+dtype[0], data_bin)
        if dtype == DataCreator.STR:
            decoded = unpacked[0][::-1].decode('utf-8')
            return ret_id, decoded.partition('\x00')[0]
        if len(unpacked) == 1:
            unpacked = unpacked[0]
        return ret_id, unpacked

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
        """!
        @param[in] mem_area memory area type defined in the 
           FINS manual. All of the types are pronounsed in
           thisfile (datacreator.py).
        @param[in] addr address in the memory area.
        @param[in] bit Bit of the address. If the memory area type
           is not bit type, this argument is ignored.
        @param[in] num byte/word size of data to be read.
        @return bytes fins binary message.
        """
        fmt = [
                (b'\x01\x01', DataCreator.BYTES),
                (mem_area[0], DataCreator.UCHAR),
                (addr, DataCreator.USHORT),
                (bit, DataCreator.UCHAR),
                (num, DataCreator.USHORT)]
        return self._header_bin + self._convert_data2ascii(fmt)

    def command_write_mem_area(self, mem_area, addr, bit, num, data):
        """!
        @param[in] mem_area memory area type defined in the 
           FINS manual. All of the types are pronounsed in
           thisfile (datacreator.py).
        @param[in] addr address in the memory area.
        @param[in] bit Bit of the address. If the memory area type
           is not bit type, this argument is ignored.
        @param[in] num byte/word size of data to be written.
        @param[in] data data to be written.
        @return bytes fins binary message.
        @retval None number and length of data are mismatch.
        """
        fmt = [
                (b'\x01\x02', DataCreator.BYTES),
                (mem_area[0], DataCreator.UCHAR),
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

    
