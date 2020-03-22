from datetime import datetime

import zope.interface


class IStorage(zope.interface.Interface):
    """ Base class for all the storage providers"""

    def upload(filename: str, data: bytes, client_modified: datetime) -> None:
        """
        Uploads a file to this storage provider
        :param filename: Name of the file
        :param data: File content
        :param client_modified: Last modified time of the file on the client
        :raises:
            UploadException: if the file upload fails
        """

    def listing() -> [(str, datetime)]:
        """
        Lists the files in this storage provider
        :return: List of filenames and client modified timestamps
        """

    def delete(filename: str) -> None:
        """
        Deletes a file from this storage provider
        :param filename: Name of the file
        :raises:
            IOException: if the file deletion fails
        """