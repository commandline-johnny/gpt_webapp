from django import forms


class ConversationForm(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea, label='Your prompt')


class ApiKeyForm(forms.Form):
    api_key = forms.CharField(widget=forms.PasswordInput, label='OpenAI API Key', max_length=100)


class GPTModelForm(forms.Form):
    def __init__(self, *args, **kwargs):
        available_models = kwargs.pop('available_models', [])
        super(GPTModelForm, self).__init__(*args, **kwargs)

        # Dynamically populate the model choices based on the available GPT models
        self.fields['model'] = forms.ChoiceField(
            choices=[(model, model) for model in available_models],
            label='Choose GPT Model'
        )