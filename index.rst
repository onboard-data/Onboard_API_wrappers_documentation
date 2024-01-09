Onboard Data API Bindings documentation
===========================================

.. tabs::
    .. group-tab:: Python

        .. image:: https://readthedocs.org/projects/onboard-docs-test/badge/?version=latest
            :target: https://onboard-docs-test.readthedocs.io/en/latest/?badge=latest

        .. image:: https://badge.fury.io/py/onboard.client.svg
            :target: https://badge.fury.io/py/onboard.client

        .. image:: https://shields.io/pypi/pyversions/onboard.client.svg
            :target: https://pypi.org/project/onboard.client/

        .. image:: https://camo.githubusercontent.com/3656aeb94541a2464bac21509c34b7942cf127702885cd6ce0002120d2bfa189/68747470733a2f2f696d672e736869656c64732e696f2f707970692f6c2f6f6e626f6172642e636c69656e74
            :target: https://camo.githubusercontent.com/3656aeb94541a2464bac21509c34b7942cf127702885cd6ce0002120d2bfa189/68747470733a2f2f696d672e736869656c64732e696f2f707970692f6c2f6f6e626f6172642e636c69656e74

    .. group-tab:: R

        .. image:: https://www.r-pkg.org/badges/version/dplyr
            :target: https://cran.r-project.org/web//packages/OnboardClient/



This package provides Python and R bindings to `Onboard Data's <https://onboarddata.io/>`_ building data API, allowing easy and lightweight access to building data.

For example, we can retrieve the last week of temperature data from all Zone Temperature points associated with FCUs in the Laboratory building:


.. tabs::

   .. code-tab:: py

    import pandas as pd
    from onboard.client import OnboardClient
    from onboard.client.dataframes import points_df_from_streaming_timeseries
    from onboard.client.models import PointSelector, TimeseriesQuery, PointData
    from datetime import datetime, timezone, timedelta
    from typing import List
    import pytz
    client = OnboardClient(api_key='your-api-key-here')

    print(list(pd.DataFrame(client.get_all_buildings())['name'])) # returns list of buildings that you have access to (you may not have 'Laboratory' in your set)

    query = PointSelector()
    query.point_types     = ['Zone Temperature'] # can list multiple point types,
    query.equipment_types = ['fcu']              # equipment types,
    query.buildings       = ['Laboratory']       # buildings, etc.
    selection = client.select_points(query)

    start = pd.Timestamp("2022-03-29 00:00:00", tz="utc")
    end = pd.Timestamp("2022-07-29 00:00:00", tz="utc")

    timeseries_query = TimeseriesQuery(point_ids = selection['points'], start = start, end = end)
    sensor_data = points_df_from_streaming_timeseries(client.stream_point_timeseries(timeseries_query))


   .. code-tab:: r R
   
    install.packages(c('OnboardClient', 'lubridate'))       # install whatever libraries you don't already have
    library(OnboardClient)
    library(lubridate)                                      # for datetime handling

    api.setup()                                             # will prompt for api key
    query <- PointSelector()                                # create point selector
    query$point_types       <- c('Zone Temperature')        # can list multiple point types
    query$equipment_types   <- c('fcu')                     # equipment types,
    query$buildings         <- c('Laboratory')              # buildings, etc.
    selection <- select_points(query)

    start <- as_datetime("2022-03-29 00:00:00", tz = "UTC")
    end <- as_datetime("2022-07-29 00:00:00", tz = "UTC")

    sensor_data <- get_timeseries(start_time = start, end_time = end, point_ids = selection$points) #Queries timeseries data for the selection list we got above

and to plot:

.. tabs::
    .. code-tab:: py

        import matplotlib.pyplot as plt
        import numpy as np
        # set the timestamp as the index and forward fill the data for plotting
        sensor_data_clean = sensor_data.set_index('timestamp').astype(float).ffill()
        # Edit the indexes just for visualization purposes
        indexes = [i.split('T')[0] for i in list(sensor_data_clean.index)]
        sensor_data_clean.index = indexes
        fig = sensor_data_clean.plot(figsize=(15,8), fontsize = 12)
        fig.set_ylabel('Fahrenheit',fontdict={'fontsize':15})
        fig.set_xlabel('time stamp',fontdict={'fontsize':15})
        plt.show()

    .. code-tab:: r R

        library(tidyverse)

        sensor_data_clean <- sensor_data %>% 
          mutate(timestamp = floor_date(timestamp, unit = "seconds")) %>%
          pivot_longer(-timestamp, names_to = "sensor", values_to = "value") %>%
          drop_na(value) %>%
          arrange(timestamp)
          
        sensor_data_clean %>% 
          ggplot(aes(x = timestamp, y = value, color = sensor)) +
          geom_line()


.. tabs::
    .. group-tab:: Python
        .. image:: images/python_example_plot.png

    .. group-tab:: R
        .. image:: images/r_example_plot.png

For installation instructions, and to get set up with API access, refer to `Initial Setup <https://onboard-data-python-client-api.readthedocs.io/en/latest/Initial%20Setup.html>`_.

.. note::

   While we are committed to backwards-compatibility, this project is under active development. If you discover a feature that would be helpful, or any unexpected behavior, please contact us at support@onboarddata.io. 

Contents
--------

.. toctree::

   Initial Setup
   Querying Data Model
   Querying Building-Specific Data
   Column Definitions

License
-------

Copyright 2018-2024 Onboard Data Inc

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
