.. image:: https://github.com/nlesc-nano/insilico-server/workflows/build/badge.svg
   :target: https://github.com/nlesc-nano/insilico-server/actions
.. image:: https://readthedocs.org/projects/insilico-server/badge/?version=latest
   :target: https://insilico-server.readthedocs.io/en/latest/?badge=latest
.. image:: https://codecov.io/gh/nlesc-nano/insilico-server/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/nlesc-nano/insilico-server

###############
insilico-server
###############
This web service provides an interface to retrieve and store simulation data,
without the user's manual intervention. See `documentation <https://insilico-server.readthedocs.io/en/latest/>`_.


Installation
************

1.🐳 Install `Docker <https://www.docker.com/>`_

2. 🚀 Define a environment variable `MONGO_PASSWORD` with the database password.  Now you need to run the following
   command to start both the server and the  mongodb
::
   provisioning/start_app.sh


Contributing
************

If you want to contribute to the development of insilico-server,
have a look at the `contribution guidelines <CONTRIBUTING.rst>`_.

License
*******

Copyright (c) 2020, Netherlands eScience Center

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.



Credits
*******

This package was created with `Cookiecutter <https://github.com/audreyr/cookiecutter>`_ and the `NLeSC/python-template <https://github.com/NLeSC/python-template>`_.
