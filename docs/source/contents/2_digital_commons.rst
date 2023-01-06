============================
Working with Digital Commons
============================

The University of Tennessee Libraries currently uses Digital Commons as its institutional repository platform.

In order to mint DOIs for works in Digital Commons, we need to associate a new DOI with the metadata of a work either
through the form in the GUI or via a batch process. Associating the DOIs first allows us to easily find associated metadata
that is required by Crossref for minting and aids in discovery of the works in other systems once the Crossref batch
minting is completed. The DOI needs to be unique and based on our prefix, but the pattern for each work is determined by
Scholarly Communications.

Once each metadata record has been updated and has a place holder DOI, we can download the metadata in batch from Digital
Commons. The code here works around the full metadata records available to us in the AWS bucket (not the CSV). This metadata
is not schema defined, but the information below and subsequent scripts describes the workflow for downloading the needed
files and registering content based on our practices.

----------------------------------------------------------------
Recursively Copying XML Files Based on Digital Commons Practices
----------------------------------------------------------------

In order to save time, we first need to download all files that are pertinent for content registration. To do this, a
python file is available in this repository at :code:`/utilities/copy_metadata_only.py`.  The file contains one function
that uses the :code:`os` library to recursively copy files from a path to another destination.

.. code-block:: python

    def copy_metadata_files(path, filename_pattern, output):
        for path, directories, files in os.walk(path):
            for file in files:
                if file == filename_pattern:
                    with open(f"{output}/{path.split('/')[-1]}.xml", 'w') as write_file:
                        with open(f"{path}/{file}", 'r') as read_file:
                            for line in read_file:
                                write_file.write(line)

Argument parsing allows you to specify this information from the CLI.

.. code-block:: shell

    python copy_metadata_files.py -p /vhosts/s3-utkbepress/trace.tennessee.edu/nqsp/vol9/iss1 -o output

When the above is ran, all :code:`metadata.xml` files are copied from the value of the :code:`-p` flag to the value of
the :code:`-o` flag.

Please note that while this works recursively, the other scripts expect this data to be in one directory with no
subdirectories. Because of this,if you use the script described above, you'll need to run it on an issue by issue basis
or it will overwrite other files.

-------------------------------
Encoding of Digital Commons XML
-------------------------------

XML files from Digital Commons are not encoded as :code:`UTF-8`. Instead, these documents are encoded as :code:`iso-8859-1`.
This is important because Crossref expects :code:`UTF-8`, and we must be careful to create this. Instructions on how to
force this are described in the following chapter(s).

