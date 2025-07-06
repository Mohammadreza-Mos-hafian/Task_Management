from enum import Enum


class FlashMessage(Enum):
    LOGIN_FAILED = ("Email or password is incorrect", "danger")
    EDIT_SUCCESS = ("Task edited successfully", "success")
    EDIT_FAILED = ("Task edited failed", "danger")

    def message(self):
        return self.value[0]

    def category(self):
        return self.value[1]
