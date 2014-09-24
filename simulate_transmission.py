import random

class Simulator():

    def simulate(new_block_size, E):

        bit_errors = 0
        # for each bit in the block
        for j in range(0, new_block_size):
            randomError = random.random()
            # if an error occured
            if(randomError < E):
                bit_errors += 1

        return bit_errors
