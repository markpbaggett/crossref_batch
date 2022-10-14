from lxml import etree


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
        self.dois = DOI(path).dois


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
        self.dois = self.__get_doi()

    def __get_doi(self):
        return [doi.text for doi in self.root.xpath('/documents/document/fields/field[@name="doi"]/value')]


if __name__ == "__main__":
    x = Proceeding('output/output/23.xml')
    print(x.dois)