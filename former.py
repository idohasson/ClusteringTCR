import csv
import itertools
import sys
import networkx as nx
from itertools import *
import time


def subsequence(s, i):
    return s[:i] + s[i + 1:]


def insert_subsequence(full_seq, l, subs_dict):
    for i in range(l):
        sub_seq = subsequence(full_seq, i)
        subs_dict.setdefault(sub_seq, set()).add(full_seq)


def main(input_path, output_path="output3.edgelist.gz", read_col=1):
    # read datasets
    subs_l = list(dict() for _ in range(100))
    with open(input_path, "r") as csvfile:
        data_reader = csv.reader(csvfile)
        next(data_reader)  # the header row
        a = 0
        for row in data_reader:
            aa_seq = row[read_col]
            aa_seq_len = len(aa_seq)
            insert_subsequence(aa_seq, aa_seq_len, subs_l[aa_seq_len])
            a += 1
            if a % 100000 == 0:
                print(a)


def main2(i_path):
    cid = 0
    clusters = []

    with open(i_path, "r") as csvfile:
        data_reader = csv.reader(csvfile)
        next(data_reader)  # the header row
        all_sequences = [(len(row[1]), row[1]) for row in data_reader]
        # sort by the first element of the tuple
        all_sequences.sort(key=lambda x: x[0])
        # group by the first element of the tuple and iterate over the groups
        for key, length_sorted_group in groupby(all_sequences, lambda x: x[0]):
            subsequences = [(i, (subsequence(seq, i), seq)) for l, seq in length_sorted_group for i in range(l)]
            # sort by the first element of the tuple
            subsequences.sort(key=lambda x: x[0])
            # group by the first element of the tuple and iterate over the groups
            for mm_i, sub_seq_i_group in groupby(subsequences, lambda x: x[0]):
                mismatches = dict()
                for _, (sub_seq, full_seq) in sub_seq_i_group:
                    mismatches.setdefault(sub_seq, set()).add(full_seq)

                # store sequences by their matching subsequences with the mismatch's index and cluster id
                for _, cluster in mismatches.items():
                    if len(cluster) > 1:
                        cluster_w = [cid, mm_i, cluster]
                        # cluster_w += list(cluster)
                        clusters.append(cluster_w)
                        cid += 1

                # # write to csv file
                # with open("output.csv", "a") as csvfile:
                #     writer = csv.writer(csvfile)
                #     writer.writerows(clusters)
                #

def main3(i_path):
    with open(i_path, "r") as csvfile:
        data_reader = csv.reader(csvfile)
        next(data_reader)  # the header row
        all_sequences = [list(row[1]) for row in data_reader]
        i = 3
        # crate a subsequence by removing th i caracter from the sequence


if __name__ == '__main__':
    i_path1 = sys.argv[1]
    o_path2 = sys.argv[2]
    o_path3 = sys.argv[3]
    # check run time
    # start_time = time.time()
    # main(i_path)
    # print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    main3(i_path1)
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    main3(o_path2)
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    main3(o_path3)
    print("--- %s seconds ---" % (time.time() - start_time))
