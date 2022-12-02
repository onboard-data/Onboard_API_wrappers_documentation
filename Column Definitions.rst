Columns for Data Model
======================

.. _dm-reference-label:

Equipment types
---------------
Accessed with 

.. tabs::
  .. code-tab:: py
    
    pd.json_normalize(client.get_equipment_types())

  .. code-tab:: r R

    get_equipment_types()


**id**: unique integer associated with the given type/tag

**tag_name**: this is the equip type tag associated with a class

**name_long**: longer, human-readable name (e.g. tag "cogen" => "Cogeneration Plant"). This is the class name you will find in the ontology

**name_abbr**: common abbreviated form (e.g. "FCU", "CHWS")

**active**: True if this class in the latest version of the ontology

**critical_point_types**: id numbers of the associated point types that are expected to be observed (look up in client.get_all_point_types())

**sub_types**: embedded JSON of possible forms of the equipment super-type (e.g. 'fan' has the sub-types 'exhaustFan', 'reliefFan', 'returnFan', etc.)

**tags**: Haystack tags associated with equipment super-type


Sub-equipment types
-------------------
Accessed for given equipment (e.g. 'fan') with 

.. tabs::
  .. code-tab:: py
    
    sub_type = pd.DataFrame(equip_type[equip_type.tag_name == 'fan']['sub_types'].item())

  .. code-tab:: r R

    get_equipment_types()

**id**: unique integer associated with the given type/tag

**equipment_type_id**: id of the associated equipment tag in client.get_equipment_types()

**tag_name**: this is the sub-equip type tag associated with a class

**name_long**: longer, human-readable name. This is the class name you will find in the ontology.

**name_abbr**: common abbreviated form


.. _point types:

Point types
-----------
Accessed with 

.. tabs::
  .. code-tab:: py
  
    client.get_all_point_types()

  .. code-tab:: r R

    get_point_types()

**id**: unique integer associated with the given type/tag

**tag_name**: human-readable name. This is the class name you will find in the ontology.

**active**: True if this class in the latest version of the ontology

**measurement_id**: id of the associated measurement type accessed as documented below

**tags**:  Haystack tags associated with point type


.. _unit types:

Unit types
----------
Accessed with 

.. tabs::
  .. code-tab:: py
    
    pd.DataFrame(client.get_all_units())

  .. code-tab:: r R

    api.get('unit') # official
    get_all_units() # dev

**id**: unique integer associated with the given type/tag

**name_long**: human-readable unit name (e.g. 'Cubic Meter per Hour')

**name_abbr**: abbreviated form (e.g. 'm3/h')

**data_type**: form of associated data. Can be 'Binary', 'Continuous', 'Enum', 'None', or 'Ordinal'

**raw_encoding**: for Binary and Enum data types, contains dictionary matching number to interpretation.

**display_encoding**: for Binary and Enum data types, contains dictionary showing how each reported number will be displayed. E.g., a 0 from an Occupancy sensor will be reported as 'Unoccupied'.

**qudt**:  url for additional information about unit (e.g. 'Degrees Celsius') on qudt.org

**unit_type**: url for additional information about measurement type (e.g. 'Temperature') on qudt.org

.. _measurement types:

Measurement types
-----------------
Accessed with

.. tabs::
  .. code-tab:: py

    pd.DataFrame(client.get_all_measurements())

  .. code-tab:: r R

    api.get('measurements') # official
    get_all_measurements    # dev

**id**: unique integer associated with the given measurement types

**name**: name of measurement type

**default_unit_id**: id of default associated unit type in client.get_all_units(). Note, pandas will cast this column as a float, but it can still be used to look up id

**units_convertible**: True if units of this measurement type can be interchangeably converted (generally True for continuous measurement types)

**units**: embedded JSON of possible units for given measurement type

**qudt_type**: url for additional information about measurement type (e.g. 'Temperature') on qudt.org


Tag metadata
------------
Accessed with 


