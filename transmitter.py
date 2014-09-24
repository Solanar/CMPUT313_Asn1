import math

class Transmitter():

    def transmit(input, K, F):
        # special case, no HSBC applied
        if(K == 0):
            return F

        # add r checkbits to the F/K sized blocks
        block_size = F/K
        r = math.floor(math.log(block_size,2)) + 1
        new_block_size = int(block_size + r)

        # return the new size of the K blocks
        return new_block_size
