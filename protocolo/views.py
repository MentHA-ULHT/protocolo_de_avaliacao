from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from .models import Protocol, Part, Area, Instrument, Dimension, Section, Question, Resolution, Answer, PossibleAnswer
from django.urls import reverse
from .functions import *
from .forms import *


# Create your views here.
def dashboard_view(request):
    return render(request, 'protocolo/dashboard.html')

def dashboard_content_view(request):
    return render(request, 'protocolo/dashboardcontent.html')

def protocolos_view(request):
    context = {'protocolos': Protocol.objects.all().order_by('order')}
    return render(request, 'protocolo/protocolos.html', context)


def parts_view(request, protocol_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    resolutions = Resolution.objects.filter(patient=request.user)  # Mudar request.user para o patient depois
    parts = Part.objects.filter(protocol=protocol_id).order_by('order')

    # statistics
    answered_list = []
    percentage_list = []
    for part in parts:
        resolution = resolutions.filter(part=part)
        if not resolution:
            answered_list.append(0)
            percentage_list.append(0)
        else:
            s = resolution.get().statistics
            answered_list.append(s.get('total_answered'))
            percentage_list.append(s.get('total_percentage'))
    # print(answered_list)
    # print(percentage_list)

    context = {
        'parts': zip(parts, answered_list, percentage_list),
        'protocol': protocol,
        'resolutions': resolutions,
    }
    return render(request, 'protocolo/parts.html', context)


def areas_view(request, protocol_id, part_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    areas = Area.objects.filter(part=part).order_by('order')

    # ESTOU A CRIAR A RESOLUÇAO AQUI, MAS DEPOIS MUDAR DE SITIO
    r = None
    if Resolution.objects.filter(patient=request.user, part=part).exists():
        r = Resolution.objects.filter(patient=request.user, part=part).get()
    else:
        r = Resolution(patient=request.user, part=part)
        r.initialize_statistics()
        r.save()
        # Sem esta ultima linha a página das àreas vinha vazia
        r = Resolution.objects.get(patient=request.user, part=part)

    # statistics
    # print_nested_dict(r.statistics, 0)
    answered_list = []
    percentage_list = []
    s = r.statistics
    for area in areas:
        if s.get(f'{area.id}') is not None:
            answered_list.append(s.get(f'{area.id}').get('answered'))
            percentage_list.append(s.get(f'{area.id}').get('percentage'))

    context = {
        'areas': zip(areas, answered_list, percentage_list),
        'part': part,
        'protocol': protocol,
        'resolution': r.id
    }
    return render(request, 'protocolo/areas.html', context)


def instruments_view(request, protocol_id, part_id, area_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)

    instruments = Instrument.objects.filter(area=area_id).order_by('order')

    # statistics
    r = Resolution.objects.get(patient=request.user, part=part)
    # print_nested_dict(r.statistics, 0)
    answered_list = []
    percentage_list = []
    s = r.statistics
    for instrument in instruments:
        if s.get(f'{area.id}') is not None:
            answered_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get('answered'))
            percentage_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get('percentage'))
    # print(answered_list)
    # print(percentage_list)

    context = {
        'area': area,
        'part': part,
        'protocol': protocol,
        'instruments': zip(instruments, answered_list, percentage_list),
        'resolution' : r.id,
    }

    return render(request, 'protocolo/instruments.html', context)


def dimensions_view(request, protocol_id, part_id, area_id, instrument_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)
    instrument = Instrument.objects.get(pk=instrument_id)

    dimensions = Dimension.objects.filter(instrument=instrument_id).order_by('order')

    # statistics
    r = Resolution.objects.get(patient=request.user, part=part)
    # print_nested_dict(r.statistics, 0)
    answered_list = []
    percentage_list = []
    s = r.statistics
    for dimension in dimensions:
        if s.get(f'{area.id}') is not None:
            answered_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get('answered'))
            percentage_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get('percentage'))
    # print(answered_list)
    # print(percentage_list)

    context = {
        'area': area,
        'part': part,
        'protocol': protocol,
        'instrument': instrument,
        'dimensions': zip(dimensions, answered_list, percentage_list),
        'resolution': r.id,
    }
    return render(request, 'protocolo/dimensions.html', context)


def sections_view(request, protocol_id, part_id, area_id, instrument_id, dimension_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)
    instrument = Instrument.objects.get(pk=instrument_id)
    dimension = Dimension.objects.get(pk=dimension_id)

    sections = Section.objects.filter(dimension=dimension_id).order_by('order')

    # statistics
    r = Resolution.objects.get(patient=request.user, part=part)
    # print_nested_dict(r.statistics, 0)
    answered_list = []
    percentage_list = []
    s = r.statistics
    for section in sections:
        if s.get(f'{area.id}') is not None:
            answered_list.append(
                s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get(f'{section.id}').get('answered'))
            percentage_list.append(
                s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get(f'{section.id}').get(
                    'percentage'))
    # print(answered_list)
    # print(percentage_list)

    if len(sections) == 1:
        return redirect(question_view)

    context = {
        'area': area,
        'part': part,
        'protocol': protocol,
        'instrument': instrument,
        'dimension': dimension,
        'sections': zip(sections, answered_list, percentage_list),
        'resolution': r.id,
    }

    return render(request, 'protocolo/sections.html', context)


