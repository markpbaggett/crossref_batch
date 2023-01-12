================
Journal Articles
================

Crossref allows you to perform batch registration for journals and the volumes, issues, and articles being registered
within the journal.  Within a journal instance you may register articles from a single issue by adding details to
:code:`journal_issue`. Crossref allows you to register items from more than one issue but to do so you must use
multiple journal instances within the XML file you submit to Crossref.

The documentation below describes what Crossref expects and our approach to batch registration of DOIs for journal
articles.

------------------------------------
Anatomy of Crossref Journal Metadata
------------------------------------

Crossref provides excellent documentation about the anatomy of a batch registration in its
`schema documentation <https://data.crossref.org/reports/help/schema_doc/5.3.1/index.html>`_.

This section describes details regarding what Crossref expects for journals so that it is easy to understand why we
create the various components in our generated XML described in later sections. Please note that the details here may
only include details about the sections we currently use. See schema documentation for more details about unused tags.

Full Description as XML
=======================

Below is a description of the anatomy of a Journal object down to its ground children tags. Please note that the
:code:`cardinality` attributes in children tags are not a part of the Crossref schema but instead included to make it
easier to understand the cardinality expectations of each tag. Please see the `schema documentation <https://data.crossref.org/reports/help/schema_doc/5.3.1/index.html>`_
for details on the anatomy of grand children tags and nodes.

.. code-block:: xml

    <journal xmlns="http://www.crossref.org/schema/5.3.1">
      <journal_metadata language="" reference_distribution_opts="none" cardinality="{1, 1}">
          <full_title>{1,10}</full_title>
          <abbrev_title>{0,10}</abbrev_title>
          <issn media_type="print">{0,6}</issn>
          <coden>{0,1}</coden>
          <archive_locations>{0,1}</archive_locations>
          <doi_data>{0,1}</doi_data>
      </journal_metadata>
      <journal_issue cardinality="{0, 1}">
          <contributors>{0,1}</contributors>
          <titles>{0,1}</titles>
          <publication_date media_type="print">{1,10}</publication_date>
          <journal_volume>{0,1}</journal_volume>
          <issue>{0,1}</issue>
          <special_numbering>{0,1}</special_numbering>
          <archive_locations>{0,1}</archive_locations>
          <doi_data>{0,1}</doi_data>
      </journal_issue>
      <journal_article language="" publication_type="full_text" reference_distribution_opts="none" cardinality="{0,unbounded}">
          <titles>{1,20}</titles>
          <contributors>{0,1}</contributors>
          <jats:abstract abstract-type="" xml:base="" id="" xml:lang="" specific-use="">{0,unbounded}</jats:abstract>
          <publication_date media_type="print">{1,10}</publication_date>
          <acceptance_date media_type="print">{0,1}</acceptance_date>
          <pages>{0,1}</pages>
          <publisher_item>{0,1}</publisher_item>
          <crossmark>{0,1}</crossmark>
          <fr:program name="fundref">{0,1}</fr:program>
          <ai:program name="AccessIndicators">{0,1}</ai:program>
          <ct:program>{0,1}</ct:program>
          <rel:program name="relations">{0,1}</rel:program>
          <archive_locations>{0,1}</archive_locations>
          <scn_policies>{0,1}</scn_policies>
          <doi_data>{1,1}</doi_data>
          <citation_list>{0,1}</citation_list>
          <component_list>{0,1}</component_list>
      </journal_article>
    </journal>

Journal Metadata
================

