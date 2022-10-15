from lxml import etree
import arrow
import yaml
from lxml.builder import ElementMaker


class BaseProperty:
    def __init__(self, path):
        self.path = path
        self.root = etree.parse(path)
        self.root_as_str = etree.tostring(self.root)


class Proceeding(BaseProperty):
    def __init__(self, path):
        super().__init__(path)
        self.contributors = Contributors(path).contributors
        self.title = Title(path).titles[0]
        self.doi = DOI(path).doi_data
        self.publication_date = PublicationDate(path).publication_date


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
        return [doi.text for doi in self.root.xpath('/documents/document/fields/field[@name="doi"]/value')][0]

    def __get_resource(self):
        return [url.text for url in self.root.xpath('/documents/document/coverpage-url')][0]

    def __build_doi_object(self):
        return {
            "doi": self.doi.replace("https://doi.org/", ""),
            "resource": self.coverpage,
            "timestamp": str(arrow.utcnow().format("YYYYMMDDHHmmss"))
        }


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


class DoiBatchWriter:
    def __init__(self, output_file, yaml_config):
        self.output_file = output_file
        self.proceedings_metadata = yaml.safe_load(open(yaml_config, "r"))
        self.head = self.proceedings_metadata['head']
        self.cr = self.__build_namespace(
            "http://www.crossref.org/schema/4.4.2",
            'cr'
        )
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
            pretty_print=True
        )

    def __build_xml(self):
        return self.cr.doi_batch(
            self.__build_head(),
            self.__build_body(),
            version='4.4.2'
        )

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
                self.cr.depositor_email(
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
                self.__build_event_metadata()
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
                    self.cr.institution(
                        self.cr.institution(
                            self.cr.institution_name(
                                person['institution']['institution_name']
                            ),
                            self.cr.institution_department(
                                department
                            )
                        )
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


if __name__ == "__main__":
    path_to_proceedings_metadata = "data/quail.yml"
    x = DoiBatchWriter('test.xml', path_to_proceedings_metadata).response
    with open('example.xml', 'wb') as example:
        example.write(x)
