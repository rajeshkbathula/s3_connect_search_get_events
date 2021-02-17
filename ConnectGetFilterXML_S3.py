# Python3 Script will get files from  s3 and filters and gets the XML's  in specific prefix given
# Rajesh Bathula - 25-06-2020
# copy this module to your path where you want to run and cd module and run
# please make sure you provide right bucket name , prifix and transaction values
import concurrent.futures
import boto3
import re, os, shutil
from pathlib import Path
from config_input import *
import sys

class GetSearchFilter:
    # Class Variables please don't change
    dir = ['transaction', 'output','found']
    output_file = 'transaction.xml'

    def __init__(self,prefix,bucket_name,keys_list,expected,multithread,file_list_to_search):
        self.prefix:str                = prefix
        self.bucket_name:str           = bucket_name
        self.keys_list:list            = keys_list
        self.file_list_to_search:list  = file_list_to_search
        self.expected:int              = expected
        self.multithread:bool          = multithread
        self.key_id:str                   = input("Please enter AWS KEY_ID:\n")
        self.secret_key:str               = input("Please enter AWS SECRET_KEY:\n")
        self.token:str                     = input("Please enter AWS SESSION_TOKEN:\n")
        self.s3:str                        = self.aws_login()
        self.prod_tran_bucket:str          = self.s3.Bucket(bucket_name)

    def aws_login(self):
        try:
            s3 = boto3.resource('s3',
                            aws_access_key_id=self.key_id,
                            aws_secret_access_key=self.secret_key
                            ,aws_session_token=self.token
                            )
            return s3
        except Exception as E:
            logger.error(f"failed to login {E}, check your credentials")

    def get_files_s3(self,s3_key):
        s3_key = Path(s3_key)
        tail = str(os.path.split(s3_key)[1])
        # if int(tail) >= 1596138000000:
        s3_prefix = f'{self.prefix}{tail}'
        logger.info(f'downloading {self.prefix}{tail}')
        self.s3.Bucket(self.bucket_name).download_file(s3_prefix, tail)
        shutil.move(tail, f'{GetSearchFilter.dir[0]}/{tail}')
        self.search_file(tail)

    def main(self):
        if len(self.file_list_to_search) > 0:
            file_list = [f'{self.prefix}{s3_key}' for s3_key in file_list_to_search ]
        else:
            file_list = [s3_key.key for s3_key in self.prod_tran_bucket.objects.filter(Prefix=self.prefix)]
        logger.info(file_list)
        cnt = len(file_list)
        logger.info(f"{cnt} file to search!")
        [os.makedirs(d) for d in GetSearchFilter.dir if not os.path.exists(d)]
        logger.info("running!")
        if self.multithread:
            with concurrent.futures.ThreadPoolExecutor() as executer:
                results = executer.map(self.get_files_s3,file_list)

                for _ in results:
                    cnt -= 1
                    logger.info(f"Pending files: {cnt}")
        else:
            results = map(self.get_files_s3, file_list)
            for _ in results:
                cnt -= 1
                logger.info(f"Pending files: {cnt}")

    def search_file(self,file):
        with open(f'{GetSearchFilter.dir[0]}/{file}') as f:
            file_search = f.read()
            for num in self.keys_list:
                x = re.findall(num,file_search)
                if len(x) > 0:
                    shutil.move(f'{GetSearchFilter.dir[0]}/{file}', f'{GetSearchFilter.dir[2]}/{file}')
                    logger.info(f"Found file {file}")
                    self.get_lines(file)
            if os.path.exists(f'{GetSearchFilter.dir[0]}/{file}'):
                os.remove(f'{GetSearchFilter.dir[0]}/{file}')

    def get_lines(self,file_found):
        with open(f'{GetSearchFilter.dir[2]}/{file_found}') as f:
            this_line = f.readlines()
            lines_list = [str(line) for line in this_line for num in self.keys_list if re.search(num, line) != None]
            os.remove(f'{GetSearchFilter.dir[2]}/{file_found}')
            with open(f"{GetSearchFilter.dir[1]}/{GetSearchFilter.output_file}",'a') as f:
                for line in lines_list:
                    f.write(line)
                logger.info("found XML!")
                if self.expected == int(len(open(f'{GetSearchFilter.dir[1]}/{GetSearchFilter.output_file}').readlines())):
                    logger.info("Matched Search target xml count, exiting!")
                    shutil.rmtree(GetSearchFilter.dir[0])
                    shutil.rmtree(GetSearchFilter.dir[2])
                    sys.exit(0)

if __name__ == '__main__':
    logger.info(f"prefix: {prefix}, bucket_name: {bucket_name}, keys_list: {keys_list}, expected: {expected}, multithread: {multithread}, file_list_to_search: {file_list_to_search}")
    filter = GetSearchFilter(prefix, bucket_name, keys_list, expected, multithread,file_list_to_search)
    filter.main()
