import csv
import os
import re
from csv import DictReader


class CrossrefCSVs:
    def __init__(self, path, pattern):
        self.path = path
        self.pattern = pattern
        self.matching = self.__find_csvs()
        self.dois_and_urls = self.__read_csvs()

    def __find_csvs(self):
        return [f for f in os.listdir(self.path) if re.match(self.pattern, f)]

    def __read_csvs(self):
        values = []
        for csv in self.matching:
            with open(os.path.join(self.path, csv), 'r') as csvfile:
                reader = DictReader(csvfile)
                for row in reader:
                    if row['url'] != "":
                        values.append({'doi': row['doi'], 'url': row['url']})
        return values


class TraceCSV:
    def __init__(self, path, matches):
        self.path = path
        self.matches =matches
        self.finals = self.process()

    def process(self):
        finals = []
        with open(self.path, 'r') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                if row['doi'] != "":
                    value = row['doi']
                else:
                    trace_path = row['calc_url']
                    value = ""
                    for match in self.matches:
                        if match['url'] == trace_path:
                            value = f"https://doi.org/{match['doi']}"
                finals.append(value)
        return finals

    def write(self):
        with open('dois_for_trace.txt', 'w') as dois_for_trace:
            for doi in self.finals:
                dois_for_trace.write(f"{doi}\n")


if __name__ == "__main__":
    x = CrossrefCSVs('csvs/ijns_vol8', 'IJNS*')
    t = TraceCSV('csvs/ijns_1.xls_Tue_Feb_06_06_10_39_2024part_1.csv', x.dois_and_urls)
    t.write()