A :code:`journal_metadata` tag is required for each :code:`journal` in a batch registration request. The
:code:`journal_metadata` element allows one attribute, :code:`@language`.  :code:`@language` is an optional attribute
but must be one of the language codes listed in the schema in `ISO 639 <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_
format. The docs don't mention this, but it looks like the schema technically expects ISO 639-1.

While most sub-elements are optional, a :code:`journal_metadata` tag must always have 1-10 :code:`full_title` tags.
The contents of this tag should be a full title by which a journal is commonly known or cited.

A :code:`journal_metadata` tag may also have 0-10 :code:`abbrev_title` tags.  These should contain common abbreviation
or abbreviations used when citing a journal. It is recommended that periods be included after abbreviated words within
the title.

A :code:`journal_metadata` tag may also have 0-6 :code:`issn` tags that describe the ISSN(s) assigned to the title being
registered. The :code:`@media_type` attribute is optional and used to describe whether the ISSN is for the electronic or
print. If not included, Crossref will assume the ISSN refers to the print.

The :code:`doi_data` section includes information related to the DOI that refers to the full journal. The :code:`doi` tag
includes the DOI for the entity being registered with Crossref, while :code:`resource` includes the URI associated with
a DOI.

A completed :code:`journal_metadata` section may have other components but may look like this:

.. code-block:: xml

    <journal_metadata>
        <full_title>National Quail Symposium Proceedings</full_title>
        <full_title>Quail</full_title>
        <full_title>National Quail Symposium proceedings</full_title>
        <full_title>Proceedings of the ... National Quail Symposium</full_title>
        <full_title>Proceedings of the National Quail Symposia</full_title>
        <full_title>Gamebird : a joint conference of Quail and Perdix</full_title>
        <full_title>NQSP</full_title>
        <abbrev_title>NQSP</abbrev_title>
        <issn media_type="print">2573-5667</issn>
        <issn media_type="electronic">2573-5683</issn>
        <doi_data>
          <doi>10.7290/nqsp</doi>
          <resource>https://trace.tennessee.edu/nqsp/</resource>
        </doi_data>
    </journal_metadata>

Journal Issue
=============

A :code:`journal_issue` tag is required for each :code:`journal` in a batch registration request.

While there are many allowed sub-elements, a :code:`journal_issue` must always have 1-10 :code:`publication_date` tags
that describe the date of publication. Multiple dates are allowed to allow for different dates of publication for online
and print versions. If you have separate dates, you must use a :code:`@media-type` attribute to describe whether the date
refers to the print or electronic. Each :code:`publication_date` must have exactly one :code:`year` but can also have
0-1 :code:`month` or :code:`day` tags.  Only use the optional tags if you know the exact date.

At UTK, we also try to describe known editors and reviewers in the :code:`contributors` section. Each contributor must
have one of the following roles: author, editor, chair, reviewer, review-assistant, stats-reviewer, reviewer-external,
reader, translator.  We do not put authors in this section but instead in the articles section. Each contributor can have
various metadata elements.  See schema docs for more information.

Each :code:`journal_issue` can have 0-1 :code:`titles` tag which acts as a container for the title and original language
title elements. Only :code:`title` is required here unless it is a translation in which :code:`original_language_title`
also becomes required.

Finally, a :code:`journal_issue` can have 0-1 :code:`journal_volume` tags which acts as a ontainer for the journal
volume and DOI assigned to an entire journal volume. You may register a DOI for an entire volume by including doi_data
in journal_volume. If included, this element must have 0, 1 :code:`volume` tags which include the volume number.

A completed :code:`journal_issue` section may have other components but may look like this:

.. code-block:: xml

    <journal_issue>
        <contributors>
          <person_name sequence="first" contributor_role="editor">
            <given_name>Frank R.</given_name>
            <surname>Thompson</surname>
            <suffix>III</suffix>
            <affiliations>
              <institution>
                <institution_name>USDA Forest Service</institution_name>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="first" contributor_role="editor">
            <given_name>Roger D.</given_name>
            <surname>Applegate</surname>
            <affiliations>
              <institution>
                <institution_name>Tennessee Wildlife Resources Agency</institution_name>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="first" contributor_role="editor">
            <given_name>Leonard A.</given_name>
            <surname>Brennan</surname>
            <affiliations>
              <institution>
                <institution_name>Texas A&amp;M University-Kingsville</institution_name>
                <institution_department>Caesar Kleberg Wildlife Research Institute</institution_department>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="first" contributor_role="editor">
            <given_name>C. Brad</given_name>
            <surname>Dabbert</surname>
            <affiliations>
              <institution>
                <institution_name>Texas Tech University</institution_name>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="first" contributor_role="editor">
            <given_name>Stephen J.</given_name>
            <surname>DeMaso</surname>
            <affiliations>
              <institution>
                <institution_name>U.S. Fish and Wildlife Service</institution_name>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="first" contributor_role="editor">
            <given_name>Kenneth</given_name>
            <surname>Duren</surname>
            <affiliations>
              <institution>
                <institution_name>Pennsylvania Game Commission</institution_name>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="first" contributor_role="editor">
            <given_name>James A.</given_name>
            <surname>Martin</surname>
            <affiliations>
              <institution>
                <institution_name>University of Georgia</institution_name>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="first" contributor_role="editor">
            <given_name>Kelly S.</given_name>
            <surname>Reyna</surname>
            <affiliations>
              <institution>
                <institution_name>Texas A&amp;M University-Commerce</institution_name>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="first" contributor_role="editor">
            <given_name>Evan P.</given_name>
            <surname>Tanner</surname>
            <affiliations>
              <institution>
                <institution_name>Texas A&amp;M University-Kingsville</institution_name>
                <institution_department>Caesar Kleberg Wildlife Research Institute</institution_department>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="first" contributor_role="editor">
            <given_name>Theron M.</given_name>
            <surname>Terhune II</surname>
            <affiliations>
              <institution>
                <institution_name>Orton Plantation</institution_name>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="first" contributor_role="editor">
            <given_name>Molly K.</given_name>
            <surname>Foley</surname>
            <affiliations>
              <institution>
                <institution_name>National Bobwhite &amp; Grassland Initiative</institution_name>
              </institution>
            </affiliations>
          </person_name>
        </contributors>
        <titles>
          <title>Quail 9: National Quail Symposium</title>
        </titles>
        <publication_date>
          <year>2022</year>
        </publication_date>
        <journal_volume>
          <volume>9</volume>
        </journal_volume>
    </journal_issue>

Journal Article
===============

The :code:`journal` tag can have 0 - "unbounded" :code:`journal_article` tags that acts as a container for all
information about a single journal article. Each :code:`journal_article` must have 1-20 :code:`titles`, 1-10
:code:`publication_date`, and 1-1 :code:`doi_data` tags.

The rules for each of these are the same as described in previous elements above, and we use them in the same way here.

In addition to the required elements, we also add authors using the :code:`contributors` tag. Each :code:`person_name`
in this section is assigned the author role.

A completed journal article should look something like this:

.. code-block:: xml

    <journal_article publication_type="full_text">
        <titles>
          <title>Northern Bobwhite and Fire: A Review and Synthesis</title>
        </titles>
        <contributors>
          <person_name sequence="first" contributor_role="author">
            <given_name>David A</given_name>
            <surname>Weber</surname>
            <affiliations>
              <institution>
                <institution_name>University of Georgia</institution_name>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="additional" contributor_role="author">
            <given_name>Evan P</given_name>
            <surname>Tanner</surname>
            <affiliations>
              <institution>
                <institution_name>Caesar Kleberg Wildlife Research Institute</institution_name>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="additional" contributor_role="author">
            <given_name>Theron M.</given_name>
            <surname>Terhune</surname>
            <suffix>II</suffix>
            <affiliations>
              <institution>
                <institution_name>Tall Timbers</institution_name>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="additional" contributor_role="author">
            <given_name>J. Morgan</given_name>
            <surname>Varner</surname>
            <affiliations>
              <institution>
                <institution_name>Tall Timbers</institution_name>
              </institution>
            </affiliations>
          </person_name>
          <person_name sequence="additional" contributor_role="author">
            <given_name>James A.</given_name>
            <surname>Martin</surname>
            <affiliations>
              <institution>
                <institution_name>University of Georgia</institution_name>
              </institution>
            </affiliations>
          </person_name>
        </contributors>
        <publication_date>
          <year>2022</year>
        </publication_date>
        <doi_data>
          <doi>10.7290/nqsp09V0ju</doi>
          <resource>https://trace.tennessee.edu/nqsp/vol9/iss1/63</resource>
        </doi_data>
    </journal_article>

---------------------------
Using CSV as the DOI Source
---------------------------

By default, it is assumed that the DOIs we intend to mint are included in the metadata record for each work. Optionally,
a CSV can be supplied as the source (see below for more details).

If you are supplying a CSV, the CSV must have 2 columns:  :code:`url` and :code:`doi`.  These columns can appear anywhere,
and there can be :code:`n` number of additional columns. The only requirement is that :code:`url` and :code:`doi` appear
in row one and the headings be lowercase.

The value of the :code:`url` column fields should be the url to the work in Digital Commons (e.g. :code:`https://trace.tennessee.edu/nqsp/vol8/iss1/24`).