.. tabs::
  .. code-tab:: py

    pd.DataFrame(client.get_tags())
  
  .. code-tab:: r R

    api.get('tags') # official
    get_tags()      # dev
  

**id**: unique integer associated with the given tag metadata

**name**: name of tag being described

**definition**: definition of tag

**def_source**: source of definition (either brick, haystack, or onboard)

**def_url**: url for source of definition (brick and haystack only)

**category**: category used to help sort point types in the ontology (see data model page). Can be 'Medium', 'Medium Property', 'Point Class', 'Quantity Modifier', or  None


.. _bsp-reference-label:

Columns for Data Extracted from Buildings
=========================================

Building-Specific Equipment
---------------------------

**id**: unique integer associated with the given equipment in this building. Will be unique across all equipment in platform.

**building_id**: unique integer associated with the building. Will be unique across all buildings in platform.

**equip_id**: Name to identify individual equipment instances. Constructed as equipment name + identifying suffix

**suffix**: Just the identifying suffix part of the equip_id

**equip_type_name**: Relevant name in the ontology

**equip_type_id**: integer id of relevant equipment type

**equip_type_abbr**: abbreviation of relevant equipment type

**equip_type_tag**: tag name of relevant equipment type

**equip_subtype_name**: name of relevant equipment sub-type

**equip_subtype_id**: integer id of relevant equipment sub-type

**equip_subtype_tag**:  tag name of relevant equipment sub-type

**floor_num_physical**: 4-digit code (see below) for floor where equipment is located. Can be integer or NaN if not available

  1000: basement

  1001: rooftop

  1002: outside

  1003: whole_buildings

  1004: ground_floor

  1005: penthouse

**floor_num_served**: 4-digit code for floor that equipment serves. Can be integer or NaN if not available

**area_served_desc**: Description of area that equipment serves

**equip_dis**: plain-text description of equipment from building documentation

**parent_equip**: integer id that links to parent equipment row(s)

**child_equip**: integer id that links to child equipment row(s)

**points**: embedded JSON containing associated points

**tags**: Haystack tags associated with equipment


Building-Specific Points
------------------------

**id**: unique integer associated with the given point in this building. Will be unique across all points in platform.

**building_id**: unique integer associated with the building. Will be unique across all buildings in platform.

**last_updated**: Unix-formatted timestamp of most recent value reported from point

**first_updated**: Unix-formatted timestamp of earliest value reported from point

**name**: raw sensor metadata (from BACnet scan)

**description**: alternate location for raw sensor metadata (from BACnet scan)

**units**: Matches to unit abbreviation in units table

**raw_unit_id**: unit id as it appears when accessing :ref:`unit types<unit types>`

**value**: Most recent reported value for point (from BACnet scan)

**type**: name of point type in the ontology

**point_type_id**: point type name as it appears when accessing :ref:`point types<point types>`

**measurement_id**: measurement type id as it appears when accessing :ref:`measurement types<measurement types>`

**state_text**: mapping between each state and text description of state

**equip_id**: unique integer associated with the associated equipment


Site-Level Data
---------------

Accessed with 

.. tabs::
  .. code-tab:: py
  
    client.get_all_buildings()

  .. code-tab:: r R

    get_buildings()

**id**: Unique ID generated for a new site (primary key for the Site Table)

**name**: Site name

**sq_ft**: Total square-footage of the site address

**equip_count**: Number of equipment instances associated with the building

**point_count**: Number of points associated with the building

**info.org**: Site's main ownership organization

**info.floors**: Number of floors associated with the site's square footage

**info.m2fend**: Site scheduled weekday closing time

**info.satend**: Site scheduled Saturday closing time

**info.sunend**: Site scheduled Sunday closing time

**info.geoCity**: Name of the city where the site is located

**info.geoState**: Name of the state where the site is located (e.g. New York)

**info.m2fstart**: Site scheduled weekday opening time

**info.satstart**: Site scheduled Saturday opening time

**info.sunstart**: Site scheduled Sunday opening time

**info.geoCountry**: Name of the country where the site is located

**info.weatherRef**: The source of weather data
