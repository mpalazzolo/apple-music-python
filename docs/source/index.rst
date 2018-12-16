Welcome to apple-music-python's documentation!
==============================================

A python wrapper for the Apple Music API.

See the `Apple Music API documentation <https://developer.apple.com/documentation/applemusicapi/about_the_apple_music_api>`_ for additional info:

**NOTE:** This does not support library resources.

Prerequisites
^^^^^^^^^^^^^

You must have an Apple Developer Account and a MusicKit API Key.
See instructions on how to obtain these here: `Getting Keys And Creating Tokens <https://developer.apple.com/documentation/applemusicapi/getting_keys_and_creating_tokens>`_.

Dependencies
^^^^^^^^^^^^

* `Requests <https://github.com/requests/requests>`_
* `PyJWT <https://github.com/jpadilla/pyjwt>`_

Installation
^^^^^^^^^^^^
::

    python setup.py install

or::

    pip install apple-music-python

Example
^^^^^^^
::

    import applemusicpy

    secret_key = 'x'
    key_id = 'y'
    team_id = 'z'

    am = applemusicpy.AppleMusic(secret_key, key_id, team_id)
    results = am.search('travis scott', types=['albums'], limit=5)

    for item in results['results']['albums']['data']:
        print(item['attributes']['name'])

:mod:`client` Module
^^^^^^^^^^^^^^^^^^^^

.. automodule:: applemusicpy.client
    :members:
    :special-members: __init__

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Versioning
^^^^^^^^^^

v1.0.0 - Initial Release - 12/15/2018

Authors
^^^^^^^

* **Matt Palazzolo** - `GitHub Profile <https://github.com/mpalazzolo>`_

License
^^^^^^^
https://github.com/mpalazzolo/applemusicpython/LICENSE.txt

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
