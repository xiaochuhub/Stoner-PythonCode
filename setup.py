import os
from setuptools import setup, find_packages
import Stoner
import re
import sys, io


def yield_sphinx_only_markup(lines):
    """
    :param file_inp:     a `filename` or ``sys.stdin``?
    :param file_out:     a `filename` or ``sys.stdout`?`

    """
    substs = [
        ## Selected Sphinx-only Roles.
        #
        (r':abbr:`([^`]+)`',        r'\1'),
        (r':ref:`([^`]+)`',         r'`\1`_'),
        (r':term:`([^`]+)`',        r'**\1**'),
        (r':dfn:`([^`]+)`',         r'**\1**'),
        (r':(samp|guilabel|menuselection):`([^`]+)`',        r'``\2``'),
        (r':py:[a-z]+:`([^`]+)`',        r'\1'),
        


        ## Sphinx-only roles:
        #        :foo:`bar`   --> foo(``bar``)
        #        :a:foo:`bar` XXX afoo(``bar``)
        #
        #(r'(:(\w+))?:(\w+):`([^`]*)`', r'\2\3(``\4``)'),
        (r':(\w+):`([^`]*)`', r'\1(``\2``)'),


        ## Sphinx-only Directives.
        #
        (r'\.\. doctest',           r'code-block'),
        (r'\.\. plot::',            r'.. '),
        (r'\.\. seealso',           r'info'),
        (r'\.\. glossary',          r'rubric'),
        (r'\.\. figure::',          r'.. '),


        ## Other
        #
        (r'\|version\|',              r'x.x.x'),
    ]

    regex_subs = [ (re.compile(regex, re.IGNORECASE), sub) for (regex, sub) in substs ]

    def clean_line(line):
        try:
            for (regex, sub) in regex_subs:
                line = regex.sub(sub, line)
        except Exception as ex:
            print("ERROR: %s, (line(%s)"%(regex, sub))
            raise ex

        return line

    for line in lines:
        yield clean_line(line)

def read(fname):
    mydir=os.path.dirname(__file__)
    with io.open(os.path.join(mydir, fname)) as fd:
        return fd.readlines()

def requires(fname):
    mydir=os.path.dirname(__file__)
    with io.open(os.path.join(mydir, fname)) as fd:
        entries=fd.readlines()
        entries=[entry for entry in entries if entry[0] not in " #\n\t"]
        return entries

setup(
    name = "Stoner",
    version = str(Stoner.__version__),
    author = "Gavin Burnell",
    author_email = "g.burnell@leeds.ac.uk",
    description = ("""The Stoner Python package is a set of utility classes for writing data analysis code. It was written within the 
                   Condensed Matter Physics group at the University of Leeds as a shared resource for quickly writing simple programs 
                   to do things like fitting functions to data, extract curve parameters, churn through large numbers of small text 
                   data files and work with certain types of scientific image files"""),
    license = "GPLv3",
    keywords = "Data-Analysis Physics",
    url = "http://github.com/~gb119/Stoner-PythonCode",
    packages=find_packages(),
    package_dir={'Stoner': 'Stoner'},
    package_data={'Stoner':['stylelib/*.mplstyle']},
    test_suite="tests",
    install_requires=requires("requirements.txt"),
    long_description= ''.join(yield_sphinx_only_markup(read('doc/readme.rst'))),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
