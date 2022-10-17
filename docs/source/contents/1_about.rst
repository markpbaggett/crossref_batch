=====
About
=====

The procedures here describe the workflows, utilities, and processes used to perform Crossref Batch operations at UT
Libraries. These procedures are used to `register persistent identifiers <https://youtu.be/G9mIUvXrTLc?t=203>`_ (DOIs)
in batch by registering our content with Crossref.

While there is significant documentation available for registering content in the
`Crossref documentation portal <https://www.crossref.org/documentation/>`_, this documentation has been tailored to
describe the procedures and utilities used to generate identifiers using our systems.

----------------------------
Content Registration Methods
----------------------------

There are two ways to register content with Crossref: `the web deposit form <https://www.crossref.org/documentation/content-registration/web-deposit-form/>`_
and direct deposit of XML. Direct deposit of XML is necessary when you need to do a batch registration or register DOIs
for particular work types including: datasets, peer reviews, posted content (including preprints), standards, and pending
publications. More details can be found online in Crossref's
`choosing a content registration method <https://www.crossref.org/documentation/register-maintain-records/choose-content-registration-method/>`_.

For direct deposit of XML, there are three methods: `Upload JATS XML using the web deposit form <https://www.crossref.org/documentation/content-registration/web-deposit-form/>`_,
`Upload XML files using the Crossref admin tool <https://www.crossref.org/documentation/member-setup/direct-deposit-xml/admin-tool/>`_,
and `XML Deposit using HTTPS Post <https://www.crossref.org/documentation/member-setup/direct-deposit-xml/https-post/>`_.
More details about each of these options can be found on the `Direct deposit of XML portal <https://www.crossref.org/documentation/register-maintain-records/direct-deposit-xml/>`_.

-------------------------
Special characters in XML
-------------------------

All XML submitted to Crossref must be UTF-8 encoded. There are two ways to include a special unicode character in a
Crossref deposit XML file. The simplest option and preferred approach according to Crossref is to encode the special
character using a numerical representation. For example, :code:`Šumbera` can be encoded as:

.. code-block:: xml
    <surname>&#352;umbera</surname>

