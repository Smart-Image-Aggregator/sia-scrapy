import zope.interface
import dropbox
from datetime import datetime

from sia_scrapy.storage.istorage import IStorage


# TODO Wrap into custom exceptions e.g. UploadError
@zope.interface.implementer(IStorage)
class Dropbox:

    def __init__(self, token: str, base_path: str):
        self.base_path = base_path
        assert base_path[-1] == '/'  # base path has to end in a slash
        self.dbx = dropbox.Dropbox(token)

    def upload(self, filename: str, data: bytes, client_modified: datetime) -> None:
        self.dbx.files_upload(data, self.base_path + filename, client_modified=client_modified)

    def listing(self) -> [(str, datetime)]:
        entries = []
        folder = self.dbx.files_list_folder(self.base_path)
        while True:
            entries += ((e.name, e.client_modified) for e in folder.entries)
            if folder.has_more:
                folder = self.dbx.files_list_folder_continue(folder.cursor)
            else:
                return entries

    def delete(self, filename: str) -> None:
        self.dbx.files_delete_v2(self.base_path + filename)
