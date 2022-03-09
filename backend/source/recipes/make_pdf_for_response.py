# import os
from io import BytesIO

# from io import StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# from django.shortcuts import render


# Все перепробовал уже...
# Не получается отрендерить мне пдф норм...
# Вместо Кириллицы там квадратики черные
def render_pdf_view(context):
    template_path = 'to_pdf.html'
    # context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # If download:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # If display:
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html.encode('utf-8'), dest=response,
        encoding='utf-8')
    # ,link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return render(request, template_path, context)
    return response


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    html = html.encode('cp1251')
    print(html)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
