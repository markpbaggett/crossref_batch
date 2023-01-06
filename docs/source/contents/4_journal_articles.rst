=================================
Minting DOIs for Journal Articles
=================================

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

---------------------------------------------
Creating Metadata about the Journal and Issue
---------------------------------------------


--------------------
Journal Batch Writer
--------------------

