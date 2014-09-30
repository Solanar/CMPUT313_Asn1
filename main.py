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
    R = 'R'  # Simulation length in bit_trials_time_units
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

    # Transmitter.transmit returns the new size of a block
    new_block_size = Transmitter.transmit(parameter_dict[K],
                                          parameter_dict[F])
    # for T trials, repeat the simulation
    for i in range(parameter_dict[T]):
        # clear this trial's variables
        trials_time = 0
        trials_received_frames = 0
        trials_failed_frames = 0
        trials_received_blocks = 0
        trials_failed_blocks = 0
        # Set the first seed for the simulation
        Simulator.set_seed(parameter_dict[TSeeds][i])
        while (trials_time <= parameter_dict[R]):
            # set the number of blocks to be transmitted in this frame
            transmitions = parameter_dict[K]
            if (parameter_dict[K] == 0):
                transmitions = 1
            # For K blocks (or 1 if K = 0), simulate the transmition
            for j in range(0, transmitions):
                # frame_failure = 0 if block was transmitted successfully
                block_failure = handle_block(new_block_size,
                                             parameter_dict[E],
                                             parameter_dict[K])
                # record block success or failure
                if(block_failure > 0):
                    trials_failed_blocks += 1
                else:
                    trials_received_blocks += 1
            # set trials_time to number of bits and response overhead
            trials_time += (parameter_dict[F]) + parameter_dict[A]
            # update number of transmitted frames
            Statistics.update(Statistics.total_frames)
            # frame failed, resend the frame
            if(trials_failed_blocks > 1):
                trials_failed_frames += 1
            # the last frame being sent
            #elif(trials_time > parameter_dict[R]):
            #    pass
            # successful transmition
            else:
                Statistics.update(Statistics.correctly_received_frames)
                trials_received_frames += 1

        print("Trial number:", i)
        print("Received Frames", trials_received_frames)
        print("Failed Frames", trials_failed_frames)

        # Assume: Take all K*(F+r) trials_time units into account
        # even if in last frame
        Statistics.append(Statistics.throughput_averages,
                          (parameter_dict[K] * new_block_size *
                           trials_received_frames) / trials_time)

        if(trials_received_frames != 0):
            # Assume: Take all frames into account, even last frame
            Statistics.append(Statistics.frame_averages,
                              (trials_received_frames + trials_failed_frames) /
                              (trials_received_frames))
        else:
            Statistics.append(Statistics.frame_averages, 0)
        if(trials_received_blocks != 0):
            # Assume: Take all blocks into account, even if in last frame
            Statistics.append(Statistics.block_averages,
                             (trials_received_blocks + trials_failed_blocks) /
                             (trials_received_blocks))
        else:
            Statistics.append(Statistics.block_averages, 0)

    # Call Print Statements
    print()
    print("----------------------------------------------")
    print_input(sys.argv)
    Statistics.set_final_values(parameter_dict[F], parameter_dict[R])
    Statistics.print_frame_ci()
    Statistics.print_throughput_ci()
    print("----------------------------------------------")
    #Statistics.print_block_ci()
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
            # Assume: Fixing the error requires 0 trials_time units
            return 0
        return bit_errors
    except MultipleBitErrors:
        Statistics.update(Statistics.multiple_bit_errors)
        return bit_errors


def print_input(args):
    # Remove the first "main.py" element
    args.pop(0)
    input_string = ""
    for arg in args:
        input_string += " " + str(arg)
    # Remove leading whitespace
    input_string = input_string[1:]
    print(input_string)

if __name__ == "__main__":
    start()
