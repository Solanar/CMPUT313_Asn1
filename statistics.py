import math


class Statistics():
    no_error = "No Error"
    one_bit_error = "One Bit Error"
    multiple_bit_errors = "Multiple Bit Errors"
    block_errors = "Block Errors"
    total_transmitions = "Total Block Transmitions"
    correctly_received_frames = "Correctly Received Frames"
    correctly_received_blocks = "Correctly Received Blocks"
    throughput_averages = "Throughput averages"
    statistics_dict = {
        no_error: 0,
        one_bit_error: 0,
        multiple_bit_errors: 0,
        block_errors: 0,
        total_transmitions: 0,
        correctly_received_frames: 0,
        correctly_received_blocks: 0,
        throughput_averages: []
    }

    def append(statistic_type, value):
        Statistics.statistics_dict[statistic_type].append(value)

    def update(statistic_type):
        Statistics.statistics_dict[statistic_type] += 1

    def print_all():
        print("Statistics:")
        for name, num in Statistics.statistics_dict.items():
            print(name, "\t=", num)
        Statistics.print_average()

    # Average block Transmitions
    def print_average():
        print("Average Block Transmitions:")
        if(Statistics.statistics_dict
           [Statistics.correctly_received_blocks] != 0):
            print(Statistics.statistics_dict[Statistics.total_transmitions] /
                  Statistics.statistics_dict
                  [Statistics.correctly_received_blocks],
                  "sent/received")
        else:
            print("No blocks received. No average available.")

    # Total throughput after all T trials
    def print_throughput(F, R, T):
        print("Throughput: (this doesnt feel right)")
        print((F * Statistics.statistics_dict
              [Statistics.correctly_received_frames]) / (R*T), "bits/time")

    # Confidence Interval after all trials
    def print_ci(F, R, T):

        print("Mean of Averages (Accruate after all T trials):")
        mean_of_averages = math.fsum(Statistics.statistics_dict
                                     [Statistics.throughput_averages])/T

        SSD = 0  # Sum of the Squared Distances
        for trial_average in (Statistics.statistics_dict
                              [Statistics.throughput_averages]):
            SSD += math.pow(trial_average - mean_of_averages, 2)

        std_dev = math.sqrt(SSD/(T-1))
        # 2.776 is the t-distribution with 95% confidence
        ci_low = mean_of_averages - (2.776 * (std_dev / math.sqrt(T)))
        ci_high = mean_of_averages + (2.776 * (std_dev / math.sqrt(T)))
        print("Confidence Interval after all trials")
        print("[", ci_low, ",", ci_high, "]")

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
