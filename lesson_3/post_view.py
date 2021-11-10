from django.http import HttpResponse
from django.views.generic import TemplateView
from django.template import loader


class MyTemplateView(TemplateView):
    template_name = "post_page.html"

    def get_context_data(self, **kwargs):
        return {"latest_question_list": [
            {'id': 2,
             'question_text': 'Что первично, дух или материя?'},
            {'id': 3,
             'question_text': 'Существует ли свобода воли?'},
            {'id': 1,
             'question_text': 'В чем смысл жизни?'},
            {'id': 4,
             'question_text': 'Существует ли свобода?'},
            {'id': 5,
             'question_text': None},
        ]}

# def index_post(request):
#     latest_question_list = [{'id': 1,
#                             'question_text': 'В чем смысл жизни?'},
#                             {'id': 2,
#                             'question_text': 'Что первично, дух или материя?'},
#                             {'id': 3,
#                             'question_text': 'Существует ли свобода воли?'},]
#     template= loader.get_template("post_page.html")
#     context={"latest_question_list": latest_question_list}
#     return HttpResponse(template.render(context, request))
    
def post_page(request, number):
    if number == 1:
        return HttpResponse(
            "Кто-то или что-то на славу потрудилось, "
            "придумав нас настолько непохожими друг на друга,"
            " но в одном это что-то явно загналось несильно,"
            " а именно в человеческой необходимости стремиться"
            " к чему-либо. Да, каждый человек уникален,"
            " но не существует ни одной жизни, в которой не"
            " было бы мечт, желаний, и целей, ведь все мы куда-то"
            " движемся в нашем существовании, нам важно чего-то достичь,"
            " никто из нас не хочет прожить зря.")
    elif number == 2:
        return HttpResponse(
            "Обычно проблематизируется в форме вопроса:"
            " «Что первично, дух или материя?»."
            " Марксизм выделяет два основных варианта"
            " решения основного вопроса философии:"
            " материализм, при котором материя обладает"
            " преимуществом по отношению к сознанию,"
            " и идеализм, при котором идея первична к материи.")
    elif number == 3:
        return HttpResponse(
            "В наше время любят говорить: "
            "свободы воли не существует (речь идет о"
            " свободе человека как мыслящего и действующего"
            " существа). В современной философии подобные идеи можно"
            " подвести под рубрику «физикализм». В простейшем"
            " обобщении физикализм утверждает, что представление о "
            "свободе воли (или, иначе, возможности выбора) есть чистейшая"
            " иллюзия, мы функционируем по программе, «встроенной» в нас"
            " природой, и свободы у нас не больше, чем у растения или"
            " животного.")
    else:
        return HttpResponse("Другой вопрос")
