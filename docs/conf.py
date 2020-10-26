# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys
import time

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))

import gcip  # noqa: E402 isort:skip

# -- Project information -----------------------------------------------------

project = "gcip"
copyright = f'2020-{time.strftime("%Y")}, DB Systel'
author = "Thomas Steinbach"

# The full version, including alpha/beta/rc tags
release = gcip.__version__
version = gcip.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.intersphinx",
    "autoapi.extension",
    "sphinx.ext.viewcode",
    "sphinxcontrib.napoleon",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_autoapi_templates", "_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- autoapi configuration -----------------------------------------------
autoapi_type = "python"
autoapi_dirs = ["../gcip"]
autoapi_member_order = "groupwise"
autoapi_template_dir = "_autoapi_templates"
autoapi_options = [
    "imported-members",
    "members",
    "show-inheritance",
    # "special-members",
    "undoc-members",
]
autoapi_python_class_content = "both"

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_style = "css/custom.css"
html_theme_options = {
    "prev_next_buttons_location": "both"
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
