from django import forms


class DynamicChoiceField(forms.ChoiceField):
    def validate(self, value):
        pass
