from django import forms


class SearchUsersForm(forms.Form):
    query = forms.CharField(
        required=True,
        max_length=30,
        widget=forms.TextInput(
            attrs={'placeholder': 'Search for users by name'}
        )
    )
