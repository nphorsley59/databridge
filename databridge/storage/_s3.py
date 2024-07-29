import boto3
from botocore.exceptions import ClientError
import io
from typing import Callable

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
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
            endpoint_url=endpoint_url,
        )

    def _read(
        self,
        fpath: str,
        reader: Callable = None,
        **kwargs,
    ):
        reader = reader or self._get_reader_callable(fpath=fpath)
        obj = self.s3_client.get_object(
            Bucket=self.bucket_name,
            Key=fpath,
            **kwargs,
        )
        body = obj["Body"]
        buffer = io.StringIO(body.read().decode("utf-8"))
        return reader(buffer, **kwargs)

    def _write(
        self,
        obj,
        fpath: str,
        writer: Callable = None,
        **kwargs,
    ):
        writer = writer or self._get_writer_callable(fpath=fpath)
        buffer = io.StringIO()
        writer(obj=obj, fpath=buffer, **kwargs)
        buffer.seek(0)
        body = buffer.getvalue().encode("utf-8")
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=fpath,
            Body=body,
            **kwargs,
        )

    def exists(self, fpath):
        fpath = self._format_fpath(fpath=fpath)
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=fpath)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                raise e

    def delete(self, fpath):
        fpath = self._format_fpath(fpath=fpath)
        if not self.exists(fpath=fpath):
            raise FileNotFoundError(f"No such file: '{fpath}'")
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=fpath)
