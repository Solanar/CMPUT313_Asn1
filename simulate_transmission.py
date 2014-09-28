import random


class Simulator():

    def set_seed(new_seed):
        Simulator.seed = new_seed

    def simulate(new_block_size, E):

        bit_errors = 0
        # Todo: This may be the wrong way to do it...
        random.seed(Simulator.seed)
        # for each bit in the block
        for j in range(0, new_block_size):
            randomError = random.random()
            # update seed
            Simulator.seed = randomError
            random.seed(Simulator.seed)
            print(randomError)
            # if an error occured
            if(randomError < E):
                bit_errors += 1

        return bit_errors
