from lxml import etree


class BaseProperty:
    def __init__(self, path):
        self.path = path
        self.root = etree.parse(path)
        self.root_as_str = etree.tostring(self.root)


class Contributors(BaseProperty):
    def __init__(self, path):
        super().__init__(path)
        self.contributors = self.__find_contributors()

    def __find_authors(self):
        self.various_titles['plain'] = [thing.text for thing in self.root.xpath(
            'mods:titleInfo[not(@supplied)]/mods:title',
            namespaces=self.namespaces
        )]
        return

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



if __name__ == "__main__":
    x = Contributors('output/output/23.xml')
    print(x.contributors)