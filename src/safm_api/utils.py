from django.utils.text import slugify


def get_safe_file_name(filename):
    '''
    Return a safe file name that has only ascii chars
    '''
    fpath = ''
    if '/' in filename:
        # file path is provided
        fpath, filename = filename.rsplit('/', 1)
        fpath += '/'

    # split filename into name and extension and slugify name
    filename_split = filename.rsplit('.', 1)
    extension = ''
    if len(filename_split) == 2:
        name, extension = filename_split
        extension = '.' + extension
    else:
        name = filename_split[0]

    return fpath + slugify(name) + extension
