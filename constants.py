DATABASE_LOCATION = 'covid/data_files/bplus/'
DATABASE_NAME = DATABASE_LOCATION + 'my_bplus_db'
KEY_SIZE = 8
FIELD_SIZE = 10 # fields are double so size needs to be 8-10 bytes
FIELD_NUM = 7  #COVID: ['day', 'month', 'year', 'cases', 'deaths', 'countryterritoryCode', 'popData2018']
FIELD_TYPES = ['string']
RECORD_SIZE = KEY_SIZE + FIELD_NUM * FIELD_SIZE
ALL_FIELDS_SIZE = RECORD_SIZE - KEY_SIZE  # size of the all fields except for key
FIELD_TYPE = FIELD_TYPES[0].strip()

def read_from_file(file_path):
    input_file = open(file_path, 'r+')
    global DATABASE_LOCATION, DATABASE_NAME, KEY_SIZE, FIELD_SIZE, FIELD_NUM, RECORD_SIZE, ALL_FIELDS_SIZE, FIELD_TYPES
    DATABASE_LOCATION = str(input_file.readline()).rstrip() + 'bplus/'
    DATABASE_NAME = DATABASE_LOCATION + str(input_file.readline()).rstrip()
    KEY_SIZE = int(input_file.readline())
    FIELD_SIZE = int(input_file.readline())
    FIELD_NUM = int(input_file.readline())
    FIELD_TYPES = input_file.readline().split()
    RECORD_SIZE = KEY_SIZE + FIELD_NUM * FIELD_SIZE
    ALL_FIELDS_SIZE = RECORD_SIZE - KEY_SIZE  # size of the all fields except for key
    FIELD_TYPE = FIELD_TYPES[0].strip()
    input_file.close()
