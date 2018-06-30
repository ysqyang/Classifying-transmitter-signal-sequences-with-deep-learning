'''
script for converting original binary data files into one
binary file in which each record consists of one byte of label 
followed by a fixed number of bytes representing the sequence 
'''
import argparse
import os
import numpy as np
import run

_DISTANCES = [5, 10, 15, 20]

def convert(data_dir, out_file_name, num_sequences_per_file):   
    with open(out_file_name, mode='wb') as out_file:
        for i in range(run._NUM_CLASSES):
            for d in _DISTANCES:
                file_path = os.path.join(data_dir, 'data', str(i), 't{}_r1_{}m'.format(i+1, d))
                '''
                if data file does not contain enough bytes to extract
                num_sequences_per_file sequences of _DEFAULT_SEQUENCE_BYTES
                each, change num_sequences_per_file to fit the data file size 
                '''
                file_size = os.path.getsize(file_path)
                with open(file_path, mode='rb') as f:
                    for _ in range(num_sequences_per_file):
                        f.seek(2*np.random.randint(0, (file_size-run._RECORD_BYTES+1)//2))
                        sequence = f.read(run._RECORD_BYTES-1)
                        # add label to the front of each extracted sequence 
                        out_file.write(i.to_bytes(1, byteorder='little'))
                        out_file.write(sequence)  

    out_path = os.path.join(data_dir, out_file_name)
    print(os.path.getsize(out_path))

def main(args):
    convert(args.data_dir, args.out_file_name, args.num_sequences_per_file)

if __name__ == '__main__':  
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default=os.getcwd(), help='data file directory')
    parser.add_argument('--out_file_name', type=str, default='all_data', help='output file name')
    parser.add_argument('--num_sequences_per_file', type=int, default=25, help='number of sequences to extract from each data file')

    args = parser.parse_args()
    main(args)