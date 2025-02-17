# This is provided to you so that you can test your bst.py file with a particular tracefile.

import argparse
import csv
import es

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-tf', '--tracefile')
    args = parser.parse_args()
    tracefile = args.tracefile

    with open(tracefile, "r") as f:
        print("Running!")
        reader = csv.reader(f)
        lines = [l for l in reader]
        for l in lines:
            if l[0] == 'esinit':
                t = es.EStack(int(l[1]),int(l[2]))
            if l[0] == 'espush':
                t.espush(int(l[1]))
            if l[0] == 'espop_quiet':
                t.espop_quiet()
            if l[0] == 'espop':
                print(t.espop())
            if l[0] == 'esdump':
                print(t.esdump())