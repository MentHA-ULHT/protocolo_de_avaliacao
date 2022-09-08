from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Protocol, Part, Area, Instrument, Dimension, Section, Question, Resolution, Answer, PossibleAnswer
from django.urls import reverse
from .functions import *
from .forms import *
from diario.models import *

# Other Imports
import plotly.graph_objects as go
import plotly
import pandas as pd


# Create your views here.
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'protocolo/dashboard.html')


@login_required(login_url='login')
def dashboard_content_view(request):
    return render(request, 'protocolo/dashboardcontent.html')


@login_required(login_url='login')
def protocolos_view(request):
    context = {'protocolos': Protocol.objects.all().order_by('order')}
    return render(request, 'protocolo/protocolos.html', context)


@login_required(login_url='login')
def parts_view(request, protocol_id, patient_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    resolutions = Resolution.objects.filter(doctor=request.user, patient=Participante.objects.filter(
        pk=patient_id).get())  # Mudar request.user para o patient depois
    parts = Part.objects.filter(protocol=protocol_id).order_by('order')
    patient = Participante.objects.get(pk=patient_id)

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
        'patient': patient,
    }
    return render(request, 'protocolo/parts.html', context)


@login_required(login_url='login')
def areas_view(request, protocol_id, part_id, patient_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    areas = Area.objects.filter(part=part).order_by('order')
    patient = Participante.objects.get(pk=patient_id)

    # ESTOU A CRIAR A RESOLUÇAO AQUI, MAS DEPOIS MUDAR DE SITIO
    r = None
    if Resolution.objects.filter(patient=patient, part=part, doctor=request.user).exists():
        r = Resolution.objects.filter(patient=patient, part=part, doctor=request.user).get()
    else:
        r = Resolution(patient=patient, part=part, doctor=request.user)
        r.initialize_statistics()
        r.save()
        # Sem esta ultima linha a página das àreas vinha vazia
        r = Resolution.objects.get(patient=patient, part=part, doctor=request.user)

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
        'resolution': r.id,
        'patient': patient,
    }
    return render(request, 'protocolo/areas.html', context)


@login_required(login_url='login')
def instruments_view(request, protocol_id, part_id, area_id, patient_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)
    patient = Participante.objects.get(pk=patient_id)

    instruments = Instrument.objects.filter(area=area_id).order_by('order')

    # statistics
    r = Resolution.objects.get(patient=patient, doctor=request.user, part=part)
    # print_nested_dict(r.statistics, 0)
    answered_list = []
    percentage_list = []
    quotation_list = []
    s = r.statistics
    for instrument in instruments:
        if s.get(f'{area.id}') is not None:
            answered_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get('answered'))
            percentage_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get('percentage'))
            quotation_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get('quotation'))
    # print(answered_list)
    # print(percentage_list)

    context = {
        'area': area,
        'part': part,
        'protocol': protocol,
        'instruments': zip(instruments, answered_list, percentage_list, quotation_list),
        'resolution': r.id,
        'patient': patient,
    }

    return render(request, 'protocolo/instruments.html', context)


@login_required(login_url='login')
def dimensions_view(request, protocol_id, part_id, area_id, instrument_id, patient_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)
    instrument = Instrument.objects.get(pk=instrument_id)
    dimensions = Dimension.objects.filter(instrument=instrument_id).order_by('order')
    patient = Participante.objects.get(pk=patient_id)

    if len(dimensions) == 1:
        return redirect('sections', protocol_id, part_id, area_id, instrument_id, dimensions.get().id, patient_id)

    # statistics
    r = Resolution.objects.get(patient=patient, doctor=request.user, part=part)
    # print_nested_dict(r.statistics.get(str(area.id)).get(str(instrument.id)))
    # print(r.statistics.get(str(area.id)).get(str(instrument.id)).get('9').get('quotation'))

    answered_list = []
    percentage_list = []
    quotation_list = []
    s = r.statistics
    for dimension in dimensions:
        if s.get(f'{area.id}') is not None:
            answered_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get('answered'))
            percentage_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get('percentage'))
            quotation_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get('quotation'))
    # print(answered_list)
    # print(percentage_list)

    context = {
        'area': area,
        'part': part,
        'protocol': protocol,
        'instrument': instrument,
        'dimensions': zip(dimensions, answered_list, percentage_list, quotation_list),
        'resolution': r.id,
        'patient': patient,
    }
    return render(request, 'protocolo/dimensions.html', context)


