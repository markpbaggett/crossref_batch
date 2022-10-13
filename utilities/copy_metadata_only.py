import os
from argparse import ArgumentParser


def copy_metadata_files(path, filename_pattern, output):
    for path, directories, files in os.walk(path):
        for file in files:
            if file == filename_pattern:
                with open(f"{output}/{path.split('/')[-1]}.xml", 'w') as write_file:
                    with open(f"{path}/{file}", 'r') as read_file:
                        for line in read_file:
                            write_file.write(line)


if __name__ == "__main__":
    parser = ArgumentParser(description="Copy metadata files from path recursively.")
    parser.add_argument(
        "-p",
        "--path_to_files",
        dest="path",
        help="Specify the path where you want to recursively copy files",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--filename_pattern",
        dest="filename_pattern",
        help="Specify the name of the file you are looking for.",
        default='metadata.xml'
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        help="Specify where you want to write files.",
        required=True
    )
    args = parser.parse_args()
    #copy_metadata_files('/home/mark/PycharmProjects/crossref_journal_minting/', 'conf.xml', 'output')
    copy_metadata_files(args.path, args.filename_pattern, args.output)