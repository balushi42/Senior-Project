from rest_framework.exceptions import APIException

class LargeFileSize(APIException):
    status_code = 400
    default_detail = "Unable to upload file, too large!"
    default_code = "large_file_size"

class InvalidFileFormat(APIException):
    status_code = 400
    default_detail = "Unable to upload file, unknown file format!"
    default_code = "invalid_file_format"