The value of the :code:`doi` column fields can be a DOI that starts with :code:`https://doi.org/` or :code:`10.7290`.
Crossref expects the value to be formatted as :code:`10.7290/xxxxxx` so code exists in the scripts to remove
:code:`https://doi.org/` if it is included:

.. code-block:: python
    :emphasize-lines: 4

    def __build_doi_object(self):
        if self.doi:
            return {
                "doi": self.doi.replace("https://doi.org/", ""),
                "resource": self.coverpage,
                "timestamp": str(arrow.utcnow().format("YYYYMMDDHHmmss"))
            }
        else:
            return None

-------------------------------------------------------
Creating Metadata about the Journal, Issue, and Deposit
-------------------------------------------------------

Additional metadata beyond what is found in the article level metadata is needed for deposit and DOI registration.

This metadata is added in a human-readable way using yaml. These yaml files should include everything needed to generate
the missing elements for deposit.

The :code:`path` property describes where the XML containing article level metadata can be found.

.. code-block:: yaml

    path: "metadata/output/vol9"

The :code:`contributors` property describes the editors and reviewers of the volume or issue:

.. code-block:: yaml

    contributors:
      - given: Frank R.
        surname: Thompson
        suffix: III
        role: editor
        sequence: first
        institution:
          institution_name: USDA Forest Service
      - given: Roger D.
        surname: Applegate
        role: editor
        sequence: additional
        institution:
          institution_name: Tennessee Wildlife Resources Agency
      - given: Leonard A.
        surname: Brennan
        role: editor
        sequence: additional
        institution:
          institution_name: Texas A&M University-Kingsville
          institution_department: Caesar Kleberg Wildlife Research Institute
      - given: C. Brad
        surname: Dabbert
        role: editor
        sequence: additional
        institution:
          institution_name: Texas Tech University
      - given: Stephen J.
        surname: DeMaso
        role: editor
        sequence: additional
        institution:
          institution_name: U.S. Fish and Wildlife Service
      - given: Kenneth
        surname: Duren
        role: editor
        sequence: additional
        institution:
          institution_name: Pennsylvania Game Commission
      - given: James A.
        surname: Martin
        role: editor
        sequence: additional
        institution:
          institution_name: University of Georgia
      - given: Kelly S.
        surname: Reyna
        role: editor
        sequence: additional
        institution:
          institution_name: Texas A&M University-Commerce
      - given: Evan P.
        surname: Tanner
        role: editor
        sequence: additional
        institution:
          institution_name: Texas A&M University-Kingsville
          institution_department: Caesar Kleberg Wildlife Research Institute
      - given: Theron M.
        surname: Terhune II
        role: editor
        sequence: additional
        institution:
          institution_name: Orton Plantation
      - given: Molly K.
        surname: Foley
        role: editor
        sequence: additional
        institution:
          institution_name: National Bobwhite & Grassland Initiative

