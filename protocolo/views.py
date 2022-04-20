from django.shortcuts import render, HttpResponse, redirect
from .models import Protocol, Part, Area, Instrument, Dimension, Section, Question, Resolution, Answer, PossibleAnswer


# Create your views here.
def protocolos_view(request):
    context = {'protocolos': Protocol.objects.all().order_by('order')}
    return render(request, 'protocolo/protocolos.html', context)


def parts_view(request, protocol_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    resolutions = Resolution.objects.filter(patient=request.user)  # Mudar request.user para o patient depois
    parts = Part.objects.filter(protocol=protocol_id).order_by('order')

    # Variaveis e calculos para o progresso
    nr_answered = get_answered_questions_per_part(parts, request.user)  # lista com o nr de perguntas respondidas
    print(nr_answered)
    percentage = get_percentage(parts, nr_answered)

    context = {
        'parts': zip(parts, nr_answered, percentage),
        'protocol': protocol,
        'resolutions': resolutions,
    }
    return render(request, 'protocolo/parts.html', context)


def areas_view(request, protocol_id, part_id):
    # ESTOU A CRIAR A RESOLUÇAO AQUI, MAS DEPOIS MUDAR DE SITIO
    r = Resolution(patient=request.user, part=Part.objects.get(pk=part_id))
    if r is None:
        r.save()

    # Areas de Avaliaçao = Dimensões
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)

    areas = Area.objects.filter(part=part).order_by('order')

    # Variaveis e calculos para o progresso
    nr_answered = get_answered_questions_per_area(part, areas, request.user)
    percentage = get_percentage(areas, nr_answered)

    context = {
        'areas': zip(areas, nr_answered, percentage),
        'part': part,
        'protocol': protocol,
    }
    return render(request, 'protocolo/areas.html', context)


def instruments_view(request, protocol_id, part_id, area_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)

    instruments = Instrument.objects.filter(area=area_id).order_by('order')

    # Variaveis e calculos para o progresso
    nr_answered = get_answered_questions_per_instrument(part, instruments, request.user)
    percentage = get_percentage(instruments, nr_answered)

    context = {
        'area': area,
        'part': part,
        'protocol': protocol,
        'instruments': zip(instruments,nr_answered,percentage)
    }

    return render(request, 'protocolo/instruments.html', context)


def dimensions_view(request, protocol_id, part_id, area_id, instrument_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)
    instrument = Instrument.objects.get(pk=instrument_id)

    dimensions = Dimension.objects.filter(instrument=instrument_id).order_by('order')

    context = {
        'area': area,
        'part': part,
        'protocol': protocol,
        'instrument': instrument,
        'dimensions': dimensions,
    }
    return render(request, 'protocolo/dimensions.html', context)


def sections_view(request, protocol_id, part_id, area_id, instrument_id, dimension_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)
    instrument = Instrument.objects.get(pk=instrument_id)
    dimension = Dimension.objects.get(pk=dimension_id)

    sections = Section.objects.filter(dimension=dimension_id).order_by('order')

    if len(sections) == 1:
        return redirect(question_view)

    context = {
        'area': area,
        'part': part,
        'protocol': protocol,
        'instrument': instrument,
        'dimension': dimension,
        'sections': sections,
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

    context = {
        'area': area,
        'part': part,
        'protocol': protocol,
        'instrument': instrument,
        'dimension': dimension,
        'section': section,
        'question': question,
    }

    for answer in r.answers.all():
        if answer.question == question:
            existing_answer_id = answer.multiple_choice_answer.id
            context['existing_answer_id'] = existing_answer_id

    return render(request, 'protocolo/question.html', context)


def post_mcq_view(request, protocol_id, part_id, area_id, instrument_id, dimension_id, section_id, question_id):
    part = Part.objects.get(pk=part_id)
    question = Question.objects.get(pk=question_id)
    user = request.user
    existing_answer = None

    if request.method == "POST":
        id_answer = request.POST.get("choice")

        r = Resolution.objects.get(part=part,
                                   patient=user)

        for answer in r.answers.all():
            if answer.question == question:
                existing_answer = answer
                break

        if existing_answer is None:
            # cria uma nova associação
            a = Answer(question=question,
                       multiple_choice_answer=PossibleAnswer.objects.get(pk=id_answer))
            a.save()
            r.answers.add(a)
            r.save()
        else:
            # modifica a associação existente
            existing_answer.multiple_choice_answer = PossibleAnswer.objects.get(pk=id_answer)
            existing_answer.save()

    # talvez dar redirect para a página anterior (sections)
    return redirect('question', protocol_id, part_id, area_id, instrument_id, dimension_id, section_id)


# Funções
def get_answered_questions_per_part(parts, user):
    nr_answered = []

    for part in parts:
        count = 0
        resolutions = Resolution.objects.filter(part=part, patient=user)
        for resolution in resolutions:
            count = len(resolution.answers.all())
        nr_answered.append(count)

    return nr_answered


def get_answered_questions_per_area(part, areas, user):
    resolution = Resolution.objects.filter(part=part, patient=user)
    nr_answered = []
    for area in areas:
        count = 0
        instruments = Instrument.objects.filter(area=area)
        for i in instruments:
            dimensions = Dimension.objects.filter(instrument=i)
            for d in dimensions:
                sections = Section.objects.filter(dimension=d)
                for s in sections:
                    questions = Question.objects.filter(section=s)
                    for q in questions:
                        for r in resolution:
                            for a in r.answers.all():
                                if a.question == q:
                                    count += 1
        nr_answered.append(count)

    return nr_answered


def get_answered_questions_per_instrument(part, instruments, user):
    resolution = Resolution.objects.filter(part=part, patient=user)
    nr_answered = []
    for i in instruments:
        count = 0
        dimensions = Dimension.objects.filter(instrument=i)
        for d in dimensions:
            sections = Section.objects.filter(dimension=d)
            for s in sections:
                questions = Question.objects.filter(section=s)
                for q in questions:
                    for r in resolution:
                        for a in r.answers.all():
                            if a.question == q:
                                count += 1
        nr_answered.append(count)

    return nr_answered


def get_percentage(obj_list, nr_answered):
    percentage = []
    for n, obj in enumerate(obj_list):
        p = 0
        if (n <= len(nr_answered)):
            if nr_answered[n] > 0 and obj.number_of_questions > 0:
                p = (nr_answered[n] / obj.number_of_questions) * 100
        percentage.append(int(p))
    return percentage
