======================
Conference Proceedings
======================

.. warning::
    While Crossref allows you to mint DOIs for conference proceedings, please note that we do not model our conference
    proceedings in VolJournals (e.g. NSQP) as conference proceedings.  While information here may be useful, please see
    the Journal Articles section for procedures on batch registration of DOIs.

Crossref allows you to perform batch operations for "series conference proceedings" and "nonseries conference proceedings."
The elements allowed, required, and recommended vary based on the option you select. More details can be found about
this in the `schema documentation <https://data.crossref.org/reports/help/schema_doc/5.3.1/index.html>`_.

----------
Conference
----------

The :code:`conference` element holds all other elements. It :code:`MUST` include:

* 1 :code:`event_metadata` element
* either:
    * 1 :code:`proceedings_metadata` element (use for non-series)
    * 1 :code:`proceedings_series_metadata` element (use for series)

It :code:`MAY` include:

* 0-1 :code:`contributors` element
* 0-n :code:`conference_paper` elements

For more information, please refer to the `schema documentation <https://data.crossref.org/reports/help/schema_doc/5.3.1/index.html>`_.

-----------------------
Series Versus Nonseries
-----------------------

Anatomy of Series Conference Proceedings
========================================

Series conference proceedings :code:`MUST` include a :code:`proceedings_series_metadata` element. This element must include:

* 1 :code:`series_metadata` element
* 1-5 :code:`publisher` elements
* 1-10 :code:`publication_date` elements
* 1 of:
    * 1 :code:`proceedings_title` element and / or 1 :code:`volume` element
    * 1 :code:`volume` element
* 1 of:
    * 1 :code:`isbn`
    * 1 :code:`noisbn`

The element :code:`MAY` include:

* 0-1 :code:`proceedings_subject`
* 0-1 :code:`publisher_item`
* 0-1 :code:`archive_locations`
* 0-1 :code:`doi_data`


Anatomy of Non-Series Conference Proceedings
============================================

Non-series conference proceedings :code:`MUST` include a :code:`proceedings_metadata` element. This element must include:

* 1 :code:`proceedings_title` element
* 1-5 :code:`publisher` elements
* 1-10 :code:`publication_date` elements
* 1 of:
    * 1 :code:`isbn`
    * 1 :code:`noisbn`

The element :code:`MAY` include:

* 0-1 :code:`proceedings_subject`
* 0-1 :code:`publisher_item`
* 0-1 :code:`archive_locations`
* 0-1 :code:`doi_data`

------------------------------------------------------
Generating Metadata for Conference Proceedings Deposit
------------------------------------------------------

To generate a metadata upload, first build a :code:`YAML` file that includes:

* the path to the files that describe your papers
* the various contributors responsible for the conference
* event metadata about the conference
* metadata about the conference series
* information about who is depositing the metadata

Adding Path to Files
====================

The path to files is defined with a :code:`path` key and the value of where to find the files on disk. Recursive file
submission is allowed (your metadata files don't need to be in 1 directory).

.. code-block:: yaml

    path: "output/output"

Adding Contributors
===================

Contributors are defined in a :code:`contributors` key and describe who is related to the conference. There are many
elements allowed here, but only a few are used by our code.

The value is an array. Currently, each value in the array must have a :code:`given` name that includes first / middle name, a
:code:`surname` that is the last name, a :code:`role` and a :code:`sequence` value, and an :code:`insitution` element with
an :code:`institution_name`.  The :code:`role` element must be one of: author, editor, chair, reviewer, review-assistant,
stats-reviewer, reviewer-external, reader, translator. The :code:`sequence` must  be one of: first or additional. A
contributor can also have a :code:`suffix` and a :code:`institution_department` in its :code:`institution`.

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

Event Metadata about the Conference
===================================

The :code:`event_metadata` key contains all information about the conference.  All included keys are currently
required.

.. code-block:: yaml

    event_metadata:
      conference_name: "Quail 9: National Quail Symposium"
      conference_number: 9
      conference_location: Springfield, Missouri
      conference_date:
        start_month: 08
        start_year: 2022
        start_day: 01
        end_month: 08
        end_year: 2022
        end_day: 05

Metadata about the Conference Series
====================================

The :code:`proceedings_series_metadata` key includes all data about the conference.  Currently, only conference series
are supported.  All keys beelow are required.

.. code-block:: yaml

    proceedings_series_metadata:
      proceedings_title: "Quail 9: National Quail Symposium Proceedings"
      publisher: Clemson University, National Bobwhite Conservation Initiative Technical Committee
      publication_date:
        year: 2022
      volume: 9
      series_metadata:
        titles:
          title: National Quail Symposium Proceedings
        issn: 2573-5667

Depositor Information
=====================

The :code:`head` key holds all information about this deposit. All elements are required.

.. code-block:: yaml

    head:
      doi_batch_id: utk_nqsp_9_10_2022
      timestamp: "20221014080808"
      depositor:
        depositor_name: Mark Baggett
        email_address: mbagget1@utk.edu
      registrant: University of Tennessee

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
------------------

Finally, run `lxml_trasform.py <https://github.com/markpbaggett/crossref_batch/blob/main/utilities/lxml_transform.py>`_
to remove blank elements.

Then, take that XML file and upload it to Crossref for testing.

First, check that your `XML is wellformed and valid <https://apps.crossref.org/XSDParse/>`_.

Next, upload your XML file to `the test system <https://test.crossref.org>`_ for proceesing.

Finally, if all is good, upload to `the production system <https://doi.crossref.org>`_.