@login_required(login_url='login')
def sections_view(request, protocol_id, part_id, area_id, instrument_id, dimension_id, patient_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)
    instrument = Instrument.objects.get(pk=instrument_id)
    dimension = Dimension.objects.get(pk=dimension_id)
    patient = Participante.objects.get(pk=patient_id)

    sections = Section.objects.filter(dimension=dimension_id).order_by('order')
    if len(sections) == 1:
        return redirect('question', protocol_id, part_id, area_id, instrument_id, dimension_id, sections.get().id,
                        patient_id)

    # statistics
    r = Resolution.objects.get(patient=patient, doctor=request.user, part=part)
    # print_nested_dict(r.statistics, 0)
    answered_list = []
    percentage_list = []
    quotation_list = []
    s = r.statistics
    for section in sections:
        if s.get(f'{area.id}') is not None:
            answered_list.append(
                s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get(f'{section.id}').get('answered'))
            percentage_list.append(
                s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get(f'{section.id}').get(
                    'percentage'))
            quotation_list.append(
                s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get(f'{section.id}').get(
                    'quotation'))

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
        'sections': zip(sections, answered_list, percentage_list, quotation_list),
        'resolution': r.id,
        'patient': patient,
    }

    # print(instrument.number_of_dimensions)

    return render(request, 'protocolo/sections.html', context)


