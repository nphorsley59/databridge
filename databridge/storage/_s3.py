import boto3
from botocore.exceptions import ClientError
import io

import pandas as pd

from databridge.storage._abstract import Storage


class S3Storage(Storage):
    def __init__(
        self, 
        bucket_name: str, 
        aws_access_key_id: str = None, 
        aws_secret_access_key: str = None, 
        region_name: str = None,
        endpoint_url: str = None,
    ):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
            endpoint_url=endpoint_url,
        )

    def _read(
        self, 
        fpath: str, 
        **kwargs,
    ):
        reader = self.s3_client.get_object
        obj = reader(Bucket=self.bucket_name, Key=fpath, **kwargs)['Body']
        buffer = io.StringIO(obj.read().decode('utf-8'))
        return pd.read_csv(buffer, **kwargs)

    def _write(
        self, 
        obj, 
        fpath: str, 
        **kwargs,
    ):
        writer = self.s3_client.put_object
        buffer = io.StringIO()
        obj.to_csv(buffer, index=False)
        buffer.seek(0)
        writer(Bucket=self.bucket_name, Key=fpath, Body=buffer.getvalue().encode("utf-8"), **kwargs)

    def exists(self, fpath):
        fpath = self._format_fpath(fpath=fpath)
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=fpath)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise e

    def delete(self, fpath):
        fpath = self._format_fpath(fpath=fpath)
        if not self.exists(fpath=fpath):
            raise FileNotFoundError(f"No such file: '{fpath}'")
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=fpath)
