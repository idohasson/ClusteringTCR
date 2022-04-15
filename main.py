import csv
import itertools
import sys
import networkx as nx
from itertools import combinations


def get_data(file_path, nrow=1000000000, read_col=1, min_size=5):
    sequence_collection = dict()
    with open(file_path, "r") as csvfile:
        data_reader = csv.reader(csvfile)
        next(data_reader)  # the header row
        for row in data_reader:
            aa_seq = row[read_col]
            if isinstance(aa_seq, str):
                seq_len = len(aa_seq)
                if seq_len >= min_size:
                    if seq_len not in sequence_collection:
                        sequence_collection[seq_len] = set()
                    sequence_collection[seq_len].add(aa_seq)
    return sequence_collection

# create a network graph
def get_graph(sequence_collection, gap=False, min_size=5):

    def get_edges(sequence_set_lis, edge_weight):
        return [(u, v, edge_weight) for seq_set in sequence_set_lis for u, v in
                itertools.combinations(seq_set, 2)]

    def get_gaps(minus_one_seq, subs_table, gap_i):
        gaps = minus_one_seq.intersection(subs_table.keys())
        return [(v, u, gap_i) for u in gaps for v in subs_table[u]]

    G = nx.Graph()
    for l in sequence_collection.keys():
        # s_dict = []
        # g_dict = []

        for i, distance_one_sequences in minus_one_subsequences(sequence_collection[l], l):
            # cluster sequences by a single substitution and optional single gap
            edge_list = get_edges(distance_one_sequences.values(), i)
            # s_dict.append(len(edge_list))
            gap_list = []

            if l - 1 in sequence_collection and gap:
                gap_list = get_gaps(sequence_collection[l - 1], distance_one_sequences, i)
                edge_list.extend(gap_list)
            # g_dict.append(len(gap_list))
            G.add_weighted_edges_from(edge_list)


        # print(l, g_dict)



    return G


def get_edges(sequence_set_lis):
    return [(u, v) for seq_set in sequence_set_lis for u, v in itertools.combinations(seq_set, 2)]


def minus_one_subsequences(same_length_sequences, sequence_length):
    # substring of a string without the char in index i
    def subsequence(s, i):
        return s[:i] + s[i + 1:]

    def subsequences_table(sequences, sub_seqs):
        subs_table = dict()
        for sub_seq, full_seq in zip(sub_seqs, sequences):
            subs_table.setdefault(sub_seq, set()).add(full_seq)
        return subs_table

    for i in range(sequence_length):
        subs = [subsequence(seq, i) for seq in same_length_sequences]
        subs_table = subsequences_table(same_length_sequences, subs)
        yield i, subs_table


def main(input_path, output_path="output3.edgelist.gz"):
    # read datasets
    dataset = get_data(input_path, min_size=5)
    # create a network graph
    G = get_graph(dataset, gap=True)
    # print(*G.edges(data=True), sep='\n')
    # write graph to file

    nx.write_edgelist(G, output_path, data=["mismatch", "gap"])

if __name__ == '__main__':
    i_path = sys.argv[1]
    o_path = sys.argv[2]
    main(i_path)
