Initial Setup
=============

Installation
------------

You can install your client of choice through official means:

.. tabs::
   .. code-tab:: py Python
   
      >>> # use pip for the python client
      >>> # requires Python >= 3.7.
      >>> pip install onboard.client

   .. code-tab:: r R

      > # use CRAN for the R client (stable)
      > install.packages('OnboardClient')

or using github:

.. tabs::
   .. code-tab:: bash Python

      $ # clone from terminal
      $ git clone git@github.com:onboard-data/client-py

   .. code-tab:: r R

      > # This is the development (unstable) version of our package
      > install.packages('devtools') # Install devtools package first
      > devtools::install_github(repo='onboard-data/client-R') # install from github

.. note::
   The github version of the R client is our active development environment. It may include cool new features, but is not guaranteed to be as stable as the official release! Proceed at your own risk.


Setting up API access
---------------------

You’ll need an active API Key with the appropriate scopes in order to use this python client.

If you are an existing Onboard user you can head over to your `account's api keys page <https://portal.onboarddata.io/account?tab=api>`_ and generate a new key and grant scopes for :code:`general` and :code:`buildings:read`.

If you would like to get access to Onboard and start prototyping against an example building please `request access here <https://www.onboarddata.io/sandbox>`_.

You can test if your API key is working with the following code:

.. tabs::
   .. code-tab:: py

      >>> from onboard.client import OnboardClient
      >>> client = OnboardClient(api_key='your-api-key-here')
      >>>
      >>> # Verify access & connectivity
      >>> client.whoami()
      {'result': 'ok', 'apiKeyInHeader': True, ... 'authLevel': 4}

   .. code-tab:: r R

      > library(OnboardClient)
      > api.setup() # in dev version, this will automatically return the server status message
      > api.status()
      [1] "Success: (200) OK"

You can also retrieve a list of your currently authorized scopes with :code:`client.whoami()['apiKeyScopes']` in Python or :code:`api.get('whoami')$apiKeyScopes` in R.

Note about data structure
-------------------------

Calls to the API (such as :code:`client.get_equipment_types()`) return JSON objects by default. For the Python client, we have left the API wrapper functions as returning the API return directly, without further alteration. In this documentation, we will be converting these objects to pandas dataframes by wrapping our API calls in pd.DataFrame(). For the R package, on the other hand, all wrapper functions convert the JSON to data.frames.