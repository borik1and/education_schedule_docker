import re
from rest_framework.serializers import ValidationError

# class UrlValidator:
#     def __init__(self, field):
#         self.field = field
#
#     def __call__(self, value):
#         if value is None:
#             return
#         pattern = re.compile(r'^(https?://)?(www\.)?youtube\.com(/.*)?$')
#         tmp_vul = dict(value).get(self.field)
#         if not bool(pattern.match(tmp_vul)):
#             raise ValidationError('Недопустимый URL')


import re
from rest_framework import serializers


class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value:
            pattern = re.compile(r'^(https?://)?(www\.)?youtube\.com(/.*)?$')
            if not pattern.match(value):
                raise serializers.ValidationError('Недопустимый URL')