@login_required(login_url='login')
def question_view(request, protocol_id, part_id, area_id, instrument_id, dimension_id, section_id, patient_id):
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)
    instrument = Instrument.objects.get(pk=instrument_id)
    dimension = Dimension.objects.get(pk=dimension_id)
    section = Section.objects.get(pk=section_id)
    question = Question.objects.filter(section=section).first()
    form = uploadAnswerForm(request.POST or None)
    patient = Participante.objects.get(pk=patient_id)
    r = Resolution.objects.get(patient=patient, doctor=request.user, part=part)
    answers = Answer.objects.filter(resolution=r)
    # print(question.section.number_of_questions)
    # print(question.section.dimension.number_of_questions)
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
        'answers': answers,
        'patient': patient,
    }
    # print(answers)

    if question.question_type == 3:
        question_list = []
        answered_ids = []
        for question in Question.objects.filter(section=section.id):
            question_list.append(question)
            for answer in answers:
                if question == answer.question:
                    answered_ids.append(question.id)

        # Esta parte permite dividir o question type 3 em dois
        # Um que tem sempre as mesmas respostas, e mostrará a página como uma tabela
        # Outro que as respostas são diferentes e mostrará varias perguntas individualmente, todas na mesma página
        ans = 0
        equal = True
        for question in Question.objects.filter(section=section.id):
            if ans == 0:
                ans = question.possible_answers.all()
                # print(ans)
            else:
                equal = set(question.possible_answers.all()) == set(ans)

        context['equal_answers'] = equal
        context['question_list'] = question_list

    existing_answer_id = []
    for answer in answers:
        if answer.resolution == r:
            if answer.question == question:
                if answer.multiple_choice_answer is not None:
                    existing_answer_id.append(answer.multiple_choice_answer.id)
                    context['existing_answer_id'] = existing_answer_id
                if answer.text_answer is not None:
                    form.initial.update({'text_answer': answer.text_answer})
                if answer.submitted_answer:
                    context['submitted_answer'] = answer.submitted_answer.url
                if answer.notes is not None:
                    context['notes'] = answer.notes
                if answer.quotation is not None:
                    context['quotation'] = answer.quotation
                if len(answer.MCCAnswer.all()) >= 1:
                    list = []
                    for mca in answer.MCCAnswer.all():
                        list.append(mca.choice.id)
                    existing_answer_id = list
                    context['existing_answer_id'] = list

    if request.method == 'POST':
        existing_answer = None

        for answer in answers:
            if answer.question == question:
                existing_answer = answer

        if question.question_type == 1 or question.question_type == 9:
            id_answer = request.POST.get("choice")
            r = Resolution.objects.get(part=part,
                                       patient=patient, doctor=request.user)
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


        elif question.question_type == 2:
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

                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                   f'{section_id}', new_answer.quotation)

        elif question.question_type == 3:
            for key in request.POST:
                if 'choice' in str(key):
                    k, question_id = key.split('-')
                    q = Question.objects.get(pk=question_id)
                    existing_answers_list = []

                    if q.id in answered_ids:
                        a = Answer.objects.filter(resolution=r, question=q).get()
                        # modifica a associação existente
                        a.multiple_choice_answer = PossibleAnswer.objects.get(pk=request.POST.get(key))
                        quotation = a.multiple_choice_answer.quotation
                        a.quotation = quotation
                        a.notes = request.POST.get('notes')
                        a.save()
                        r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                           f'{section_id}', quotation)
                    else:
                        a = Answer()
                        a.resolution = r
                        a.multiple_choice_answer = PossibleAnswer.objects.get(pk=request.POST.get(key))
                        a.question = q
                        quotation = a.multiple_choice_answer.quotation
                        a.quotation = quotation
                        a.notes = request.POST.get('notes')
                        a.save()
                        r.increment_statistics(f'{part_id}', f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                               f'{section_id}')
                        r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                           f'{section_id}', quotation)

        elif question.question_type == 4 or question.question_type == 6 or question.question_type == 7 or question.question_type == 8:
            existing = False
            if len(Answer.objects.filter(question=question, resolution=r)) >= 1:
                a = Answer.objects.filter(question=question, resolution=r).get()
                a.delete()
                existing = True
            a = Answer()
            a.resolution = r
            a.question = question
            a.notes = request.POST.get('notes')
            q = 0
            a.save()
            for id in request.POST.getlist("choice"):
                c = MultipleChoicesCheckbox()
                c.answer = a
                pa = PossibleAnswer.objects.filter(pk=id).get()
                c.choice = pa
                q = q + c.choice.quotation
                c.save()

            if 'Repetição I' in question.name:
                l = len(request.POST.getlist("choice"))
                if l == 4:
                    q = 2
                elif l == 3:
                    q = 1
                else:
                    q = 0

            a.quotation = q
            a.save()

            if existing:
                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                   f'{section_id}', q)
            else:
                r.increment_statistics(f'{part_id}', f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                       f'{section_id}')
                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                   f'{section_id}', q)

        elif question.question_type == 5:
            # print(request.POST)
            existing = False
            if len(Answer.objects.filter(question=question, resolution=r)) >= 1:
                a = Answer.objects.filter(question=question, resolution=r).get()
                a.delete()
                existing = True
            a = Answer()
            a.resolution = r
            a.question = question
            a.notes = request.POST.get('notes')
            a.save()
            counter = 0
            for i in range(1, 5):
                text_area = request.POST.get(str(i))
                if len(text_area) > 1:
                    counter += len(text_area.split(","))
                    print(text_area)
                    print(counter)
                    ti = TextInputAnswer()
                    ti.answer = a
                    ti.seconds = i
                    ti.text = text_area
                    ti.save()
            q = calculate_timer_quotation(question, counter)
            a.quotation = q
            a.save()

            if existing:
                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                   f'{section_id}', q)
            else:
                r.increment_statistics(f'{part_id}', f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                       f'{section_id}')
                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                   f'{section_id}', q)
        #print(question.section.dimension.number_of_questions)
        if question.question_type == 3:
            return redirect('instruments',
                            protocol_id=protocol_id, part_id=part_id,
                            area_id=area_id, patient_id=patient_id)
        elif question.section.dimension.name == "None":
            return redirect('instruments',
                            protocol_id=protocol_id, part_id=part_id,
                            area_id=area_id, patient_id=patient_id)
        elif question.section.name == "None" or question.question_type == 9 or question.section.dimension.number_of_questions == 1:
            return redirect('dimensions',
                            protocol_id=protocol_id, part_id=part_id,
                            area_id=area_id, instrument_id=instrument_id, patient_id=patient_id)
        else:
            return redirect('sections',
                            protocol_id=protocol_id, part_id=part_id,
                            area_id=area_id, instrument_id=instrument_id, dimension_id=dimension_id, patient_id=patient_id)



    return render(request, 'protocolo/question.html', context)





