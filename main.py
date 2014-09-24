import sys

from transmitter import Transmitter
from simulate_transmission import Simulator
from receiver import Receiver, Error
from statistics import Statistics


def start():
    A = 'A'  # Feedback time in bit_time_units
    K = 'K'  # Number of blocks frame is broken into
    F = 'F'  # Frame size (in bits)
    E = 'E'  # Probability of a bit error
    R = 'R'  # Simulation length in bit_time_units
    T = 'T'  # Trials
    # Todo: also accept the T seeds for the trial

    parameter_dict = {
        A: 500,
        K: 400,
        F: 4000,
        E: 0.00015,
        R: 400000,
        T: 5
    }
    # fill parameter_dict with arguments
    parameter_dict[A] = int(sys.argv[1])
    parameter_dict[K] = int(sys.argv[2])
    parameter_dict[F] = int(sys.argv[3])
    parameter_dict[E] = float(sys.argv[4])
    parameter_dict[R] = int(sys.argv[5])
    parameter_dict[T] = int(sys.argv[6])
    print("Parameters:")
    for name, value in parameter_dict.items():
        print("Name:", name, "\tValue:", value)
    print()

    # for T trials, repeat the simulation
    for i in range(parameter_dict[T]):
        print("Simulating", str(i))
        # Transmitter.transmit returns the new size of a block
        new_block_size = Transmitter.transmit(i, parameter_dict[K],
                                parameter_dict[F])

        block_errors = 0
        # Simulator.simulate returns the number of bit erors in each block
        for j in range(0, parameter_dict[K]):
            bit_errors = Simulator.simulate(new_block_size, parameter_dict[E])
            if(bit_errors != 0):
                block_errors += 1
                # TODO: Resend the block at the receiver
        print(block_errors,"of", parameter_dict[K],"blocks transmited an error")

        try:
            Receiver.receive(bit_errors)
            Statistics.update(Statistics.Correct)
            print(Statistics.Correct)
        except Error:
            Statistics.update(Statistics.Error)
            print(Statistics.Error)
        except Exception as e:  # create exceptions based on results
            print("Other Exception", e)
            # Statistics.update("Resend")

            #pass
    print()

    Statistics.print_all()
    # TODO: Determine average number of frame transmitions (total / received)
    # Determine the throughput ( (F x recieved) / total_time_required)
    # Determine the confidence interval
        # Determing mean of averages above (sum(X) \ T)
        # Determine S.D. s = root(sum(x-X)^2 / (T-1))
        # Determine C.I. from T-Distribution (t = 2.776 gives us % C.I.)
            #  c = X [+-] 2.776(s/root(T))
    # Graph the shite out of it (throughput vs E for differing values of K)
    # Tables where possible (at least w/ averages and C.I.)
    # Discussion of the results with varied inputs (possibly ideal values?)


if __name__ == "__main__":
    start()
