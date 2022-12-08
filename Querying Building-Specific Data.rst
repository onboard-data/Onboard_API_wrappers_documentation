Querying Building-Specific Data
================================

For column definitions, see :ref:`bsp-reference-label`.

Querying Equipment
------------------

Using the API, we can retrieve the data from all the buildings that belong to our organization:

.. tabs::
    .. code-tab:: py

        >>> # Get a list of all the buildings under your Organization
        >>> pd.json_normalize(client.get_all_buildings())
            id  org_id             name  ... point_count info.note info
        0   66       6   T`Challa House  ...          81            NaN
        1  427       6  Office Building  ...        4219       NaN  NaN
        2  428       6       Laboratory  ...        2206       NaN  NaN
        3  429       6         Hogwarts  ...        4394       NaN  NaN

    .. code-tab:: r R

        # Get a list of all the buildings under your Organization
        get_buildings() %>% select_if(~ !any(is.na(.))) # select call drops columns with all NAs
        #   id org_id            name         timezone status equip_count point_count
        #1  66      2  T`Challa House America/New_York   LIVE          18         171
        #2 427      6 Office Building America/New_York   LIVE         137        2422
        #3 428      6      Laboratory America/New_York   LIVE         124        1658
        #4 429      2     Residential America/New_York   LIVE         311        4394



The first column of this dataframe (:code:`id`) contains the building identifier number.

In order to retrieve the equipment for a particular building (e.g. Laboratory, id: 428), we use :code:`get_building_equipment()`:


.. tabs::
    .. code-tab:: py

        >>> # Get a list of all equipment in a building
        >>> all_equipment = pd.DataFrame(client.get_building_equipment(428))
        >>> all_equipment[['id', 'building_id', 'equip_id',  'points', 'tags']]
                id  building_id        equip_id                                             points                     tags
        0    27293          428      crac-T-105  [{'id': 291731, 'building_id': 428, 'last_upda...             [crac, hvac]
        1    27294          428   exhaustFan-01  [{'id': 290783, 'building_id': 428, 'last_upda...  [fan, hvac, exhaustFan]
        2    27295          428  exhaustFan-021  [{'id': 289684, 'building_id': 428, 'last_upda...  [fan, hvac, exhaustFan]
        3    27296          428  exhaustFan-022  [{'id': 289655, 'building_id': 428, 'last_upda...  [fan, hvac, exhaustFan]

    .. code-tab:: r R
    
        ## TODO: make wrapper in R

Querying Specific Points
------------------------

In order to query specific points, first we need to instantiate the PointSelector:

.. tabs::
    .. code-tab:: py
    
        >>> from onboard.client.models import PointSelector
        >>> query = PointSelector()

    .. code-tab:: r R

        query <- PointSelector()


There are multiple ways to select points using the PointSelector. The user can select all the points that are associated with one or more lists containing any of the following::

    'organizations', 'buildings', 'point_ids', 'point_names', 'point_hashes',
    'point_ids', 'point_names', 'point_topics', 'equipment', 'equipment_types'

For example, here we make a query that returns all the points of the type 'Real Power' OR of the type 'Zone Temperature' that belong to the 'Laboratory' building:

.. tabs::
    .. code-tab:: py
        
        >>> query = PointSelector()
        >>> query.point_types = ['Real Power', 'Zone Temperature']
        >>> query.buildings = ['Laboratory']
        >>> selection = client.select_points(query)

    .. code-tab:: r R

        query <- PointSelector()
        query$point_types <- c('Real Power', 'Zone Temperature')
        query$buildings <- c('Laboratory')
        selection <- select_points(query)

We can add to our query to e.g. further require that returned points must be associated with the 'fcu' equipment type:

.. tabs::
    .. code-tab:: py

        >>> query = PointSelector()
        >>> query.point_types = ['Real Power', 'Zone Temperature']
        >>> query.equipment_types = ['fcu']
        >>> query.buildings = ['Laboratory']
        >>> selection = select_points(query)
        >>> selection
        {'buildings': [428],
        'equipment': [27356, 27357],
        'equipment_types': [9],
        'orgs': [6],
        'point_types': [77],
        'points': [289701, 289575]}

    .. code-tab:: r R

        query <- PointSelector()
        query$point_types <- c('Real Power', 'Zone Temperature')
        query$equipment_types <- c('fcu')
        query$buildings <- c('Laboratory')
        selection <- select_points(query)
        selection
        $orgs
        [1] 6

        $buildings
        [1] 428

        $equipment
        [1] 27356 27357

        $equipment_types
        [1] 9

        $point_types
        [1] 77

        $points
        [1] 289701 289575

In this example, the points with ID=289701, and 289575 are the only ones that satisfy the requirements of our query.

We can get more information about these points by calling the function :code:`get_points_by_ids()` on the :code:`points` field in the :code:`selection` entity:

.. tabs::
    .. code-tab:: py

        >>> # Get metadata for the sensors you would like to query
        >>> sensor_metadata = client.get_points_by_ids(selection['points'])
        >>> sensor_metadata_df = pd.DataFrame(sensor_metadata)
        >>> sensor_metadata_df[['id', 'building_id', 'first_updated', 'last_updated', 'type', 'value', 'units']]
               id  building_id  first_updated  last_updated              type value              units
        0  289575          428   1.626901e+12  1.641928e+12  Zone Temperature  66.0  degreesFahrenheit
        1  289701          428   1.626901e+12  1.641928e+12  Zone Temperature  61.0  degreesFahrenheit

    .. code-tab:: r R

        # Get metadata for the sensors you would like to query
        sensor_metadata_df <- get_points_by_ids(selection$points) %>% 
            select(id, building_id, first_updated, last_updated, type, value, units)
        #      id building_id first_updated last_updated             type value             units
        #1 289575         428  1.626901e+12 1.669934e+12 Zone Temperature  68.0 degreesFahrenheit
        #2 289701         428  1.626901e+12 1.669934e+12 Zone Temperature  64.0 degreesFahrenheit

:code:`sensor_metadata_df` now contains a dataframe with rows for each point. Based on the information about these points, we can observe that none of the points of our list belongs to the point type 'Real Power', but only to the point type 'Zone Temperature'

Exporting Data to .csv
-----------------------

Data extracted using the API can be exported to a .csv or excel file like so:

.. tabs::
    .. code-tab:: py

        >>> # Save metadata to .csv file
        >>> sensor_metadata_df.to_csv('./metadata_query.csv')

    .. code-tab:: r R

        # Save metadata to .csv file
        write.csv(sensor_metadata_df, file = "./metadata_query.csv")

Querying Time-Series Data
-------------------------

To query time-series data first we need to import relevant helper modules/packages.

.. tabs::
    .. code-tab:: py

        >>> from datetime import datetime, timezone, timedelta
        >>> import pytz
        >>> from onboard.client.models import TimeseriesQuery, PointData
        >>> from onboard.client.dataframes import points_df_from_streaming_timeseries

    .. code-tab:: r R

        # install.packages('lubridate') # install if you haven't already
        library(lubridate)

We select the range of dates we want to query, making sure to specify timezones:

.. tabs::
    .. code-tab:: py

        >>> start = pd.Timestamp("2022-03-29 00:00:00", tz="utc")
        >>> end = pd.Timestamp("2022-07-29 00:00:00", tz="utc")

    .. code-tab:: r R
    
        start <- as_datetime("2022-03-29 00:00:00", tz = "UTC")
        end <- as_datetime("2022-07-29 00:00:00", tz = "UTC")


Now we are ready to query the time-series data for the points we previously selected in the specified time-period

.. tabs::
    .. code-tab:: py

        >>> # Get time series data for the sensors you would like to query
        >>> timeseries_query = TimeseriesQuery(point_ids = selection['points'], start = start, end = end)
        >>> sensor_data = points_df_from_streaming_timeseries(client.stream_point_timeseries(timeseries_query))
        >>> sensor_data
                                 timestamp  289575 289701
        0      2022-01-04T19:34:11.741000Z  NaN   60.0
        1      2022-01-04T19:34:19.143000Z  62.0  NaN
        2      2022-01-04T19:35:12.133000Z  NaN   60.0

    .. code-tab:: r R

        sensor_data <- get_timeseries(start_time = start, end_time = end, point_ids = selection$points) #Queries timeseries data for the selection list we 
        sensor_data
        #   timestamp           `289575` `289701`
        #   <dttm>                 <int>    <int>
        #1  2022-03-29 00:00:24       62       NA
        #2  2022-03-29 00:01:25       62       NA
        #3  2022-03-29 00:02:26       62       NA


This returns a dataframe containing columns for the timestamp and for each requested point. And now we can plot these data:

.. tabs::
    .. code-tab:: py

        >>> # set the timestamp as the index and forward fill the data for plotting
        >>> sensor_data_clean = sensor_data.set_index('timestamp').astype(float).ffill()
        >>>
        >>> # Edit the indexes just for visualization purposes
        >>> indexes = [i.split('T')[0] for i in list(sensor_data_clean.index)]
        >>> sensor_data_clean.index = indexes
        >>>
        >>> fig = sensor_data_clean.plot(figsize=(15,8), fontsize = 12)
        >>>
        >>> # Adding some formatting
        >>> fig.set_ylabel('Farenheit',fontdict={'fontsize':15})
        >>> fig.set_xlabel('time stamp',fontdict={'fontsize':15})

    .. code-tab:: r R

        library(tidyverse)
        # now, wrangle to tidy format:
        sensor_data_clean <- sensor_data %>% 
              mutate(timestamp = floor_date(timestamp, unit = "seconds")) %>%
              pivot_longer(-timestamp, names_to = "sensor", values_to = "value") %>%
              drop_na(value) %>%
              arrange(timestamp)
        # and plot:  
        sensor_data_clean %>% 
              ggplot(aes(x = timestamp, y = value, color = sensor)) +
              geom_line()


.. tabs::
    .. group-tab:: Python
        .. image:: images/python_example_plot.png

    .. group-tab:: R
        .. image:: images/r_example_plot.png