The :code:`journal_metadata` property includes metadata about the journal overall.

.. code-block:: yaml

    journal_metadata:
      full_title:
        - National Quail Symposium Proceedings
        - Quail
        - National Quail Symposium proceedings
        - Proceedings of the ... National Quail Symposium
        - Proceedings of the National Quail Symposia
        - "Gamebird : a joint conference of Quail and Perdix"
        - NQSP
      abbrev_title:
        - NQSP
      issn_data:
        - issn: 2573-5667
          type: print
        - issn: 2573-5683
          type: electronic
      doi_data:
        doi: "10.7290/nqsp"
        resource: "https://trace.tennessee.edu/nqsp/"

The :code:`journal_issue` property includes other metadata about the issue.

.. code-block:: yaml

    journal_issue:
      publication_date:
        year: "2022"
      journal_volume:
        volume: "9"
      titles:
        title: "Quail 9: National Quail Symposium"

Finally, the :code:`head` property includes metadata required for deposit.

.. code-block:: yaml

    head:
      doi_batch_id: utk_nqsp_9_10_2022
      timestamp: "20221021080808"
      depositor:
        depositor_name: Mark Baggett
        email_address: mbagget1@utk.edu
      registrant: University of Tennessee

------------------------------------------------------------------------
DOIJournalBatchWriter and Other Classes Used for Registration Generation
------------------------------------------------------------------------

Crossref batch registration of DOIs for journals and journal articles is handled primarily by the :code:`crawl_papers.py`
script in this repository.  While there are a few classes here, :code:`DOIJournalBatchWriter` is primarily used.

:code:`DOIJournalBatchWriter` also includes an optional argument, :code:`csv_path`. By default, this is an empty string.
If the string is not empty, it signifies to the :code:`DOIJournalBatchWriter` instance that the relevant DOIs in this
registration is found in an attached CSV rather than the metadata record for individual works.

