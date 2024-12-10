from cbr_custom_data_feeds.data_feeds.Data_Feeds__Http_Content  import Data_Feeds__Http_Content
from cbr_custom_data_feeds.data_feeds.Data_Feeds__S3_DB         import Data_Feeds__S3_DB
from osbot_utils.base_classes.Type_Safe                         import Type_Safe

class Data_Feeds__Files(Type_Safe):
    s3_db       : Data_Feeds__S3_DB
    http_content: Data_Feeds__Http_Content

    def all_files(self):
        return self.s3_db.provider__all_files()