def question_view(request, protocol_id, part_id, area_id, instrument_id, dimension_id, section_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)
    instrument = Instrument.objects.get(pk=instrument_id)
    dimension = Dimension.objects.get(pk=dimension_id)
    section = Section.objects.get(pk=section_id)
    question = Question.objects.get(section=section.id)
    r = Resolution.objects.get(patient=request.user, part=part)
    answers = Answer.objects.filter(resolution=r)
    print(question.helping_images)
    form = uploadAnswerForm(request.POST or None)

    context = {
        'area': area,
        'part': part,
        'protocol': protocol,
        'instrument': instrument,
        'dimension': dimension,
        'section': section,
        'question': question,
        'form': form,
        'resolution': r.id,
    }

    for answer in answers:
        if answer.resolution == r:
            if answer.question == question:
                if answer.multiple_choice_answer is not None:
                    existing_answer_id = answer.multiple_choice_answer.id
                    context['existing_answer_id'] = existing_answer_id
                if answer.text_answer is not None:
                    form.initial.update({'text_answer': answer.text_answer})
                if answer.submitted_answer:
                    context['submitted_answer'] = answer.submitted_answer.url
                if answer.notes is not None:
                    context['notes'] = answer.notes
                if answer.quotation is not None:
                    context['quotation'] = answer.quotation
    print(context['notes'])
    if request.method == 'POST':
        question_type = int(request.POST.get('type'))  # 0 -> Escolha Multipla \ 1 -> Resposta Escrita
        existing_answer = None

        for answer in answers:
            if answer.question == question:
                existing_answer = answer
                print(existing_answer)

        if question_type == 0:
            print(request.POST)
            id_answer = request.POST.get("choice")
            r = Resolution.objects.get(part=part,
                                       patient=request.user)
            if existing_answer is None:
                # cria uma nova associação
                new_answer = Answer(question=question,
                                    multiple_choice_answer=PossibleAnswer.objects.get(pk=id_answer),
                                    resolution=r)
                quotation = new_answer.multiple_choice_answer.quotation
                new_answer.quotation = quotation
                new_answer.notes = request.POST.get('notes')
                new_answer.save()
                r.increment_statistics(f'{part_id}', f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                       f'{section_id}')
                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                   f'{section_id}', quotation)
            else:
                # modifica a associação existente
                existing_answer.multiple_choice_answer = PossibleAnswer.objects.get(pk=id_answer)
                quotation = existing_answer.multiple_choice_answer.quotation
                existing_answer.quotation = quotation
                existing_answer.notes = request.POST.get('notes')
                existing_answer.save()
                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                   f'{section_id}', quotation)
            # quando guarda a pergunta volta às secções
            return redirect('sections',
                            protocol_id=protocol_id, part_id=part_id,
                            area_id=area_id, instrument_id=instrument_id,
                            dimension_id=dimension_id)
        elif question_type == 1:
            form = uploadAnswerForm(request.POST, files=request.FILES)
            if form.is_valid():
                new_answer = Answer()
                new_answer.submitted_answer = form.cleaned_data['submitted_answer']
                new_answer.text_answer = form.cleaned_data['text_answer']
                new_answer.quotation = form.cleaned_data['quotation']
                new_answer.notes = form.cleaned_data['notes']
                new_answer.question = question
                new_answer.resolution = r

                if existing_answer is None:
                    # cria uma nova resposta
                    r.increment_statistics(f'{part_id}', f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                           f'{section_id}')
                    new_answer.resolution = r
                    new_answer.save()
                else:
                    # modifica a resposta existente
                    existing_answer.submitted_answer = new_answer.submitted_answer
                    existing_answer.text_answer = new_answer.text_answer
                    existing_answer.quotation = new_answer.quotation
                    existing_answer.notes = new_answer.notes
                    existing_answer.save()


                r.change_quotation( f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                           f'{section_id}', new_answer.quotation)
                # quando guarda a pergunta volta às secções
                return redirect('sections',
                                protocol_id=protocol_id, part_id=part_id,
                                area_id=area_id, instrument_id=instrument_id,
                                dimension_id=dimension_id)
    return render(request, 'protocolo/question.html', context)


def report_view(request, resolution_id):
    r = Resolution.objects.get(pk=resolution_id)
    # É necessário o ensure_ascii = False para mostrar caracteres UTF-8
    report_json = r.statistics
    report_json_dumps = json.dumps(report_json, indent=1, sort_keys=False, ensure_ascii=False)
    report = {}
    answers = Answer.objects.filter(resolution=r)

    for area in Area.objects.filter(part=r.part):
        report[area.name] = {}
        instruments = Instrument.objects.filter(area=area)
        for instrument in instruments:
            report[area.name][instrument.name] = {}
            dimensions = Dimension.objects.filter(instrument=instrument)
            report[area.name][instrument.name]["Total"] = 0
            for dimension in dimensions:
                report[area.name][instrument.name][dimension.name] = {}
                report[area.name][instrument.name][dimension.name]['Total'] = 0
                sections = Section.objects.filter(dimension=dimension)
                for section in sections:
                    report[area.name][instrument.name][dimension.name][section.name] = {}
                    questions = Question.objects.filter(section=section)
                    # for question in questions:
                    report[area.name][instrument.name][dimension.name][section.name] = \
                        report_json[str(area.id)][str(instrument.id)][str(dimension.id)][str(section.id)].get(
                            'quotation')
                    sum_quotations = 0
                    for question in questions:
                        answer = Answer.objects.filter(question=question, resolution=r)
                        if answer.exists():
                            print(answer.get().quotation)
                            report[area.name][instrument.name]["Total"] += answer.get().quotation
                            report[area.name][instrument.name][dimension.name]["Total"] += answer.get().quotation


    print(questions)
    print(answers)



    #print(json.dumps(report_json, indent=1, sort_keys=False, ensure_ascii=False))
    # Funcionalidade
    context = {'report_json': report_json,
               'report_json_dumps': report_json_dumps,
               'report': report,
               'resolution': r,
               'answers': answers,
               }

    return render(request, 'protocolo/report.html', context)
