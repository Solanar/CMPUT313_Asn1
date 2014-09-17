import sys

from .transmitter import Transmitter
from .simulated_transmitter import Simulator
from .receiver import Receiver
from .statistics import Statistics


def start():
    first_arg = sys.argv[1]
    t_arg = sys.argv[2]  # Change position
    print("Parameters:", first_arg)

    for i in range(t_arg):
        transmission = Transmitter.transmit()
        simulated_transmission = Simulator.simulate(transmission)
        try:
            Receiver.receive(simulated_transmission)
            Statistics.update("Correct")
        except:  # create exceptions based on results
            # Statistics.update("Resend")
            # Statistics.update("Error")
            pass
        Statistics.print_all()


if __name__ == "__main__":
    start()
