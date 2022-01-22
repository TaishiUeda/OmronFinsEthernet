# OmronFinsEthernet
Utility functions for FINS protocol used by omron's PLCs

This library can read and write memory area of PLC via FINS protocol.
It is confirmed that this can work with NX series PLC.

## Usage

Please refer to documents created by doxygen for the details.
When you access structs' data in PLC, please set memory offset 'CJ' mode.
And please notice that offset of structure is shown as number of bytes,
on the other hand, the number of address is defined as number of 16bit segments.
So, the address of data in a struct can be calculated by adding half number of the 
offset to the initial address of the struct.

It's a sample code.

```python
import omronfins.finsudp as finsudp
from omronfins.finsudp import datadef

fins = finsudp.FinsUDP(0, 170)
ret = fins.open('192.168.2.13', 9600)  # Please change according to your PLC's address.
fins.set_destination(dst_net_addr=0, dst_node_num=13, dst_unit_addr=0)

# Writing a word to Extended memory area's address 0.
ret = fins.write_mem_area(datadef.EM0_WORD, 0, 0, 1, (20, datadef.USHORT))

# Reading a word from Extended memory area's address 0.
ret, value = fins.read_mem_area(datadef.EM0_WORD, 0, 0, 1, datadef.USHORT)
print(value)  # the value becomes '20'

# Writing four bits to Extended memory area's address 5.
ret = fins.write_mem_area(datadef.EM0_BIT, 5, 0, 4,
    [(1, datadef.BIT), (0, datadef.BIT), (1, datadef.BIT), (0, datadef.BIT)])

# Reading four bits from Extended memory area's address 5.
ret, values = fins.read_mem_area(datadef.EM0_BIT, 5, 0, 4, datadef.BIT)
print(values)  # values become a tuple like (1, 0, 1, 0).

# Writing a string to Extended memory area's address 6.
# Fourth argument '4' means size of 16bit element and it becomes half of length of the string.
ret = fins.write_mem_area(datadef.EM0_WORD, 6, 0, 4, ("testtest", datadef.STR))

# Reading a string from Extended memory area's address 6.
ret, value = fins.read_mem_area(datadef.EM0_WORD, 6, 0, 4, datadef.STR)
print(value)  # value become "testtest"
```

