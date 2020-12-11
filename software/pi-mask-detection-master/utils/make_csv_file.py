"""
Script to generate the CSV file required by AutoML vision to retrain a model.

The CSV format must be:
[set,]image_path[,label]
TRAIN, gs://my_bucket/sample_1, cat
TEST, gs://my_bucket/sample_2, dog

"""
import os
import csv

BUCKET = "gs://pi-mask-detection-vcm"  # TODO: Use your bucket name
out_file = "/path/to/dataset/all_data.csv"  # TODO: Fix with your dataset path

data_dir = "dataset"
mask = "mask"
no_mask = "no_mask"

mask_path = "/path/to/dataset/with_mask"  # TODO: Fix with your dataset path
no_mask_path = "/path/to/dataset/with_mask"  # TODO: Fix with your dataset path


def main():
    with open(out_file, "w", newline="") as csv_file:
        w = csv.writer(csv_file, delimiter=",")
        w.writerow(["image_path", "label"])
        for f in os.listdir(mask_path):
            if f == ".DS_store":  # ignore mac OS files
                continue
            w.writerow([BUCKET + "/with_mask/" + f, "mask"])

        for f in os.listdir(no_mask_path):
            if f == ".DS_store":
                continue
            w.writerow([BUCKET + "/without_mask/" + f, "no_mask"])


if __name__ == "__main__":
    main()
