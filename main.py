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
    T = 'T'  # Change position

    parameter_dict = {
        A: 500,
        K: 0,
        F: 4000,
        E: 0.0015,
        R: "",
        T: 5
    }

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

    for i in range(parameter_dict[T]):
        print("Simulating", str(i))
        # Transmitter.transmit returns the new size of a block
        new_block_size = Transmitter.transmit(i, parameter_dict[K],
                                parameter_dict[F])
        simulated_transmission = Simulator.simulate(new_block_size,
                                parameter_dict[K], parameter_dict[E])
        try:
            Receiver.receive(simulated_transmission)
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


if __name__ == "__main__":
    start()
