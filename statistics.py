
class Statistics():
    no_error = "No Error"
    one_bit_error = "One Bit Error"
    multiple_bit_errors = "Multiple Bit Errors"
    block_errors = "Block Errors"
    total_transmitions = "Total Transmitions"
    statistics_dict = {
        no_error: 0,
        one_bit_error: 0,
        multiple_bit_errors: 0,
        block_errors: 0,
        total_transmitions: 0
    }

    def update(statistic_type):
        Statistics.statistics_dict[statistic_type] += 1

    def print_all():
        print("Statistics:")
        for name, num in Statistics.statistics_dict.items():
            print("Name:", name, "\tNumber:", num)
