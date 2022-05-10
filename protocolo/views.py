from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from .models import Protocol, Part, Area, Instrument, Dimension, Section, Question, Resolution, Answer, PossibleAnswer
from django.urls import reverse
from .functions import *
from .forms import *


# Create your views here.
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
    # ESTOU A CRIAR A RESOLUÇAO AQUI, MAS DEPOIS MUDAR DE SITIO
    current_resolution = Resolution(patient=request.user, part=Part.objects.get(pk=part_id))
    existing_resolution = Resolution.objects.filter(patient=request.user, part=Part.objects.get(pk=part_id))
    r = None
    if not existing_resolution:
        r = current_resolution
        r.initialize_statistics()
        r.save()
    else:
        r = existing_resolution.get()

    # Areas de Avaliaçao = Dimensões
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)

    areas = Area.objects.filter(part=part).order_by('order')

    # statistics
    # print_nested_dict(r.statistics, 0)
    answered_list = []
    percentage_list = []
    s = r.statistics
    for area in areas:
        if s.get(f'{area.id}') is not None:
            answered_list.append(s.get(f'{area.id}').get('answered'))
            percentage_list.append(s.get(f'{area.id}').get('percentage'))
    # print(answered_list)
    # print(percentage_list)

    context = {
        'areas': zip(areas, answered_list, percentage_list),
        'part': part,
        'protocol': protocol,
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
        'instruments': zip(instruments, answered_list, percentage_list)
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
    a = Answer.objects.filter(resolution=r)

    form = uploadAnswerForm

    context = {
        'area': area,
        'part': part,
        'protocol': protocol,
        'instrument': instrument,
        'dimension': dimension,
        'section': section,
        'question': question,
        'form': form,
    }

    for answer in a:
        if answer.resolution == r:
            if answer.question == question:
                existing_answer_id = answer.multiple_choice_answer.id
                context['existing_answer_id'] = existing_answer_id

    if request.method == 'POST':
        id_answer = request.POST.get("choice")
        print(request.POST)
        print(id_answer)
        r = Resolution.objects.get(part=part,
                                   patient=request.user)

        for answer in a:
            if answer.question == question:
                existing_answer = answer
                break

        if existing_answer is None:
            # cria uma nova associação
            a = Answer(question=question,
                       multiple_choice_answer=PossibleAnswer.objects.get(pk=id_answer))
            a.save()
            r.increment_statistics(f'{part_id}', f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                   f'{section_id}')
            r.answers.add(a)
            r.save()
        else:
            # modifica a associação existente
            existing_answer.multiple_choice_answer = PossibleAnswer.objects.get(pk=id_answer)
            existing_answer.save()
        # quando guarda a pergunta volta às secções
        return redirect('sections',
                        protocol_id=protocol_id, part_id=part_id,
                        area_id=area_id, instrument_id=instrument_id,
                        dimension_id=dimension_id)

    return render(request, 'protocolo/question.html', context)
