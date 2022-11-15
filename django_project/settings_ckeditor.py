CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',
        'toolbar_itpolygon': [
            {'name': 'document', 'items': [
                'Source', 'Preview', 'CodeSnippet', ]},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', 'Blockquote', 'CreateDiv',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
            {'name': 'links', 'items': ['Link', 'Unlink']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'InsertSnippet', 'Table', 'HorizontalRule', 'SpecialChar']},

            {'name': 'styles', 'items': [
                'Styles', 'Format', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': [
                'Preview', 'Maximize', 'ShowBlocks', 'codesnippet']},
        ],
        'toolbar': 'itpolygon',  # put selected toolbar config here
        'height': 300,
        'width': '100%',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'codesnippet',
            'uploadimage',
            'autolink',
        ]),
    },
    

}
