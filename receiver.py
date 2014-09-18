

class Receiver():

    def receive(simulated_transmission):
        if simulated_transmission == 0:  # arbitrary, need to check for error
            raise Error
        elif simulated_transmission == 1:
            raise Exception
        elif simulated_transmission == 2:
            pass  # Correct


class Error(Exception):
    pass
