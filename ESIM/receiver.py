

class Receiver():

    def receive(bit_errors):
        # no error, no need to resend
        if bit_errors == 0:
            pass
        # if (k!=0) fix the error using HSBC
        elif bit_errors == 1:
            raise OneBitError
        # resend the block
        elif bit_errors > 1:
            raise MultipleBitErrors


class OneBitError(Exception):
    pass


class MultipleBitErrors(Exception):
    pass