@login_required(login_url='login')
def report_view(request, resolution_id):
    r = Resolution.objects.get(pk=resolution_id)
    # print(r)
    # É necessário o ensure_ascii = False para mostrar caracteres UTF-8
    report_json = r.statistics
    report_json_dumps = json.dumps(report_json, indent=1, sort_keys=False, ensure_ascii=False)
    report = {}
    answers = Answer.objects.filter(resolution=r).order_by("question__section__order")
    # print(answers)
    done = []

    for area in Area.objects.filter(part=r.part):
        report[area.name] = {}
        instruments = Instrument.objects.filter(area=area)
        for instrument in instruments:
            quotations = []
            names = []
            report[area.name][instrument.name] = {}
            dimensions = Dimension.objects.filter(instrument=instrument)
            report[area.name][instrument.name]["Total"] = 0
            report[area.name][instrument.name]["Graph"] = None
            for dimension in dimensions:
                if dimension.name != 'None':
                    names.append(dimension.name)
                report[area.name][instrument.name][dimension.name] = {}
                report[area.name][instrument.name][dimension.name]['Total'] = 0
                sections = Section.objects.filter(dimension=dimension)
                for section in sections:
                    if dimension.name == 'None' and section.name != 'None':
                        names.append(section.name)
                    report[area.name][instrument.name][dimension.name][section.name] = {}
                    questions = Question.objects.filter(section=section)
                    report[area.name][instrument.name][dimension.name][section.name] = \
                        report_json[str(area.id)][str(instrument.id)][str(dimension.id)][str(section.id)].get(
                            'quotation')
                    for question in questions:
                        answer = Answer.objects.filter(question=question, resolution=r)
                        if answer.exists():
                            report[area.name][instrument.name]["Total"] += answer.get().quotation
                            if report[area.name][instrument.name][dimension.name][
                                "Total"] + answer.get().quotation <= question.quotation_max:
                                report[area.name][instrument.name][dimension.name]["Total"] += answer.get().quotation
                            if dimension.name == 'None' and section.name != 'None':
                                quotations.append(answer.get().quotation)
                if dimension.name != 'None':
                    quotations.append(report[area.name][instrument.name][dimension.name]["Total"])

            if len(quotations) == len(names) and dimension.name != 'None' or len(quotations) == len(
                    names) and section.name != 'None' and len(quotations) != 0:
                for answer in answers:
                    if answer.instrument == instrument.name and instrument.name not in done:
                        report[area.name][instrument.name]["Graph"] = make_graph(names,quotations, instrument.minimum_quotation, instrument.maximum_quotation)
                        done.append(instrument.name)

        for instrument in instruments:
            if instrument.name == "BSI":
                for answer in answers:
                    if answer.instrument == instrument.name:
                        names = ['Somatização', 'Obsessões-Compulsões', 'Depressão', 'Sensibilidade Interpessoal', 'Ansiedade',
                                 'Hostilidade', 'Ansiedade Fóbica', 'Ideação Paranóide', 'Psicotismo']
                        quotations = bsi_quotation(answers)
                        report[area.name]["BSI"]["Graph"] = make_graph(names, quotations, 0, 28)
                        done.append(instrument.name)

    # print(json.dumps(report_json, indent=1, sort_keys=False, ensure_ascii=False))
    # Funcionalidade
    context = {'report_json': report_json,
               'report_json_dumps': report_json_dumps,
               'report': report,
               'resolution': r,
               'answers': answers,
               'instruments': Instrument.objects.all(),
               'questions': Question.objects.all(),}
    print(Question.objects.all())

    return render(request, 'protocolo/report.html', context)


@login_required(login_url='login')
def protocol_participants_view(request, protocol_id):
    doctor = request.user
    protocolo = Protocol.objects.get(pk=protocol_id)
    participants = Participante.objects.filter(avaliador=doctor)
    resolutions = Resolution.objects.filter(doctor=doctor)

    context = {'participants': participants,
               'resolutions': resolutions,
               'protocolo': protocolo}
    return render(request, 'protocolo/protocol-participants.html', context)


@login_required(login_url='login')
def participants_view(request):
    doctor = request.user
    participants = Participante.objects.filter(avaliador=doctor)
    resolutions = Resolution.objects.filter(doctor=doctor)

    context = {'participants': participants,
               'resolutions': resolutions}
    return render(request, 'protocolo/participants.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'protocolo/login.html')


from django.contrib.auth import logout


def logout_view(request):
    logout(request)

    return render(request, 'protocolo/login.html')


def profile_view(request, participant_id):
    #Falta mostrar as resoluções das partes feitas no perfil e os seus relatorios
    p = Participante.objects.filter(pk=participant_id).get()
    resolutions = Resolution.objects.filter(patient=p)
    c = []

    for cuidador in Cuidador.objects.all():
        if cuidador in p.cuidadores.all():
            c.append(cuidador.nome)

    cuidadores = ", ".join(c)

    # print(cuidadores)
    context = {
        'p': p,
        'cuidadores': cuidadores,
        'resolutions': resolutions,
    }
    return render(request, 'protocolo/profile.html', context)
