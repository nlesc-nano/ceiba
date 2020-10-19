Data Layout
###########
The data layouts specifies how is the data and its metadata store in the database.
Since we use `Mongodb <https://www.mongodb.com/>`_  for the database, we will
also explain the data layout using Mongobd's terminology.


Properties collections
**********************
The following schema defines how the properties are stored:
::

  # Unique identifier
  _id: Integer
  # Name to which the property belongs. e.g. Theory level
  collection_name: String

  #Smile representing the molecule
  smile: String

  # Optimize geometry
  geometry: Optional[String]

  # Properties values as JSON
  data: Optional[String]

  # Input with which the property was computed encoded as JSON
  input: Optional[String]

Notice that the previous schema mirros the
`GraphQL definition of Property in the server <https://github.com/nlesc-nano/insilico-server/blob/master/insilicoserver/sdl/Query.graphql>`_.


Jobs collections
****************
The following schema defines how jobs are defined:
::
   
  # Unique identifier
  id: Integer

  # compute Properties
  property: Ref[Property]
  
  # Input to perform the computation
  settings: String

  # Job status
  status: Status

  # User who es executing the job
  user: Optional[String]

  # Timestamp = datatime.timestamp()
  schedule_time: Optional[Float]

  # Timestamp = datatime.timestamp()
  completion_time: Optional[Float]

  # platform where the job was run: platform.platform()
  platform: Optional[String]
   

Notice that the previous schema mirros the
`GraphQL definition of Job in the server <https://github.com/nlesc-nano/insilico-server/blob/master/insilicoserver/sdl/Query.graphql>`_.


.. Note::
   * `Optional[T] <https://docs.python.org/3/library/typing.html#typing.Optional>`_  is a type that could be either ``None`` or some ``T``.
   * References ``ref`` are implemented as `Mongodb DBRefs <https://docs.python.org/3/library/typing.html#typing.Optional>`_.
   * Jobs are stored in a collections named like ``jobs_<property_collection_name>``.
