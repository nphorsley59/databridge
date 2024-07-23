import boto3
from botocore.exceptions import ClientError
from pathlib import Path
from typing import Callable, Union

from databridge.storage._abstract import Storage


class S3Storage(Storage):
    def __init__(
        self, 
        bucket_name: str, 
        aws_access_key_id: str = None, 
        aws_secret_access_key: str = None, 
        region_name: str = None,
    ):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def _format_fpath(self, fpath: Union[Path, str]):
        if isinstance(fpath, Path):
            fpath = str(fpath)
        if not isinstance(fpath, str):
            raise TypeError("File path must be Path or str.")
        return fpath

    def _read(self, fpath: str, reader: Callable, **kwargs):
        reader = reader or self._get_reader_callable(fpath=fpath)
        obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=fpath)
        return reader(obj['Body'], **kwargs)

    def _write(self, obj, fpath: str, writer: Callable, **kwargs):
        writer = writer or self._get_writer_callable(fpath=fpath)
        body = writer(obj=obj, **kwargs)
        self.s3_client.put_object(Bucket=self.bucket_name, Key=fpath, Body=body)

    def exists(self, fpath):
        fpath = self._format_fpath(fpath=fpath)
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=fpath)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise
