import datetime
import os
def get_attachment_path(request, filename):
    original_filename = filename
    nowTime = datetime.now().strftime('%Y_%m_%d_%H:%M:%S_')
    filename = "%s%s%s" % ('RentRite_', nowTime, original_filename)
    return os.path.join('message/attachments/', filename)