
from pythonjsonlogger import jsonlogger
import logging, sys,os

logger_name = "ConnectGetFilterXML_S3"
logger = logging.getLogger(logger_name)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = jsonlogger.JsonFormatter(
'%(name)s - %(levelname)s - %(asctime)s - %(filename)s - %(lineno)d - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate=False
logger.setLevel(logging.INFO)
try:
    bucket_name:str          = "s3_bucket_name_with_out_s3//"
    prefix:str               = "/prefix/thatwanttolookin/"
    keys_list:list           =  ['keytosearch']
    file_list_to_search:list = ['filestosearchforifspecific']
    expected:int             = 1
    multithread:bool         = False
except Exception as e:
    logger.error("config failed exiting!")
    raise


