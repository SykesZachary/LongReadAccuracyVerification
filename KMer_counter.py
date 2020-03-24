### Script to count specified number of K-Mers in a specified file
### 17.03.2020

def kmer_read_counter(sequence, kmer, read_lst, read_name):
    test_seq = sequence

    kmer_lst = []
    read_lst = []

    # Loop to take all 3-Mers out of test_seq
    bp = 0
    kmer_test_spec = kmer  # SPECIFY THE K-MER LENGTH HERE
    while bp < len(test_seq) - (kmer_test_spec - 1):  # Right of the < ensures an incorrect k-mer length isn't read
        kmer_seq_move = bp + kmer_test_spec  # Ensures the K-Mer length is kept consistent
        kmer_selector = test_seq[bp:kmer_seq_move]
        # print(KMer_selector) # Output test
        if len(kmer_selector) == kmer_test_spec:
            read_lst.append(kmer_selector)
            bp += 1
        else:
            print('The K-Mer', kmer_selector,
                  'did not meet the specified length of: ', kmer_test_spec)
            break
        kmer_lst.append(read_lst)
    # print(kmer_lst) # Output test
    print('There are', len(read_lst), str(kmer_test_spec) + '-mers in', read_name)
