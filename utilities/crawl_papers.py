from lxml import etree
import arrow
import yaml
from lxml.builder import ElementMaker
import os
import csv


class BaseProperty:
    def __init__(self, path):
        self.path = path
        self.root = self.__decode(path)
        self.root_as_str = etree.tostring(self.root)

    @staticmethod
    def __decode(path_to_file):
        with open(path_to_file, 'rb') as xml_file:
            return etree.parse(xml_file)


class Article(BaseProperty):
    def __init__(self, path, doi_location='metadata', doi_csv=None):
        super().__init__(path)
        self.doi_location = doi_location
        self.contributors = Contributors(path).contributors
        self.title = Title(path).titles[0]
        self.doi = DOI(path, doi_location, doi_csv).doi_data
        self.publication_date = PublicationDate(path).publication_date
        self.metadata = self.__get_relevant_metadata()

    def __get_relevant_metadata(self):
        return {
            "contributors": self.contributors,
            "title": self.title,
            "doi": self.doi,
            "date": self.publication_date
        }


class Contributors(BaseProperty):
    def __init__(self, path):
        super().__init__(path)
        self.contributors = self.__find_contributors()

    def __find_contributors(self):
        final = []
        contributors = self.root.xpath('/documents/document/authors/author')
        for contributor in contributors:
            current_contributor = {}
            for elem in contributor.iter():
                if elem.tag == "lname":
                    current_contributor['last'] = elem.text
                elif elem.tag == "institution":
                    current_contributor['institution'] = elem.text
                elif elem.tag == 'fname':
                    current_contributor['fname'] = elem.text
                elif elem.tag == 'mname':
                    current_contributor['mname'] = elem.text
                elif elem.tag == 'suffix':
                    current_contributor['suffix'] = elem.text
            final.append(current_contributor)
        return final


class Title(BaseProperty):
    def __init__(self, path):
        super().__init__(path)
        self.titles = self.__get_title()

    def __get_title(self):
        return [title.text for title in self.root.xpath('/documents/document/title')]


