import django_tables2 as tables

from registration.models import IDPinGenerate


class IDPinGenerateTable(tables.Table):
    class Meta:
        model = IDPinGenerate
        fields = ("id", "id_pin", "share_no", "share_price", "created_user")

    def before_render(self, request):
        self.columns.hide('id')
