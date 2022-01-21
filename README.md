# OmronFinsEthernet
Utility functions for FINS protocol used by omron's PLCs

This library can read and write memory area of PLC via FINS protocol.
It is confirmed that this can work with NX series PLC.

## Usage

```python
import omronfins.finsudp as finsudp
from omronfins.finsudp import datadef

fins = finsudp.FinsUDP(0, 170)
ret = fins.open('192.168.255.2', 9600)  # Please change according to your PLC's address.
fins.set_destination(dst_net_addr=0, dst_node_num=2, dst_unit_addr=0)

# Writing four words to Extended memory area's address 53.
ret = fins.write_mem_area(datadef.EM0_WORD, 53, 0, 4, (20, datadef.USHORT))

# Reading four words from Extended memory area's address 53.
ret, value = fins.read_mem_area(datadef.EM0_WORD, 53, 0, 4, datadef.USHORT)
# the value becomes '20'

# Writing four bits to Extended memory area's address 53.
ret = fins.write_mem_area(datadef.EM0_BIT, 57, 0, 4,
    [(1, datadef.BIT), (0, datadef.BIT), (1, datadef.BIT), (0, datadef.BIT)])

# Reading four words from Extended memory area's address 53.
ret, values = fins.read_mem_area(datadef.EM0_BIT, 57, 0, 4, datadef.BIT)
# values become a tuple like (1, 0, 1, 0).

# Writing a string to Extended memory area's address 60.
# Fourth argument '4' means size of 16bit element and it becomes half of length of the string.
ret = fins.write_mem_area(datadef.EM0_BIT, 60, 0, 4, ("testtest", datadef.STR))

# Reading four words from Extended memory area's address 53.
ret, value = fins.read_mem_area(datadef.EM0_BIT, 57, 0, 4, datadef.STR)
# value become "testtest"
```