On initialization, :code:`DOIJournalBatchWriter` requires one argument: :code:`yaml_config` or the yaml file that
contains additional metadata beyond what is found in the article level metadata that is needed for deposit and DOI
registration. The :code:`yaml_config` is read by the class, converted to a dictionary, and stored as an attribute. If
:code:`csv_path` is included, it is stored in an attribute as well.

Also during initialization, initial namespaces are declared for later use.  This is important to know in case there
are future efforts to make use of other namespaces listed in the Crossref documentation and examples above as they are
not declared currently and will need to be before they can be used. A special attribute called :code:`doi_location` is
also defined. This attribute determines whether the source of the DOIs should be the metadata record or a CSV.

.. code-block:: python

    def __find_doi_location(self):
        if self.csv_path != "":
            return "csv"
        else:
            return "metadata"

Next, the path to the metadata files that is declared in the :code:`yaml_config` is crawled. Each metadata file found
in the path is passed to the :code:`Article` class which builds relevant metadata and determines whether the article
should have a DOI registered. This method sends the path to the current file, where to look for the DOI, a path to the
CSV to use for lookup if the source is CSV.

.. code-block:: python

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

The :code:`Article` class decodes the binary XML file and converts it to an :code:`ElementTree`. It then passes relevant
metadata to other defined classes to build the title, date, doi, and contributor information that is expected in the
registration. Note that if future imports expect more information in the article that additional classes will need to be
added and added to :code:`Article` appropriately.

.. code-block:: python

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

The :code:`DOI` class includes the code for find the relevant DOI based on the DOI location information passed to it
during initialiization. If the source is the metadata file, it looks at :code:`/documents/document/fields/field[@name="doi"]/value`.
If the source is a CSV, it crawls the CSV for each row in the CSV looking for a match.

.. code-block:: python
    :emphasize-lines: 19-25

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

Finally, the output XML file is generated. Each section of the outgoing XML is defined in a private method in
:code:`DOIBatchJournalWriter` like in the examples below:

.. code-block:: python

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

    def __build_journal_metadata(self):
        return self.cr.journal_metadata(
            *self.__get_full_titles(),
            *self.__get_abrev_titles(),
            *self.__get_issns(),
            self.__get_doi()
        )

Ultimately, this data is passed up appropriately to methods representing parent nodes and ultimately converted
to one XML file.

.. code-block:: python

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

In order to pass information accordingly, file and path names are added for each registration at the bottom of the file
as so:

.. code-block:: python

    if __name__ == "__main__":
        path_to_proceedings_metadata = "data/quail_journal.yml"
        x = DoiJournalBatchWriter('test.xml', path_to_proceedings_metadata).response
        with open('example_journal.xml', 'wb') as example:
            example.write(x)


---------------
Crawling Papers
---------------

Crawling papers and generating an XML upload can be done with
`the script found here <https://github.com/markpbaggett/crossref_batch/blob/main/utilities/crawl_papers.py>`_.
The script iterates over all XML files in a directory and creates an XML file according to the
`Crossref 5.3.1 XML schema definition <https://data.crossref.org/schemas/common5.3.1.xsd>`_. The script needs a yml file
with the parts described above including a path to the metadata files.

To generate an initial XML registration where DOIs are located in the metadata record, you can run the script like this:

.. code-block:: shell

    python utilities/crawl_papers.py -y data/quail_journal -o quail_8.xml

To generate an initial XML registration where DOIs are found in an attached CSV, you can run the script like this:

.. code-block:: shell

    python utilities/crawl_papers.py -y data/quail_journal.yml -d csv -c nqsp_8.csv -o nqsp8.xml

This will generate a registration file that includes metadata from the supplied yaml and any articles in the path that
have a DOI. Once the XML file is generated, it may need to be cleaned. The following section describes this process.

----------------------
Finalizing XML Deposit
----------------------

Finally, run `lxml_transform.py <https://github.com/markpbaggett/crossref_batch/blob/main/utilities/lxml_transform.py>`_
to remove blank elements and perform other required steps for finalizing the XML output.

.. code-block:: shell

    python utilities/lxml_transform.py -i quail_8.xml -o quail_8_clean.xml


Then, take that XML file and upload it to Crossref for testing.

First, check that your `XML is wellformed and valid <https://apps.crossref.org/XSDParse/>`_ by uploading here.

Next, upload your XML file to `the test system <https://test.crossref.org>`_ for processing and to insure there are no
major issues.

Finally, if all is good, upload to `the production system <https://doi.crossref.org>`_. After deposit, you will receive
an email stating whether your upload was successful.
