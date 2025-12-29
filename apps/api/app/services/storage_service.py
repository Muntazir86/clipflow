"""Storage service for file management (local and S3)."""

import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO, Optional
from uuid import UUID

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from app.config import get_settings

settings = get_settings()


class StorageBackend(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    def save_file(self, file: BinaryIO, filename: str) -> str:
        """Save a file and return the storage path."""
        pass

    @abstractmethod
    def get_file(self, path: str) -> Optional[bytes]:
        """Get file contents by path."""
        pass

    @abstractmethod
    def delete_file(self, path: str) -> bool:
        """Delete a file by path."""
        pass

    @abstractmethod
    def file_exists(self, path: str) -> bool:
        """Check if a file exists."""
        pass

    @abstractmethod
    def get_presigned_upload_url(
        self, filename: str, content_type: str, expires_in: int = 3600
    ) -> Optional[str]:
        """Generate a presigned URL for direct upload."""
        pass

    @abstractmethod
    def get_presigned_download_url(self, path: str, expires_in: int = 3600) -> Optional[str]:
        """Generate a presigned URL for download."""
        pass


class LocalStorageBackend(StorageBackend):
    """Local filesystem storage backend."""

    def __init__(self, upload_dir: str):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_file(self, file: BinaryIO, filename: str) -> str:
        """Save a file to local storage."""
        file_path = self.upload_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file, f)
        return str(file_path)

    def get_file(self, path: str) -> Optional[bytes]:
        """Get file contents from local storage."""
        file_path = Path(path)
        
        # If path is not absolute, try relative to upload_dir
        if not file_path.is_absolute():
            file_path = self.upload_dir / path
        
        if file_path.exists():
            return file_path.read_bytes()
        return None

    def delete_file(self, path: str) -> bool:
        """Delete a file from local storage."""
        try:
            file_path = Path(path)
            
            # If path is not absolute, try relative to upload_dir
            if not file_path.is_absolute():
                file_path = self.upload_dir / path
            
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False

    def file_exists(self, path: str) -> bool:
        """Check if file exists in local storage."""
        file_path = Path(path)
        
        # If path is not absolute, try relative to upload_dir
        if not file_path.is_absolute():
            file_path = self.upload_dir / path
        
        return file_path.exists()

    def get_presigned_upload_url(
        self, filename: str, content_type: str, expires_in: int = 3600
    ) -> Optional[str]:
        """Local storage doesn't support presigned URLs."""
        return None

    def get_presigned_download_url(self, path: str, expires_in: int = 3600) -> Optional[str]:
        """Local storage doesn't support presigned URLs."""
        return None

    def get_file_path(self, filename: str) -> Path:
        """Get the full path for a file."""
        return self.upload_dir / filename


class S3StorageBackend(StorageBackend):
    """S3-compatible storage backend."""

    def __init__(
        self,
        bucket_name: str,
        access_key: str,
        secret_key: str,
        region: str,
        endpoint_url: Optional[str] = None,
    ):
        self.bucket_name = bucket_name
        self.client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
            endpoint_url=endpoint_url,
            config=Config(signature_version="s3v4"),
        )

    def save_file(self, file: BinaryIO, filename: str) -> str:
        """Save a file to S3."""
        try:
            self.client.upload_fileobj(file, self.bucket_name, filename)
            return f"s3://{self.bucket_name}/{filename}"
        except ClientError as e:
            raise Exception(f"Failed to upload to S3: {e}")

    def get_file(self, path: str) -> Optional[bytes]:
        """Get file contents from S3."""
        try:
            # Extract key from path
            key = path.replace(f"s3://{self.bucket_name}/", "")
            response = self.client.get_object(Bucket=self.bucket_name, Key=key)
            return response["Body"].read()
        except ClientError:
            return None

    def delete_file(self, path: str) -> bool:
        """Delete a file from S3."""
        try:
            key = path.replace(f"s3://{self.bucket_name}/", "")
            self.client.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError:
            return False

    def file_exists(self, path: str) -> bool:
        """Check if file exists in S3."""
        try:
            key = path.replace(f"s3://{self.bucket_name}/", "")
            self.client.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError:
            return False

    def get_presigned_upload_url(
        self, filename: str, content_type: str, expires_in: int = 3600
    ) -> Optional[str]:
        """Generate a presigned URL for direct upload to S3."""
        try:
            url = self.client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": filename,
                    "ContentType": content_type,
                },
                ExpiresIn=expires_in,
            )
            return url
        except ClientError:
            return None

    def get_presigned_download_url(self, path: str, expires_in: int = 3600) -> Optional[str]:
        """Generate a presigned URL for download from S3."""
        try:
            key = path.replace(f"s3://{self.bucket_name}/", "")
            url = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": key},
                ExpiresIn=expires_in,
            )
            return url
        except ClientError:
            return None


class StorageService:
    """Storage service that abstracts storage backend."""

    def __init__(self):
        if settings.storage_type == "s3":
            self.backend = S3StorageBackend(
                bucket_name=settings.s3_bucket_name,
                access_key=settings.s3_access_key,
                secret_key=settings.s3_secret_key,
                region=settings.s3_region,
                endpoint_url=settings.s3_endpoint_url,
            )
        else:
            self.backend = LocalStorageBackend(settings.upload_dir)

    def save_file(self, file: BinaryIO, filename: str) -> str:
        """Save a file."""
        return self.backend.save_file(file, filename)

    def get_file(self, path: str) -> Optional[bytes]:
        """Get file contents."""
        return self.backend.get_file(path)

    def delete_file(self, path: str) -> bool:
        """Delete a file."""
        return self.backend.delete_file(path)

    def file_exists(self, path: str) -> bool:
        """Check if file exists."""
        return self.backend.file_exists(path)

    def get_presigned_upload_url(
        self, filename: str, content_type: str, expires_in: int = 3600
    ) -> Optional[str]:
        """Get presigned upload URL."""
        return self.backend.get_presigned_upload_url(filename, content_type, expires_in)

    def get_presigned_download_url(self, path: str, expires_in: int = 3600) -> Optional[str]:
        """Get presigned download URL."""
        return self.backend.get_presigned_download_url(path, expires_in)

    def get_local_path(self, filename: str) -> Optional[Path]:
        """Get local file path (only for local storage)."""
        if isinstance(self.backend, LocalStorageBackend):
            return self.backend.get_file_path(filename)
        return None


def get_storage_service() -> StorageService:
    """Get storage service instance."""
    return StorageService()
