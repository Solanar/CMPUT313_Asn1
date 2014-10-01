import random


class Simulator():

    def set_seed(new_seed):
        Simulator.seed = new_seed
        random.seed(Simulator.seed)
        #print("Seed: " + str(Simulator.seed))

    def simulate(new_block_size, E):
        bit_errors = 0
        # Todo: This may be the wrong way to do it...
        # well it's not done properly but it works
        # once seed is set all .random() numbers will be the same
        # should only need to set .seed() once
        #random.seed(Simulator.seed)
        # for each bit in the block
        #totalRands = 0
        #first = True
        for j in range(new_block_size):  # range starts at 0
            randomError = random.random()
            # if (first):
            #     print("Rand: " + str(randomError))
            #     first = False
            #totalRands += 1
            # update seed
            #Simulator.seed = randomError
            #random.seed(Simulator.seed)
            # if an error occured
            if(randomError < E):
                bit_errors += 1

        #print("totalRands: " + str(totalRands))
        return bit_errors
