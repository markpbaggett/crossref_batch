============================
Working with Digital Commons
============================

The University of Tennessee Libraries currently uses Digital Commons as its institutional repository platform. Metadata
about each work in the repository is available via an AWS Bucket in a not schema defined XML format. This section
describes a workflow go getting the files you need for content registration.

----------------------------------------------------------------
Recursively Copying XML Files Based on Digital Commons Practices
----------------------------------------------------------------

In order to save time, we first need to download all files that are pertinent for content registration. To do this, a
python file is available in this repository at :code:`/utilities/copy_metadata_only.py`.  The file contains one function
that uses the :code:`os` library to recursively copy files from a path to another destination:

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