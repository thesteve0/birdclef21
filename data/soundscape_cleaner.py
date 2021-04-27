import csv

if __name__ == '__main__':

    # read a line from the file
    with open('../data/raw-data/train_soundscape_labels.csv', 'r' ) as io_file:
        csv_file = csv.DictReader(io_file)
        with open('../data/raw-data/cleaned_train_soundscape.csv', 'w', newline= '') as output:
            linewriter = csv.DictWriter(output, csv_file.fieldnames)
            linewriter.writeheader()
            for i, line in enumerate(csv_file):

                # turn the bird array string into a proper python list
                bird_list = line['birds'].split(" ")

                # now turn the list into a literal string
                line['birds'] = str(bird_list)

                # now make the array markers work for postgreSQL \copy commands  { }
                line['birds'] = line['birds'].replace('[', '{').replace(']', '}')

                linewriter.writerow(line)

        output.close()
    io_file.close()
