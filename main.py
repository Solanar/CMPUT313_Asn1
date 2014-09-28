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
        while (time <= parameter_dict[R]):
            # Transmitter.transmit returns the new size of a block
            new_block_size = Transmitter.transmit(i, parameter_dict[K],
                                                  parameter_dict[F])
            # Time += F (bits) + A (responseOverhead)
            if (parameter_dict[K] == 0):
                #time += parameter_dict[F] + parameter_dict[A]
                handle_block(new_block_size, parameter_dict[E],
                             parameter_dict[K])
                Statistics.update(Statistics.correctly_received_frames)
                # Move these to Statistics if you want/need to
                trials_received_frames += 1
            else:
                for j in range(0, parameter_dict[K]):
                    #time += new_block_size + parameter_dict[A]
                    handle_block(new_block_size, parameter_dict[E],
                                 parameter_dict[K])
                Statistics.update(Statistics.correctly_received_frames)
                trials_received_frames += 1
                #print("Time left", time, "Value", Simulator.seed)
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
    while(1):
        time += new_block_size + parameter_dict[A]
        # Simulator.simulate returns the number of bit erors in each block
        bit_errors = Simulator.simulate(new_block_size, E)
        Statistics.update(Statistics.total_transmitions)
        if(bit_errors != 0):
            Statistics.update(Statistics.block_errors)
        try:
            Receiver.receive(bit_errors)
            Statistics.update(Statistics.no_error)
            #print(Statistics.no_error)
            break
        except OneBitError:
            Statistics.update(Statistics.one_bit_error)
            #print(Statistics.one_bit_error)
            if (K != 0):
                # fix error (add time units?)
                break
        except MultipleBitErrors:
            Statistics.update(Statistics.multiple_bit_errors)
            #print(Statistics.multiple_bit_errors)

if __name__ == "__main__":
    start()
