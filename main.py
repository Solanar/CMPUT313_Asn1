import sys

from transmitter import Transmitter
from simulate_transmission import Simulator
from receiver import Receiver, OneBitError, MultipleBitErrors
from statistics import Statistics


def start():

    A = 'A'  # Response overhead
    K = 'K'  # Number of blocks frame is broken into
    F = 'F'  # Frame size (in bits)
    E = 'E'  # Probability of a bit error
    R = 'R'  # Simulation length in bit_time_units
    T = 'T'  # Trials
    TSeeds = "T Seeds"

    parameter_dict = {
        A: 500,
        K: 400,
        F: 4000,
        E: 0.00015,
        R: 400000,
        T: 5,
        TSeeds: []
    }
    # fill parameter_dict with arguments
    parameter_dict[A] = int(sys.argv[1])
    parameter_dict[K] = int(sys.argv[2])
    parameter_dict[F] = int(sys.argv[3])
    parameter_dict[E] = float(sys.argv[4])
    parameter_dict[R] = int(sys.argv[5])
    parameter_dict[T] = int(sys.argv[6])
    for i in range(parameter_dict[T]):
        parameter_dict[TSeeds].append(int(sys.argv[6+i+1]))

    print("Parameters:")
    for name, value in parameter_dict.items():
        print("Name:", name, "\tValue:", value)
    print()

    # for T trials, repeat the simulation
    for i in range(parameter_dict[T]):
        time = 0
        trials_received_frames = 0
        # Set the first seed for the simulation
        Simulator.set_seed(parameter_dict[TSeeds][i])
        # Transmitter.transmit returns the new size of a block
        new_block_size = Transmitter.transmit(i, parameter_dict[K],
                                              parameter_dict[F])
        while (time <= parameter_dict[R]):
            # set the number of blocks to be transmitted in this frame
            transmitions = parameter_dict[K]
            if (parameter_dict[K] == 0):
                transmitions = 1
            # For K blocks (or 1 if K = 0), simulate the transmition
            j = 0
            while j < transmitions:
                # failure = 0 if block was transmitted successfully
                failure = handle_block(new_block_size,
                                       parameter_dict[E],
                                       parameter_dict[K])
                # increment time by number of bits and and response overhead
                time += (parameter_dict[F]/transmitions) + parameter_dict[A]
                # if out of time, stop transmitting blocks
                if(time > parameter_dict[R]):
                    break
                # if block failed, decrement counter j (retry)
                if(failure > 0):
                    j -= 1
                else:
                    pass
                # increment to the next block
                j += 1
            # if transmitions in this frame completed before time ran out
            if(time <= parameter_dict[R]):
                Statistics.update(Statistics.correctly_received_frames)
                trials_received_frames += 1

        print("Trial number:", i)
        #TODO remove comment when no longer the same every time
        print("Trials Received Frames", trials_received_frames)
        Statistics.append(Statistics.throughput_averages,
                          (parameter_dict[F] * trials_received_frames) /
                          parameter_dict[R])
    # test
    Statistics.print_ci(parameter_dict[F], parameter_dict[R],
                        parameter_dict[T])
    print()

    Statistics.print_all()


def handle_block(new_block_size, E, K):

    # Simulator.simulate returns the number of bit erors in each block
    bit_errors = Simulator.simulate(new_block_size, E)
    Statistics.update(Statistics.total_transmitions)
    if(bit_errors != 0):
        Statistics.update(Statistics.block_errors)
    try:
        Receiver.receive(bit_errors)
        Statistics.update(Statistics.no_error)
        Statistics.update(Statistics.correctly_received_blocks)
        return 0
    except OneBitError:
        Statistics.update(Statistics.one_bit_error)
        if (K != 0):
            Statistics.update(Statistics.correctly_received_blocks)
            # Assume: Fixing the error requires 0 time units
            return 0
        return bit_errors
    except MultipleBitErrors:
        Statistics.update(Statistics.multiple_bit_errors)
        return bit_errors

if __name__ == "__main__":
    start()
