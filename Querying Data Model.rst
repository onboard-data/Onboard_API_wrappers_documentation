Querying Data Model
===================

Onboard's data model contains both equipment types (e.g. fans, air handling units) and point types (e.g. zone temperature). We can query the full data model within our API.

Data model column definitions for each of the below tables can be found in :ref:`data model columns page<dm-reference-label>`.

Equipment types
---------------

First, we 
make an API call with :code:`client.get_equipment_types()`. This returns a JSON object, which we will convert to a dataframe using Pandas:


.. tabs::
   .. code-tab:: py

      >>> from onboard.client import OnboardClient
      >>> client = OnboardClient(api_key='')
      >>> import pandas as pd
      >>> # Get all equipment types from the Data Model
      >>> equip_type = pd.json_normalize(client.get_equipment_types())
      >>> equip_type.columns
      ['id', 'tag_name', 'name_long', 'name_abbr', 'active', 'flow_order',
      'critical_point_types', 'sub_types', 'tags']

   .. code-tab:: r R

      > library(OnboardClient)
      > library(tidyverse)
      > api.setup()
      > equip_type <- get_equip_types() 
      > equip_type


.. tabs::
    .. group-tab:: Python
        .. image:: images/py_equip_types_df.png

    .. group-tab:: R
        .. image:: images/r_equip_types_df.png



.. > equip_type %>% names()
.. [1] "id"                "tag_name"          "name_long"         "name_abbr"         "tags"              "id_subtype"       
.. [7] "tag_name_subtype"  "name_long_subtype" "name_abbr_subtype"




:code:`equip_type` now contains a dataframe listing all equipment types in our data model, along with associated attributes (e.g. tags, full names, associated point types, and sub-equipment types).


In the Python client, the sub-equipment types are nested as dataframes within each row, and can be listed for an equipment type (e.g. 'fan') like so:

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

Accessing point types is very similar, and can be accessed through client.get_all_point_types():

   >>> # Get all point types from the Data Model
   >>> point_type = pd.DataFrame(client.get_all_point_types())
   >>> point_type[['id', 'tag_name', 'tags']]
         id                                  tag_name                                            tags
   0    124                 Occupied Heating Setpoint             [air, sp, temp, zone, heating, occ]
   1    118                Outside Air Carbon Dioxide                     [air, co2, sensor, outside]
   2    130           Return Air Temperature Setpoint                         [air, sp, temp, return]
   3     84  Dual-Temp Coil Discharge Air Temperature  [air, discharge, dualTemp, sensor, temp, coil]
   ...

point_type now contains a dataframe listing all the tags associated with each point type.

We can extract the metadata associated with each tag in our data model like so:

   >>> # Get all tags and their definitions from the Data Model
   >>> pd.DataFrame(client.get_tags())
         id        name                                         definition def_source                                            def_url
   0    120     battery  A container that stores chemical energy that c...      brick  https://brickschema.org/ontology/1.1/classes/B...
   1    191  exhaustVAV  A device that regulates the volume of air bein...    onboard                                               None
   2    193         oil  A viscous liquid derived from petroleum, espec...      brick  https://brickschema.org/ontology/1.2/classes/Oil/
   3    114    fumeHood  A fume-collection device mounted over a work s...      brick  https://brickschema.org/ontology/1.1/classes/F...
   ...

This returns a dataframe containing definitions for all tags in our data model, with attribution where applicable.

Unit types
----------

   >>> # Get all unit types from the Data Model
   >>> unit_types = pd.DataFrame(client.get_all_units())
   >>> unit_types[['id', 'name_long', 'qudt']]
      id             name_long                                  qudt
   0  55                 Litre          http://qudt.org/vocab/unit/L
   1  68             US Gallon     http://qudt.org/vocab/unit/GAL_US
   2  75                   Bar        http://qudt.org/vocab/unit/BAR
   3  76                 Watts          http://qudt.org/vocab/unit/W
   ...

Measurement types
-----------------

   >>> # Get all measurement types from the Data Model
   >>> measurement_types = pd.DataFrame(client.get_all_measurements())
   >>> measurement_types[['id', 'name', 'qudt_type']]
       id               name                                          qudt_type
   0   20     Reactive Power   http://qudt.org/vocab/quantitykind/ReactivePower
   1   27              Floor   http://qudt.org/vocab/quantitykind/Dimensionless
   2   33       Power Factor   http://qudt.org/vocab/quantitykind/Dimensionless
   3   31             Torque  http://qudt.org/vocab/quantitykind/Dimensionle...
   ...
