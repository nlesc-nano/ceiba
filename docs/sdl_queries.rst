Schema Queries
##############

The following schema defines the available queries:
::

    """Possible job status"""
    enum Status{
      AVAILABLE
      DONE
      FAILED
      RUNNING
      RESERVED
    }

    """Job computed by an user"""
    type Job {
      """Unique identifier"""
      _id: Int
      """compute Properties"""
      property: Property!
      """Input to perform the computation"""
      settings: String!
      """Job status"""
      status: Status!
      """User who es executing the job."""
      user: String
      """Timestamp=datatime.timestamp() """
      schedule_time: Float
      """Timestamp=datatime.timestamp()"""
      report_time: Float
      """platform where the job was run: platform.platform()"""
      platform: String
    }

    type Property {
      """Unique identifier"""
      _id: Int
      """Name to which the property belongs. e.g. Theory level"""
      collection_name: String!
      """Smile representing the molecule"""
      smile: String!
      """Optimize geometry"""
      geometry: String
      """Properties values as JSON"""
      data: String
      """Input with which the property was computed encoded as JSON"""
      input: String
      }

    type Query {
      """Query jobs by status and maximum number of jobs to retrieve"""
      jobs(status: Status!, collection_name: String!, max_jobs: Int!) : [Job!]
      properties(collection_name: String!): [Property!]
       property(smile: String!, collection_name: String!): Property
    }