class DOI(BaseProperty):
    def __init__(self, path, doi_source='metadata', doi_csv=''):
        super().__init__(path)
        self.coverpage = self.__get_resource()
        self.doi_csv = doi_csv
        self.doi = self.__get_doi(doi_source)
        self.doi_data = self.__build_doi_object()

    def __get_doi(self, source):
        if source == 'metadata':
            matches = [doi.text for doi in self.root.xpath('/documents/document/fields/field[@name="doi"]/value')]
            if len(matches) > 0:
                return matches[0]
            else:
                return None
        else:
            return self.__find_if_doi_in_csv()

    def __find_if_doi_in_csv(self):
        with open(self.doi_csv, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['url'] == self.coverpage:
                    return row['doi']
        return None

    def __get_resource(self):
        return [url.text for url in self.root.xpath('/documents/document/coverpage-url')][0]

    def __build_doi_object(self):
        if self.doi:
            return {
                "doi": self.doi.replace("https://doi.org/", ""),
                "resource": self.coverpage,
                "timestamp": str(arrow.utcnow().format("YYYYMMDDHHmmss"))
            }
        else:
            return None


class PublicationDate(BaseProperty):
    def __init__(self, path):
        super().__init__(path)
        self.publication_date = [
            date.text for date in self.root.xpath('/documents/document/publication-date')
        ][0].split('-')[0]


class Pages(BaseProperty):
    def __init__(self, path):
        super().__init__(path)


class CitationList(BaseProperty):
    def __init__(self, path):
        super().__init__(path)


class DoiProceedingsBatchWriter:
    def __init__(self, output_file, yaml_config):
        self.output_file = output_file
        self.proceedings_metadata = yaml.safe_load(open(yaml_config, "r"))
        self.head = self.proceedings_metadata['head']
        self.path_to_proceedings = self.proceedings_metadata['path']
        self.cr = self.__build_namespace(
            "http://www.crossref.org/schema/5.3.1",
            None
        )
        self.xsi = self.__build_namespace(
            "http://www.w3.org/2001/XMLSchema-instance",
            "xsi"
        )
        self.valid_papers = self.__crawl_conference_papers()
        self.response = self.__build_response().strip()

    @staticmethod
    def __build_namespace(uri, short):
        return ElementMaker(
            namespace=uri,
            nsmap={
                short: uri,
            }
        )

    def __build_response(self):
        return etree.tostring(
            self.__build_xml(),
            pretty_print=True,
            xml_declaration=True,
            encoding='iso-8859-1'
        )

    def __build_xml(self):
        begin = self.cr.doi_batch(
            self.__build_head(),
            self.__build_body()
        )
        begin.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation'] = "http://www.crossref.org/schema/5.3.1 http://www.crossref.org/schemas/crossref5.3.1.xsd"
        begin.attrib['version'] = '5.3.1'
        return begin

    def __build_head(self):
        return self.cr.head(
            self.cr.doi_batch_id(
                self.head['doi_batch_id']
            ),
            self.cr.timestamp(
                self.head['timestamp']
            ),
            self.cr.depositor(
                self.cr.depositor_name(
                    self.head['depositor']['depositor_name']
                ),
                self.cr.email_address(
                    self.head['depositor']['email_address']
                )
            ),
            self.cr.registrant(
                self.head['registrant']
            )
        )

    def __build_body(self):
        return self.cr.body(
            self.cr.conference(
                self.__build_contributors(),
                self.__build_event_metadata(),
                self.__build_proceedings_metadata(),
                *self.__build_conference_papers()
            )
        )

    def __build_contributors(self):
        """Build a list of contributors and unpack them into an element with the unpack operator (*)."""
        i = 0
        final_contributors = []
        for person in self.proceedings_metadata['contributors']:
            sequence = 'first'
            department = ''
            suffix = ''
            if i != 0:
                sequence = "additional"
            if 'suffix' in person:
                suffix = person['suffix']
            if 'institution_department' in person['institution']:
                department = person['institution']['institution_department']
            final_contributors.append(
                self.cr.person_name(
                    self.cr.given_name(
                        person['given']
                    ),
                    self.cr.surname(
                        person['surname']
                    ),
                    self.cr.suffix(
                        suffix
                    ),
                    self.cr.affiliations(
                        self.cr.institution(
                            self.cr.institution_name(
                                person['institution']['institution_name']
                            ),
                            self.cr.institution_department(
                                department
                            )
                        ),
                    ),
                    sequence=sequence,
                    contributor_role=person['role']
                )
            )
        return self.cr.contributors(*final_contributors)

    def __build_event_metadata(self):
        return self.cr.event_metadata(
            self.cr.conference_name(
                self.proceedings_metadata['event_metadata']['conference_name']
            ),
            self.cr.conference_number(
                str(self.proceedings_metadata['event_metadata']['conference_number'])
            ),
            self.cr.conference_location(
                self.proceedings_metadata['event_metadata']['conference_location']
            ),
            self.cr.conference_date(
                start_month=str(self.proceedings_metadata['event_metadata']['conference_date']['start_month']),
                start_year=str(self.proceedings_metadata['event_metadata']['conference_date']['start_year']),
                start_day=str(self.proceedings_metadata['event_metadata']['conference_date']['start_day']),
                end_month=str(self.proceedings_metadata['event_metadata']['conference_date']['end_month']),
                end_year=str(self.proceedings_metadata['event_metadata']['conference_date']['end_year']),
                end_day=str(self.proceedings_metadata['event_metadata']['conference_date']['end_day']),
            )
        )

    def __build_proceedings_metadata(self):
        return self.cr.proceedings_series_metadata(
            self.cr.series_metadata(
                self.cr.titles(
                    self.cr.title(self.proceedings_metadata['proceedings_series_metadata']['series_metadata']['titles']['title'])),
                self.cr.issn(
                    str(self.proceedings_metadata['proceedings_series_metadata']['series_metadata']['issn'])
                )
            ),
            self.cr.proceedings_title(
                self.proceedings_metadata['proceedings_series_metadata']['proceedings_title']
            ),
            self.cr.publisher(
                self.cr.publisher_name(
                    self.proceedings_metadata['proceedings_series_metadata']['publisher']
                )
            ),
            self.cr.publication_date(
                self.cr.year(
                    str(self.proceedings_metadata['proceedings_series_metadata']['publication_date']['year'])
                )
            ),
            self.cr.noisbn(
                reason="simple_series"
            )
        )

    def __crawl_conference_papers(self):
        valid_proceedings = []
        for path, directories, files in os.walk(self.path_to_proceedings):
            for file in files:
                proceeding = Article(f"{path}/{file}")
                if proceeding.doi:
                    valid_proceedings.append(proceeding.metadata)
        return valid_proceedings

    def __build_conference_papers(self):
        final_papers = []
        for paper in self.valid_papers:
            final_papers.append(self.cr.conference_paper(
                self.cr.contributors(
                    *self.__build_paper_contributors(paper['contributors'])
                ),
                self.cr.titles(
                    self.cr.title(
                        paper['title']
                    )
                ),
                self.cr.publication_date(
                    self.cr.year(
                        paper['date']
                    )
                ),
                self.cr.doi_data(
                    self.cr.doi(
                        paper['doi']['doi']
                    ),
                    self.cr.resource(
                        paper['doi']['resource']
                    )
                ),
                publication_type='full_text'
            ))
        return final_papers

    def __build_paper_contributors(self, contributors):
        final_contributors = []
        i = 0
        sequence = 'first'
        for contributor in contributors:
            given = contributor['fname']
            if 'mname' in contributor:
                given = f"{contributor['fname']} {contributor['mname']}"
            if i != 0:
                sequence = 'additional'
            final_contributors.append(self.cr.person_name(
                self.cr.given_name(
                    given
                ),
                self.cr.surname(
                    contributor['last']
                ),
                self.cr.suffix(
                    self.__get_suffix_if_exists(contributor)
                ),
                *self.__get_institution_name(contributor),
                sequence=sequence,
                contributor_role='author'
            ))
            i += 1
        return final_contributors

    @staticmethod
    def __get_suffix_if_exists(contributor):
        if 'suffix' in contributor:
            return contributor['suffix']
        else:
            return ""

    def __get_institution_name(self, contributor):
        affiliations = []
        if 'institution' in contributor:
            affiliations.append(
                self.cr.affiliations(
                    self.cr.institution(
                        self.cr.institution_name(
                            contributor['institution']
                        )
                    )
                )
            )
        else:
            affiliations.append(self.cr.affiliations())
        return affiliations


class DoiJournalBatchWriter:
    def __init__(self, yaml_config, csv_path=""):
        self.proceedings_metadata = yaml.safe_load(open(yaml_config, "r"))
        self.csv_path = csv_path
        self.doi_location = self.__find_doi_location()
        self.head = self.proceedings_metadata['head']
        self.path_to_articles = self.proceedings_metadata['path']
        self.cr = self.__build_namespace(
            "http://www.crossref.org/schema/5.3.1",
            None
        )
        self.xsi = self.__build_namespace(
            "http://www.w3.org/2001/XMLSchema-instance",
            "xsi"
        )
        self.valid_papers = self.__crawl_journal_articles()
        self.response = self.__build_response().strip()

    def __find_doi_location(self):
        if self.csv_path != "":
            return "csv"
        else:
            return "metadata"

    @staticmethod
    def __build_namespace(uri, short):
        return ElementMaker(
            namespace=uri,
            nsmap={
                short: uri,
            }
        )

    def __build_response(self):
        return etree.tostring(
            self.__build_xml(),
            pretty_print=True,
            xml_declaration=True,
            encoding='iso-8859-1'
        )

    def __build_xml(self):
        begin = self.cr.doi_batch(
            self.__build_head(),
            self.__build_body()
        )
        begin.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation'] = "http://www.crossref.org/schema/5.3.1 http://www.crossref.org/schemas/crossref5.3.1.xsd"
        begin.attrib['version'] = '5.3.1'
        return begin

    def __build_head(self):
        return self.cr.head(
            self.cr.doi_batch_id(
                self.head['doi_batch_id']
            ),
            self.cr.timestamp(
                self.head['timestamp']
            ),
            self.cr.depositor(
                self.cr.depositor_name(
                    self.head['depositor']['depositor_name']
                ),
                self.cr.email_address(
                    self.head['depositor']['email_address']
                )
            ),
            self.cr.registrant(
                self.head['registrant']
            )
        )

    def __build_body(self):
        return self.cr.body(
            self.cr.journal(
                self.__build_journal_metadata(),
                self.__build_journal_issue(),
                *self.__build_journal_articles()
            )
        )

    def __build_journal_metadata(self):
        return self.cr.journal_metadata(
            *self.__get_full_titles(),
            *self.__get_abrev_titles(),
            *self.__get_issns(),
            self.__get_doi()
        )

    def __get_full_titles(self):
        full_titles = []
        for title in self.proceedings_metadata['journal_metadata']['full_title']:
            full_titles.append(self.cr.full_title(title))
        return full_titles

    def __get_issns(self):
        issn_data = []
        for issn in self.proceedings_metadata['journal_metadata']['issn_data']:
            issn_data.append(
                self.cr.issn(
                    issn['issn'],
                    media_type=issn['type']
                )
            )
        return issn_data

    def __get_doi(self):
        return self.cr.doi_data(
            self.cr.doi(
                self.proceedings_metadata['journal_metadata']['doi_data']['doi']
            ),
            self.cr.resource(
                self.proceedings_metadata['journal_metadata']['doi_data']['resource']
            )
        )

    def __get_abrev_titles(self):
        abbrev_titles = []
        for title in self.proceedings_metadata['journal_metadata']['abbrev_title']:
            abbrev_titles.append(
                self.cr.abbrev_title(
                    title
                )
            )
        return abbrev_titles

    def __build_journal_issue(self):
        return self.cr.journal_issue(
            self.__build_contributors(),
            self.cr.titles(
                self.cr.title(
                    self.proceedings_metadata['journal_issue']['titles']['title']
                )
            ),
            self.cr.publication_date(
                self.cr.year(
                    self.proceedings_metadata['journal_issue']['publication_date']['year']
                )
            ),
            self.cr.journal_volume(
                self.cr.volume(
                    self.proceedings_metadata['journal_issue']['journal_volume']['volume']
                )
            )
        )

    def __build_contributors(self):
        """Build a list of contributors and unpack them into an element with the unpack operator (*)."""
        i = 0
        final_contributors = []
        if 'contributors' in self.proceedings_metadata:
            for person in self.proceedings_metadata['contributors']:
                sequence = 'first'
                department = ''
                suffix = ''
                if i != 0:
                    sequence = "additional"
                if 'suffix' in person:
                    suffix = person['suffix']
                if 'institution_department' in person['institution']:
                    department = person['institution']['institution_department']
                final_contributors.append(
                    self.cr.person_name(
                        self.cr.given_name(
                            person['given']
                        ),
                        self.cr.surname(
                            person['surname']
                        ),
                        self.cr.suffix(
                            suffix
                        ),
                        self.cr.affiliations(
                            self.cr.institution(
                                self.cr.institution_name(
                                    person['institution']['institution_name']
                                ),
                                self.cr.institution_department(
                                    department
                                )
                            ),
                        ),
                        sequence=sequence,
                        contributor_role=person['role']
                    )
                )
            return self.cr.contributors(*final_contributors)
        else:
            return self.cr.contributors()

    def __build_journal_articles(self):
        final_papers = []
        for paper in self.valid_papers:
            final_papers.append(self.cr.journal_article(
                self.cr.titles(
                    self.cr.title(
                        paper['title']
                    )
                ),
                self.cr.contributors(
                    *self.__build_paper_contributors(paper['contributors'])
                ),
                self.cr.publication_date(
                    self.cr.year(
                        paper['date']
                    )
                ),
                self.cr.doi_data(
                    self.cr.doi(
                        paper['doi']['doi']
                    ),
                    self.cr.resource(
                        paper['doi']['resource']
                    )
                ),
                publication_type='full_text'
            ))
        return final_papers

    def __build_paper_contributors(self, contributors):
        final_contributors = []
        i = 0
        sequence = 'first'
        for contributor in contributors:
            given = contributor['fname']
            if 'mname' in contributor:
                given = f"{contributor['fname']} {contributor['mname']}"
            if i != 0:
                sequence = 'additional'
            final_contributors.append(self.cr.person_name(
                self.cr.given_name(
                    given
                ),
                self.cr.surname(
                    contributor['last']
                ),
                self.cr.suffix(
                    self.__get_suffix_if_exists(contributor)
                ),
                *self.__get_institution_name(contributor),
                sequence=sequence,
                contributor_role='author'
            ))
            i += 1
        return final_contributors

    def __crawl_journal_articles(self):
        """Crawl a directory of Journal Articles and find a list files with DOIs. Ignore any journal content where no
        DOI is present."""
        valid_articles = []
        for path, directories, files in os.walk(self.path_to_articles):
            for file in files:
                article = Article(f"{path}/{file}", self.doi_location, self.csv_path)
                if article.doi:
                    valid_articles.append(article.metadata)
        return valid_articles

    @staticmethod
    def __get_suffix_if_exists(contributor):
        if 'suffix' in contributor:
            return contributor['suffix']
        else:
            return ""

    def __get_institution_name(self, contributor):
        affiliations = []
        if 'institution' in contributor:
            affiliations.append(
                self.cr.affiliations(
                    self.cr.institution(
                        self.cr.institution_name(
                            contributor['institution']
                        )
                    )
                )
            )
        else:
            affiliations.append(self.cr.affiliations())
        return affiliations


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Crawl Papers and Generate Output XML.')
    parser.add_argument("-o", "--output", dest="output", help="Specify output XML file.", default='output.xml')
    parser.add_argument(
        "-y",
        "--yaml_config",
        dest="yaml_config",
        help="Specify path to your yaml configuration",
        required=True
    )
    parser.add_argument(
        "-t",
        "--registration_type",
        dest="r_type",
        help="Specify type of registration",
        default='journal_articles',
        choices=['journal_articles', 'proceedings']
    )
    parser.add_argument(
        "-d",
        "--doi_source",
        dest="doi_source",
        help="Specify the source of dois.",
        default='metadata',
        choices=['metadata', 'csv']
    )
    parser.add_argument(
        "-c",
        "--csv_path",
        dest="csv_path",
        help="If a CSV is your source, what is the path to the csv?",
    )
    args = parser.parse_args()
    if args.r_type == 'journal_articles':
        if args.doi_source == 'metadata':
            x = DoiJournalBatchWriter(args.yaml_config).response
        else:
            x = DoiJournalBatchWriter(args.yaml_config, csv_path=args.csv_path).response
        with open(args.output, 'wb') as example:
            example.write(x)
    elif args.r_type == 'proceedings':
        x = DoiProceedingsBatchWriter(args.output, args.yaml_config).response
        with open(args.output, 'wb') as example:
            example.write(x)
