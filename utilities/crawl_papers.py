from lxml import etree
import arrow


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


if __name__ == "__main__":
    x = Proceeding('output/output/23.xml')
    print(x.publication_date)
