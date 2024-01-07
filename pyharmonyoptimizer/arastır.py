def parse_harmony_data(file_path):
    results = []
    with open(file_path, 'r') as file:
        for line in file:
            if 'Iteration' in line:
                parts = line.split(',')
                iteration = int(parts[0].split(' ')[1])
                fitness = float(parts[2].split(': ')[1])
                penalty = float(parts[3].split(': ')[1])
                results.append({'Iteration': iteration, 'Fitness': fitness, 'Penalty': penalty})
    return results
parse_harmony_data("en_iyi_sonuc103.txt")