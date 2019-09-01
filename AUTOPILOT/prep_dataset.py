import os
import sys
import numpy as np
import pickle 
import argparse
import pdb

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="unpack log pickle files")
    parser.add_argument("--log_dir", type=str, 
                        default="data/session_1",
                        help="path to log pkl files")
    parser.add_argument("--output_dir", type=str,
                        default="prepared_data/session_1",
                        help="the output directory with unpacked samples")
    args = parser.parse_args()

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
            pdb.set_trace()
            for sample in samples:
                output_file = os.path.join(args.output_dir,
                                    "ts%f.pkl"%sample["timestamp"])
                with open(output_file, "wb") as f:
                    pickle.dump(sample, f)