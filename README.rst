pyplagiarism - Plagiarism Tool for Python Source Code
==========================================================================


You can find the detailed documentation here: https://www.egr.msu.edu/coinlab/blankjul/pyplagiarism/


|travis| |python| |license|


.. |travis| image:: https://travis-ci.com/julesy89/pyplagiarism.svg?branch=master
   :alt: build status
   :target: https://travis-ci.com/julesy89/pyplagiarism

.. |python| image:: https://img.shields.io/badge/python-3.6-blue.svg
   :alt: python 3.6

.. |license| image:: https://img.shields.io/badge/license-apache-orange.svg
   :alt: license apache
   :target: https://www.apache.org/licenses/LICENSE-2.0


An example of using pyplagiarism is provided below. This uses directly the API.
In the future, we are planning to provide a command line tool in addition.


.. code:: python

    
    from pyplagiarism.tool import plagiarism

    a = """
    def calculate():
        x = 6
        y = 5
        return x + y
    """

    b = """
    def calculate():
        return 5 + 6
    """

    c = """
    def calculate():
        x = 6
        y = 5
        return x + y
    """

    data = {"a": a, "b": b, "c": c}

    plagiarism(data, visualize_as_html=False, diff_of_files=False)
