Updating TRACE
==============

About
-----

Ocassionally, we may be asked to also update TRACE with recently minted DOIs.  This describes my process for doing that.

The Process
-----------

In order to update Trace, first you need to be a spreadsheet for batch revising metadata.  To do this, login to Trace
and navigate to the Journal and follow the process described `here <https://bepress.com/reference_guide_dc/batch-upload-export-revise/>`_.

Once you have the spreadsheet, you need to add the DOIs to the spreadsheet.  To do this, you need to open the :code:`xls`
file and save it as a CSV.

Then you can open :code:`utilities/update_trace.py` with the path to your original CSVs that include your DOI, the pattern
for those CSVs assuming the path includes things you don't care about, and adding the CSV file you just created.

.. code-block:: python

    if __name__ == "__main__":
        x = CrossrefCSVs('csvs', 'JAEPL*')
        t = TraceCSV('jaepl_1.xls_Mon_May_08_08_15_05_2023part_1.csv', x.dois_and_urls)
        t.write()

This will create a new file called :code:`dois_for_trace.txt` formatted so that you can copy and paste the results
back into your original XLS.
