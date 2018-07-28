Library outline 

move bucketing loginc into order book frame

what will be passed through the constructor? 
<constructor injection>

What will happen to the TimeSeriesRepository?
This will have a single responsibility of taking in the path to the 
csv file and returning a raw data frame

Move following methods from TimeSeriesRepository into
OrderBookFrame:
_convert_datetime_to_seconds
_create_file_name
_filter_data_matrix
_create_time_bucket_structure

at present I inject time_structure object into _create_time_bucket_structure

TimeStructure: Is there a need for this
	__init__
	create_time_structure
	create_time_series

order book frame will have a 2 dimensional index, first value will be
the start time and second value will be the end time
