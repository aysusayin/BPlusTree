DATABASE_LOCATION = 'iot_data/data_files/bplus/'
DATABASE_NAME = DATABASE_LOCATION + 'my_bplus_db'
KEY_SIZE = 8
FIELD_SIZE = 10 # fields are double so size needs to be 8-10 bytes
FIELD_NUM = 7  #COVID: ['day', 'month', 'year', 'cases', 'deaths', 'countryterritoryCode', 'popData2018']
RECORD_SIZE = KEY_SIZE + FIELD_NUM * FIELD_SIZE
ALL_FIELDS_SIZE = RECORD_SIZE - KEY_SIZE  # size of the all fields except for key