from rest_framework.serializers import ValidationError


class Validatorlink:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_link = dict(value).get(self.field)
        if not (tmp_link is None or "youtube.com" in tmp_link):
            raise ValidationError("Ссылка не разрешена.")
