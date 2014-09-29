import math


class Statistics():
    no_error = "No Error"
    one_bit_error = "One Bit Error"
    multiple_bit_errors = "Multiple Bit Errors"
    block_errors = "Block Errors"
    total_transmitions = "Total Block Transmitions"
    correctly_received_frames = "Correctly Received Frames"
    correctly_received_blocks = "Correctly Received Blocks"
    block_averages = "Block Averages"
    throughput_averages = "Throughput Averages"
    final_block_average = "Final Block Average"
    final_block_ci = "Final Block Confidence Interval"
    final_throughput = "Final Throughput"
    final_throughput_ci = "Final Throughput Confidence Interval"
    statistics_dict = {
        no_error: 0,
        one_bit_error: 0,
        multiple_bit_errors: 0,
        block_errors: 0,
        total_transmitions: 0,
        correctly_received_frames: 0,
        correctly_received_blocks: 0,
        block_averages: [],
        throughput_averages: [],

        final_block_average: 0,
        final_block_ci: '',
        final_throughput: 0,
        final_throughput_ci: ''
    }

    def append(statistic_type, value):
        Statistics.statistics_dict[statistic_type].append(value)

    def update(statistic_type):
        Statistics.statistics_dict[statistic_type] += 1

    def set_final_values(F, R):
        # 2.776 is the t-distribution value with 95% confidence
        confidence_value = 2.776
        T = len(Statistics.statistics_dict[Statistics.block_averages])
        if(Statistics.statistics_dict
           [Statistics.correctly_received_blocks] != 0):
            average = Statistics.statistics_dict[Statistics.total_transmitions] / Statistics.statistics_dict[Statistics.correctly_received_blocks]
            Statistics.statistics_dict[Statistics.final_block_average] = average
        else:
            Statistics.statistics_dict[Statistics.final_block_average] = 0

        mean_of_averages = (math.fsum(Statistics.statistics_dict
                                      [Statistics.block_averages]) / T)
        SSD = 0  # Sum of the Squared Distances
        for trial_average in (Statistics.statistics_dict
                              [Statistics.block_averages]):
            SSD += math.pow(trial_average - mean_of_averages, 2)

        std_dev = math.sqrt(SSD/(T-1))
        variance = (confidence_value * (std_dev / math.sqrt(T)))
        ci_low = str(mean_of_averages - variance)
        ci_high = str(mean_of_averages + variance)
        final_string = "(" + ci_low + ", " + ci_high + ")"

        Statistics.statistics_dict[Statistics.final_block_ci] = final_string

        T = len(Statistics.statistics_dict[Statistics.throughput_averages])
        throughput = ((F * Statistics.statistics_dict
                      [Statistics.correctly_received_frames]) / (R*T))
        Statistics.statistics_dict[Statistics.final_throughput] = throughput

        mean_of_averages = (math.fsum(Statistics.statistics_dict
                                      [Statistics.throughput_averages]) / T)
        SSD = 0  # Sum of the Squared Distances
        for trial_average in (Statistics.statistics_dict
                              [Statistics.throughput_averages]):
            SSD += math.pow(trial_average - mean_of_averages, 2)

        std_dev = math.sqrt(SSD/(T-1))
        variance = (confidence_value * (std_dev / math.sqrt(T)))
        ci_low = str(mean_of_averages - variance)
        ci_high = str(mean_of_averages + variance)
        final_string = "(" + ci_low + ", " + ci_high + ")"
        Statistics.statistics_dict[Statistics.final_throughput_ci] = final_string

    # Print all statistics variables stored
    def print_all():
        print("Statistics:")
        for name, num in Statistics.statistics_dict.items():
            print(name, "\t=", num)

    # Confidence Interval for throughput
    def print_block_ci():
        print(Statistics.statistics_dict[Statistics.final_block_average],
              Statistics.statistics_dict[Statistics.final_block_ci])

    # Confidence Interval for throughput
    def print_throughput_ci():
        print(Statistics.statistics_dict[Statistics.final_throughput],
              Statistics.statistics_dict[Statistics.final_throughput_ci])

    # Graph the shite out of it (throughput vs E for differing values of K)
    # Tables where possible (at least w/ averages and C.I.)
    # Discussion of the results with varied inputs (possibly ideal values?)
