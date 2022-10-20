======================
Conference Proceedings
======================

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
