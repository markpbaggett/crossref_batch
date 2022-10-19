======================
Conference Proceedings
======================

Crossref allows you to perform batch operations for "series conference proceedings" and "nonseries conference proceedings."
The elements allowed, required, and recommended vary based on the option you select.

----------------------------------------
Anatomy of Series Conference Proceedings
----------------------------------------

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

----------------------------------------
Anatomy of Non-Series Conference Proceedings
----------------------------------------

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