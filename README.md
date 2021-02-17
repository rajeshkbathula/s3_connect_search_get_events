#  STEPS

* developed in a way that if you set multithreading to True in config , will be faster but also effects other programs in local.

1. > cd ./s3_connect_search_get_events

2. > python3 -m venv .venv 
3. > source ./.venv/bin/activate 
4. > pip install -r requirements.txt 
5. > input in config_input.py file inputs required
6. > pytest ./                
    * Tests still in progress 
7. > python3 ./ConnectGetFilterXML_S3.py
    * Kindly provide aws key,secret and token when prompted
* Matching XML's will be sent to output ./folder/transaction.xml

## Example Config Arguments 
```
    bucket_name:str          = 'some-bucket-name' -- s3 bucket name
    prefix:str               = 'data/2020-06-21/' -- prefix of s3 bucket
    keys_list:list         = ['11ES5NFYAV' ,'12END6ZNE1'] -- objects that you want to match
    file_list_to_search:list = [] -- this is optional pass file names if you know to search in ["1592734278698","1592737542752"]
    expected:int             = 2   -- number of records expecting once reached program will exit
    multithread:bool         = False   -- setting it to true will do multithreading

```