Querying Data Model
===================

Onboard's data model contains both equipment types (e.g. fans, air handling units) and point types (e.g. zone temperature). We can query the full data model within our API.

Data model column definitions for each of the below tables can be found in :ref:`data model columns page<dm-reference-label>`.

Equipment types
---------------

First, we query equipment types.

.. tabs::
   .. code-tab:: py

      >>> from onboard.client import OnboardClient
      >>> client = OnboardClient(api_key='')
      >>> import pandas as pd
      >>> # this query returns a JSON object, 
      >>> # which we convert to data frame using pd.json_normalize()
      >>> equip_type = pd.json_normalize(client.get_equipment_types())


   .. code-tab:: r R

      > library(OnboardClient)
      > library(tidyverse)
      > api.setup()
      > get_equip_types() 

.. tabs::
    .. group-tab:: Python
        .. image:: images/py_equip_types_df.png

    .. group-tab:: R
        .. image:: images/r_equip_types_df.png


While the R client expands nested lists (meaning there is a row for each subtype), the Python client has one row per equipment type, meaning the sub-equipment types are nested as dataframes within each row. In the Python client, you can list subtypes for an equipment type (e.g. 'fan') like so:

   >>> sub_type = pd.DataFrame(equip_type[equip_type.tag_name == 'fan']['sub_types'].item())
      id  equipment_type_id         tag_name          name_long name_abbr
   0  12                 26       exhaustFan        Exhaust Fan       EFN
   1  13                 26        reliefFan         Relief Fan      RlFN
   2  14                 26        returnFan         Return Fan       RFN
   3  15                 26        supplyFan         Supply Fan       SFN
   ...


Note that not all equipment types have associated sub-types.

Point types
-----------

Accessing point types is very similar:

.. tabs::
   .. code-tab:: py

      >>> # Get all point types from the Data Model
      >>> point_types = pd.DataFrame(client.get_all_point_types())
      >>> point_types[['id', 'tag_name', 'tags']]
            id                                  tag_name                                            tags
      0    124                 Occupied Heating Setpoint             [air, sp, temp, zone, heating, occ]
      1    118                Outside Air Carbon Dioxide                     [air, co2, sensor, outside]
      2    130           Return Air Temperature Setpoint                         [air, sp, temp, return]
      3     84  Dual-Temp Coil Discharge Air Temperature  [air, discharge, dualTemp, sensor, temp, coil]

   .. code-tab:: r R

      > point_types <- get_point_types()
      > point_types %>% select(id, point_type, tags) %>% distinct()
      #   id    point_type                                   tags
      #1  124   Occupied Heating Setpoint                    "air", "sp", "temp", "zone", "heating", "occ"
      #2  118   Outside Air Carbon Dioxide                   "air", "co2", "sensor", "outside"
      #3  130   Return Air Temperature Setpoint              "air", "sp", "temp", "return"
      #4  84    Dual-Temp Coil Discharge Air Temperature     "air", "discharge", "dualTemp", "sensor", "temp", "coil"

:code:`point_types` is now a dataframe listing all the tags associated with each point type.

.. note::
   In the following, convenience wrapper functions are currently only available on the development version of the R package. For the official version, use each respective :code:`api.get()` call mentioned in the code.

We can extract the metadata associated with each tag in our data model like so:

.. tabs::
   .. code-tab:: py
   
      >>> # Get all tags and their definitions from the Data Model
      >>> pd.DataFrame(client.get_tags())
            id        name                                         definition def_source                                            def_url
      0    120     battery  A container that stores chemical energy that c...      brick  https://brickschema.org/ontology/1.1/classes/B...
      1    191  exhaustVAV  A device that regulates the volume of air bein...    onboard                                               None
      2    193         oil  A viscous liquid derived from petroleum, espec...      brick  https://brickschema.org/ontology/1.2/classes/Oil/
      3    114    fumeHood  A fume-collection device mounted over a work s...      brick  https://brickschema.org/ontology/1.1/classes/F...

   .. code-tab:: r R

      > api.get('tags') # official
      > get_tags()      # dev
      #     id    name        definition                                                     def_source  def_url                                                           category
      #1    120   battery     A container that stores chemical energy that can be con...     brick       https://brickschema.org/ontology/1.1/classes/Battery/             <NA>
      #2    191   exhaustVAV  A device that regulates the volume of air being exhaust...     onboard     <NA>                                                              <NA>
      #3    193   oil         A viscous liquid derived from petroleum, especially for...     brick       https://brickschema.org/ontology/1.2/classes/Oil/                 <NA>
      #4    114   fumeHood    A fume-collection device mounted over a work space, tab...     brick       https://brickschema.org/ontology/1.1/classes/Fume_Hood/           <NA>
      #5    118   limit       A parameter that places a lower or upper bound on the r...     brick       https://brickschema.org/ontology/1.1/classes/Limit/               Point Class
      #6    119   reset       Indicates a boolean point that reset a flag, property o...     brick       https://brickschema.org/ontology/1.1/classes/Reset_Command/       <NA>


This returns a dataframe containing definitions for all tags in our data model, with attribution where applicable.

Unit types
----------

.. tabs::
   .. code-tab:: py

      >>> # Get all unit types from the Data Model
      >>> unit_types = pd.DataFrame(client.get_all_units())
      >>> unit_types[['id', 'name_long', 'qudt']]
         id             name_long                                  qudt
      0  55                 Litre          http://qudt.org/vocab/unit/L
      1  68             US Gallon     http://qudt.org/vocab/unit/GAL_US
      2  75                   Bar        http://qudt.org/vocab/unit/BAR
      3  76                 Watts          http://qudt.org/vocab/unit/W

   .. code-tab:: r R

      > # Get all unit types from the Data Model
      > units <- api.get('unit') # official
      > units <- get_all_units() # dev
      > units %>% select(id, name_long, qudt)
      #  id name_long                              qudt
      #1 55     Litre      http://qudt.org/vocab/unit/L
      #2 68 US Gallon http://qudt.org/vocab/unit/GAL_US
      #3 75       Bar    http://qudt.org/vocab/unit/BAR
      #4 76     Watts      http://qudt.org/vocab/unit/W




Measurement types
-----------------

.. tabs::
   .. code-tab:: py
   
      >>> # Get all measurement types from the Data Model
      >>> measurement_types = pd.DataFrame(client.get_all_measurements())
      >>> measurement_types[['id', 'name', 'qudt_type']]
          id               name                                          qudt_type
      0   20     Reactive Power   http://qudt.org/vocab/quantitykind/ReactivePower
      1   27              Floor   http://qudt.org/vocab/quantitykind/Dimensionless
      2   33       Power Factor   http://qudt.org/vocab/quantitykind/Dimensionless
      3   31             Torque  http://qudt.org/vocab/quantitykind/Dimensionle...

   .. code-tab:: r R

      > # Get all measurement types from the Data Model
      > measurements <- api.get('measurements')   # official
      > measurements <- get_all_measurements()    # dev
      > measurements %>% select(id, name, qudt_type)
      #  id           name                                        qudt_type
      #1 31         Torque                                             <NA>
      #2 27          Floor http://qudt.org/vocab/quantitykind/Dimensionless
      #3 33   Power Factor http://qudt.org/vocab/quantitykind/Dimensionless
      #4 20 Reactive Power http://qudt.org/vocab/quantitykind/ReactivePower

