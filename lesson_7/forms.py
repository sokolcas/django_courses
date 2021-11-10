from django import forms
# так подключаем внешний, не стандартный виджет
from durationwidget.widgets import TimeDurationWidget

from lesson_5.models import Client


class MyForm(forms.Form):
    # label - то, как будет отображаться на странице
    name = forms.CharField(label="User name", initial="User name",
                           error_messages={'required': 'Please enter your'
                                                       ' true name'})
    # виджет нужен, чтобы изменить стиль поля
    profile_picture = forms.ImageField(widget=forms.FileInput)
    additional_file = forms.FileField(widget=forms.FileInput)
    email = forms.EmailField(initial="admin@admin.com", error_messages={
        'required': 'Please enter your available email'})
    # required - обязательное ли поле
    password = forms.CharField(max_length=20, min_length=10,
                               required=True,
                               widget=forms.PasswordInput())
    age = forms.IntegerField(required=False, initial="45",
                             help_text="Enter your current age")
    agreement = forms.BooleanField(required=True)
    average_score = forms.FloatField(initial=10.1)
    birthday = forms.DateField(widget=forms.SelectDateWidget,
                               required=False)
    # отключили дни, чтобы не отображались. Остальные поля остались
    work_experience = forms.DurationField(required=False,
                                          widget=TimeDurationWidget(
                                              show_days=False))
    # описываем выбор, который предстоит сделать пользователю 
    # 1,2 - номера элементов. Не отображаются
    gender = forms.ChoiceField(required=False,
                               choices=[("1", "man"), ("2", "woman")])


# класс формы наследуется от класса дающего возможность
# превращать модели в формы. 
class FormFromModel(forms.ModelForm):
    class Meta:
        model = Client
        # указываются поля, которые учитываем
        fields = '__all__'
