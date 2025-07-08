from enum import Enum


class FlashMessage(Enum):
    LOGIN_FAILED = ("Email or password is incorrect", "danger")
    EDIT_SUCCESS = ("Task edited successfully", "success")
    EDIT_FAILED = ("Task edited failed", "danger")
    CREATE_FILE_SUCCESS = ("All files uploaded successfully", "success")
    CREATE_FILE_FAILED = ("Upload failed due to a database error", "danger")
    DELETE_FILE_SUCCESS = ("File has deleted successfully", "success")
    DOWNLOAD_FILE_FAILED = ("Download is failed.", "warning")

    def message(self):
        return self.value[0]

    def category(self):
        return self.value[1]
