import csv
import sys
import networkx as nx


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


def no_gap(seq_len_table):
    # substring of a string without the char in index i
    def subsequence(s, i):
        return s[:i] + s[i + 1:]

    # dictionary of all the subsequences as a key to the full sequence
    def table_i(sequences, sub_i):
        subs_table = dict()
        for sub_seq, full_seq in zip([subsequence(seq, sub_i) for seq in sequences], sequences):
            subs_table.setdefault(sub_seq, set()).add(full_seq)
        return subs_table

    # all buckets contain more than one sequence
    def more_than_one(subs_table):
        return [sub_seq for sub_seq in subs_table if len(subs_table[sub_seq]) > 1]

    # loop in descending order of dataset keys
    for l in range(len(seq_len_table), 0, -1):
        print("size:", l)
        for i in range(l):
            if seq_len_table[l]:
                Tli = table_i(seq_len_table[l], i)
                print("table size:", len(more_than_one(Tli)))
    return []


def main(input_path, output_path, no_gap=True, none_or_2_gaps=True, up_to_1_gap=True, up_to_2_gaps=True):
    # substring of a string without the char in index i
    def subsequence(s, i):
        return s[:i] + s[i + 1:]

    # dictionary of all the subsequences as a key to the full sequence
    def table_i(sequences, sub_i):
        subs_table = dict()
        for sub_seq, full_seq in zip([subsequence(seq, sub_i) for seq in sequences], sequences):
            subs_table.setdefault(sub_seq, set()).add(full_seq)
        return subs_table

    # all buckets contain more than one sequence
    def more_than_one(subs_table):
        return [sub_seq for sub_seq in subs_table if len(subs_table[sub_seq]) > 1]

    dataset = get_data(input_path, min_size=5)

    # loop in descending order of dataset keys
    for l in dataset.keys():
        for i in range(l):
            # One Substitution
            Tli = table_i(dataset[l], i)
            # One Gap
            if l-1 in dataset:
                gap_sequences = dataset[l - 1].intersection(Tli.keys())
                for gap_seq in gap_sequences:
                    Tli[gap_seq].add(gap_seq)

            cliques = more_than_one(Tli)

            print("size:", l, "i:", i, "cliques:", len(cliques))


if __name__ == '__main__':
    i_path = sys.argv[1]
    o_path = sys.argv[2]
    main(i_path, o_path)
