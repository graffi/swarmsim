import sys, getopt, subprocess
from datetime import datetime
import os
import configparser
import components.generators.plot.plot_generator as pltgen


def main(argv):
    max_round = 100
    seed_start = 1
    seed_end = 5
    config = configparser.ConfigParser(allow_no_value=True)
    config.read("config.ini")

    try:
        scenario_file = config.get ("Simulator", "scenario")
    except (configparser.NoOptionError) as noe:
        scenario_file = "init_scenario.py"

    try:
        solution_file = config.get("Simulator", "solution")
    except (configparser.NoOptionError) as noe:
        solution_file = "solution.py"

    n_time = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')[:-1])

    # n_time = datetime.now().strftime('%Y-%m-%d_%H')[:-1]
    try:
        opts, args = getopt.getopt(argv, "hs:w:r:n:v:", ["scenaro=", "solution="])
    except getopt.GetoptError:
        print('Error: multiple.py -r <randomeSeed> -w <scenario> -s <solution> -n <maxRounds>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('multiple.py -ss <seed_start> -se <seed_end> -w <scenario> -s <solution>  -n <maxRounds>')
            sys.exit()
        elif opt in ("-s", "--solution"):
            solution_file = arg
        elif opt in ("-w", "--scenario"):
            scenario_file = arg
        elif opt in ("-ss", "--seed_start"):
            seed_start = int(arg)
        elif opt in ("-se", "--seed_end"):
            seed_end = int(arg)
        elif opt in ("-n", "--maxrounds"):
            max_round = int(arg)

    direction = "./outputs/multiple/" + n_time + "_" + scenario_file.rsplit('.', 1)[0] + "_" + \
          solution_file.rsplit('.', 1)[0]

    if not os.path.exists(direction):
        os.makedirs(direction)
    out = open(direction + "/multiprocess.txt", "w")
    child_processes = []
    process_cnt=0
    for seed in range(seed_start, seed_end+1):
        process ="python", "swarm-sim.py", "-n"+ str(max_round), "-m 1", "-d"+n_time, "-r"+ str(seed), "-v" + str(0)
        p = subprocess.Popen(process, stdout=out, stderr=out)
        child_processes.append(p)
        process_cnt += 1
        print("Process Nr. ", process_cnt, "started")
        if len(child_processes) == os.cpu_count():
            for cp in child_processes:
                cp.wait()
            child_processes.clear()

    for cp in child_processes:
        cp.wait()
    fout = open(direction+"/all_aggregates.csv","w+")
    for seed in range(seed_start, seed_end+1):
        f = open(direction+"/"+str(seed)+"/aggregate_rounds.csv")
        if seed != seed_start:
            f.__next__() # skip the header
        for line in f:
            fout.write(line)
        f.close() # not really needed
    fout.close()

    all_plot_generator(direction)

def all_plot_generator(directory):
    # def plotter(data, name, x_index, y_start, plot_dir):
    with open(directory + "/" + "all_aggregates.csv", 'r') as data:
        pltgen.plotter(data, "simulations", 2, 2, directory + "/all")


if __name__ == "__main__":
    main(sys.argv[1:])

