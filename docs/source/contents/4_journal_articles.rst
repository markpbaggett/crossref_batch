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

This section describes details regardingv what Crossref expects for journals so that it is easy to understand why we
create the various components in our generated XML described in later sections. Please note that the details here may
only include details about the sections we currently use. See schema documentation for more details about unused tags.

Full Description as XML
=======================

Below is a description of the anatomy of a Journal object down to its ground children tags. Please note that the
:code:`cardinality` attributes in children tags are not a part of the Crossref schem but instead included to make it
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

---------------------------------------------
Creating Metadata about the Journal and Issue
---------------------------------------------


--------------------
Journal Batch Writer
--------------------


---------------
Crawling Papers
---------------

Crawling papers and generating an XML upload can be done with
`the script found here <https://github.com/markpbaggett/crossref_batch/blob/main/utilities/crawl_papers.py>`_.
The script iterates over all XML files in a directory and creates an XML file according to the
`Crossref 5.3.1 XML schema definition <https://data.crossref.org/schemas/common5.3.1.xsd>`_. The script needs a yml file
with the parts described above and path to files.

----------------------
Finalizing XML Deposit
----------------------

Finally, run `lxml_trasform.py <https://github.com/markpbaggett/crossref_batch/blob/main/utilities/lxml_transform.py>`_
to remove blank elements.

Then, take that XML file and upload it to Crossref for testing.

First, check that your `XML is wellformed and valid <https://apps.crossref.org/XSDParse/>`_.

Next, upload your XML file to `the test system <https://test.crossref.org>`_ for proceesing.

Finally, if all is good, upload to `the production system <https://doi.crossref.org>`_.

