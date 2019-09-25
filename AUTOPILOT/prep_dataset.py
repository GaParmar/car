import os
import sys
import numpy as np
import pickle 
import argparse
import pdb

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="unpack log pickle files")
    parser.add_argument("--log_dir", type=str, 
                        default="raw_data/test_verano_room_stand",
                        help="path to log pkl files")
    parser.add_argument("--output_dir", type=str,
                        default="prepared_data/",
                        help="the output directory with unpacked samples")
    args = parser.parse_args()

    # output dir
    args.output_dir = os.path.join(args.output_dir,
                        os.path.basename(os.path.abspath(args.log_dir)))

    log_files = []
    # get all pickle files
    for file in os.listdir(args.log_dir):
        if ".pkl" in file:
            log_files.append(os.path.join(args.log_dir, file))

    # make the output dir if it does not exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    for log_file in log_files:
        # unpickle the list of samples
        with open(log_file, "rb") as file:
            samples = pickle.load(file)
            for sample in samples:
                output_file = os.path.join(args.output_dir,
                                    "ts%f.pkl"%sample["timestamp"])
                with open(output_file, "wb") as f:
                    pickle.dump(sample, f)