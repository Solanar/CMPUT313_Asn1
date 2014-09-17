import sys

from transmitter import Transmitter
from simulate_transmission import Simulator
from receiver import Receiver
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
        transmission = Transmitter.transmit()
        simulated_transmission = Simulator.simulate(transmission)
        try:
            Receiver.receive(simulated_transmission)
            Statistics.update(Statistics.Correct)
        except Exception as e:  # create exceptions based on results
            print(e)
            # Statistics.update("Resend")
            # Statistics.update("Error")
            #pass

    Statistics.print_all()


if __name__ == "__main__":
    start()
