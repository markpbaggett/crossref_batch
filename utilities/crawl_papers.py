from lxml import etree
import arrow
import yaml
from lxml.builder import ElementMaker
import os


class BaseProperty:
    def __init__(self, path):
        self.path = path
        self.root = self.__decode(path)
        self.root_as_str = etree.tostring(self.root)

    @staticmethod
    def __decode(path_to_file):
        with open(path_to_file, 'rb') as xml_file:
            return etree.parse(xml_file)


class Proceeding(BaseProperty):
    def __init__(self, path):
        super().__init__(path)
        self.contributors = Contributors(path).contributors
        self.title = Title(path).titles[0]
        self.doi = DOI(path).doi_data
        self.publication_date = PublicationDate(path).publication_date
        self.full_proceeding = self.__get_full_proceeding()

    def __get_full_proceeding(self):
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
    def __init__(self, path):
        super().__init__(path)
        self.doi = self.__get_doi()
        self.coverpage = self.__get_resource()
        self.doi_data = self.__build_doi_object()

    def __get_doi(self):
        matches = [doi.text for doi in self.root.xpath('/documents/document/fields/field[@name="doi"]/value')]
        if len(matches) > 0:
            return matches[0]
        else:
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
                proceeding = Proceeding(f"{path}/{file}")
                if proceeding.doi:
                    valid_proceedings.append(proceeding.full_proceeding)
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
        #self.valid_papers = self.__crawl_conference_papers()
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
            self.cr.journal(
                self.__build_journal_metadata(),
                # self.__build_journal_issue(),
                # self.__build_journal_articles()
            )
        )

    def __build_journal_metadata(self):
        return self.cr.journal_metadata(
            *self.__get_full_titles(),
            *self.__get_abrev_titles(),
            *self.__get_issns()
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
        return

    def __build_journal_articles(self):
        return


if __name__ == "__main__":
    # path_to_proceedings_metadata = "data/quail.yml"
    # x = DoiProceedingsBatchWriter('test.xml', path_to_proceedings_metadata).response
    # with open('example.xml', 'wb') as example:
    #     example.write(x)

    path_to_proceedings_metadata = "data/quail_journal.yml"
    x = DoiJournalBatchWriter('test.xml', path_to_proceedings_metadata).response
    with open('example_journal.xml', 'wb') as example:
        example.write(x)
