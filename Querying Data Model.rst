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
      >>> equip_type[["id", "tag_name", "name_long"]]
         id          tag_name         name_long
      0  70    ELECTRICAL/ATS    ELECTRICAL/ATS
      1  71   ELECTRICAL/BATT   ELECTRICAL/BATT
      2  72     ELECTRICAL/CB     ELECTRICAL/CB
      3  73    ELECTRICAL/GEN    ELECTRICAL/GEN
      4  74  ELECTRICAL/PANEL  ELECTRICAL/PANEL

   .. code-tab:: r R

      library(OnboardClient)
      library(tidyverse)
      api.setup()
      get_equip_types() %>% select(id, tag_name, name_long)
        id  tag_name name_long
      1 12  HVAC/AHU  HVAC/AHU
      6 19  HVAC/BLR  HVAC/BLR

Note that not all equipment types have associated sub-types.

Point types
-----------

Accessing point types is very similar:

.. tabs::
   .. code-tab:: py

      >>> # Get all point types from the Data Model
      >>> point_types = pd.DataFrame(client.get_all_point_types())
              id                      tag_name                     tags
      0      868             ac_voltage_sensor           [sensor, volt]
      1      869           air_pressure_sensor  [pressure, sensor, air]
      2      870           air_pressure_status          [pressure, air]
      3      871  ammonia_leak_detection_alarm    [alarm, leakDetector]
      4      872   apparent_energy_accumulator       [energy, apparent]

   .. code-tab:: r R

      point_types <- get_point_types()
      point_types %>% select(id, point_type, tags) %>% distinct()
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
            id                  name                                         definition def_source def_url category
      0    499          cogeneration            Associated with a cogeneration process.        dbo    None     None
      1    500      dehumidification             Process of removing moisture from air.        dbo    None     None
      2    405       ELECTRICAL/TXMR  Tag for transformers, which are devices that t...        dbo    None     None
      3    406        ELECTRICAL/UPS  Tag for all uninterruptible power supply (UPS)...        dbo    None     None
      4    407  GATEWAYS/PASSTHROUGH  A device that provides translations for virtua...        dbo    None     None

   .. code-tab:: r R

      api.get('tags') # official
      get_tags()      # dev
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
      >>> unit_types[['id', 'name_long', 'qudt']].sample(5)
            id                  name_long                                        qudt
      29    88  Kilo British Thermal Unit       http://qudt.org/vocab/unit/KiloBTU_IT
      21   103              Square Meters               http://qudt.org/vocab/unit/M2
      114    7      Cubic Feet Per Minute      http://qudt.org/vocab/unit/FT3-PER-MIN
      15    98             Milligravities           http://qudt.org/vocab/unit/MilliG
      33    78             Megawatt Hours         http://qudt.org/vocab/unit/MegaW-HR

   .. code-tab:: r R

      # Get all unit types from the Data Model
      units <- api.get('unit') # official
      units <- get_all_units() # dev
      units %>% select(id, name_long, qudt)
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
          id                name                                          qudt_type
      0   26         Multi-State                                               None
      1   33         powerfactor   http://qudt.org/vocab/quantitykind/Dimensionless
      2   17  rotationalvelocity  http://qudt.org/vocab/quantitykind/AngularVelo...
      3   28             current  http://qudt.org/vocab/quantitykind/ElectricCur...
      4   14              energy          http://qudt.org/vocab/quantitykind/Energy


   .. code-tab:: r R

      # Get all measurement types from the Data Model
      measurements <- api.get('measurements')   # official
      measurements <- get_all_measurements()    # dev
      measurements %>% select(id, name, qudt_type)
      #  id           name                                        qudt_type
      #1 31         Torque                                             <NA>
      #2 27          Floor http://qudt.org/vocab/quantitykind/Dimensionless
      #3 33   Power Factor http://qudt.org/vocab/quantitykind/Dimensionless
      #4 20 Reactive Power http://qudt.org/vocab/quantitykind/ReactivePower

