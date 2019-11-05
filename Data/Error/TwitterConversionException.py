import time

_SLEEP_TIME = 0.1


class TwitterConversionException:
    def __init__(self, data, obj):
        self.data = data
        self.obj_name = type(obj).__name__

    def error_handling(self):
        if self.data['limit'] is not None:
            print('Sleeping...')
            time.sleep(_SLEEP_TIME)
        else:
            print('Undefined error!')
            print(self.data)
