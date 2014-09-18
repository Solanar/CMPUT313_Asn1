
class Statistics():
    Correct = "Correct"
    Error = "Error"
    statistics_dict = {
        Correct: 0,
        Error: 0
    }

    def update(statistic_type):
        Statistics.statistics_dict[statistic_type] += 1

    def print_all():
        print("Statistics:")
        for name, num in Statistics.statistics_dict.items():
            print("Name:", name, "\tNumber:", num)
