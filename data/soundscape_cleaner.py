import csv

if __name__ == '__main__':

    # read a line from the file
    with open('../data/raw-data/sample_soundscape.csv', 'rw' ) as input_file:
        csv_file = csv.DictReader(input_file)
        # need to tell CSV file there is a header
