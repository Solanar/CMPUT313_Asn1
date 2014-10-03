import math


class Transmitter():
    r = 0

    def transmit(K, F):
        # special case, no HSBC applied
        if (K == 0):
            Transmitter.r = 0
            return F

        # add r checkbits to the F/K sized blocks
        # (F/K  +  r  +  1)  <=  2^r
        block_size = F / K
        new_r = int(math.log(block_size, 2))  # minimum
        while (block_size + new_r + 1 > 2 ** new_r):
            new_r += 1

        Transmitter.r = new_r

        new_block_size = int(block_size + new_r) + 1  # parity bit

        # return the new size of the K blocks
        return new_block_size
