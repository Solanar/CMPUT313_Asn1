import sys

from transmitter import Transmitter
from simulate_transmission import Simulator
from receiver import Receiver, Error
from statistics import Statistics


def start():
    T = 'T'
    First = 'First'
    parameter_dict = {
        First: "",
        T: ""
    }

    parameter_dict[First] = sys.argv[1]
    parameter_dict[T] = int(sys.argv[2])  # Change position

    print("Parameters:")
    for name, value in parameter_dict.items():
        print("Name:", name, "\tValue:", value)
    print()

    for i in range(parameter_dict[T]):
        print("Simulating", str(i))
        transmission = Transmitter.transmit(i)
        simulated_transmission = Simulator.simulate(transmission)
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
