import pickle
import os
import time
import pdb
import cv2

def get_all_images(dirs):
    img_paths = {}
    imgs = {}
    for ldir in dirs:
        for f in os.listdir(ldir):
            if ".jpeg" in f:
                path = ldir+"/"+f
                ts = f.replace("img_","").replace(".jpeg","")
                img_paths[float(ts)] = path
                imgs[float(ts)] = cv2.imread(path)
    return img_paths, imgs

def get_log_data(dirs):
    # key = timestamp, value = thrust, steer
    data ={}
    for ldir in dirs:
        for file in os.listdir(ldir):
            if "log" in file:
                path = ldir+"/"+file
                f = open(path, "rb")
                buf = pickle.load(f)
                f.close()
                for dpoint in buf:
                    data[dpoint["timestamp"]] = (dpoint["throttle"],
                                                    dpoint["steer"])
    return data

if __name__ == "__main__":
    log_dirs = ["/Users/gauravparmar/Desktop/CAR/DATA/LOG/f_table_0",
                "/Users/gauravparmar/Desktop/CAR/DATA/LOG/f_table_1"]
    logs = get_log_data(log_dirs)
    paths, imgs = get_all_images(log_dirs)
    dkeys = logs.keys()
    dkeys.sort()
    deltas = []
    DATASET = {"X":[], "Y":[], "X_paths":[]}
    # for every image, get the datapoint closest after the ts
    for key in imgs:
        ts = key
        lts = None
        for dts in dkeys:
            if dts>ts:
                if(abs(ts-dts) > 0.5):
                    lts = None
                else:
                    deltas.append(abs(ts-dts))
                    lts = dts
                break
        img = imgs[key]
        path = paths[key]
        if lts == None:
            continue
        log = logs[lts]
        DATASET["X"].append(img)
        DATASET["Y"].append(log)
        DATASET["X_paths"].append(path)
    pdb.set_trace()
    # cvs file where each line is <path> <throttle> <steer>
    f = open("table_data.txt","w")
    for i in range(len(DATASET["X"])):
        path = DATASET["X_paths"][i]
        throttle = DATASET["Y"][i][0]
        steer = DATASET["Y"][i][1]
        f.write("%s %f %f\n"%(path, throttle, steer))
    f.close()


