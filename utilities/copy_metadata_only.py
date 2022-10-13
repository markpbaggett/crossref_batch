import os


def copy_metadata_files(path, filename_pattern, output):
    for path, directories, files in os.walk(path):
        for file in files:
            if file == filename_pattern:
                with open(f"{output}/{path.split('/')[-1]}.xml", 'w') as write_file:
                    with open(f"{path}/{file}", 'r') as read_file:
                        for line in read_file:
                            write_file.write(line)


if __name__ == "__main__":
    copy_metadata_files('/home/mark/PycharmProjects/crossref_journal_minting/', 'conf.xml', 'output')