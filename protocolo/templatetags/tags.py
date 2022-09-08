from django import template
register = template.Library()

@register.filter
def convert(value):
    return value.encode('iso-8859-1').decode('iso-8859-1') if value else value

@register.simple_tag
def minimum(val1, val2):
    return min(val1,val2)

@register.simple_tag
def count(list):
    return len(list)

@register.simple_tag
def subtraction(val1, val2):
    return val1-val2

@register.simple_tag
def abvd_evaluation(val):
    if val == 0:
        return "Nulo"
    elif val <= 7:
        return "Ligeiro"
    elif val <= 14:
        return "Moderado"
    elif val <= 19:
        return "Severo"
    elif val <= 24:
        return "Muito Severo"

@register.simple_tag
def aivd_evaluation(val, sex):
    if sex == 'Masculino':
        if val == 0:
            return "Total"
        elif val <= 1:
            return "Grave"
        elif val <= 3:
            return "Moderada"
        elif val <= 4:
            return "Ligeira"
        else:
            return "Independente"
    elif sex == 'Feminino':
        if val <= 1:
            return "Total"
        elif val <= 3:
            return "Grave"
        elif val <= 5:
            return "Moderada"
        elif val <= 7:
            return "Ligeira"
        else:
            return "Independente"


@register.simple_tag
def hads_a_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'HADS':
            if a.question.order % 2 != 0:
                q = q + a.quotation
    return q


@register.simple_tag
def hads_d_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'HADS':
            if a.question.order % 2 == 0:
                q = q + a.quotation
    return q

@register.simple_tag
def hads_evaluation(quotation):
    if quotation <= 7:
        return "Normal"
    elif quotation <= 10:
        return "Ligeiro"
    elif quotation <= 14:
        return "Moderado"
    else:
        return "Severo"

@register.simple_tag
def bsi_somatizacao_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [2,7,23,29,30,33,37]:
                q = q + a.multiple_choice_answer.quotation
    return q

@register.simple_tag
def bsi_obs_comp_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [5,15,26,27,32,36]:
                q = q + a.multiple_choice_answer.quotation
    return q

@register.simple_tag
def bsi_sens_interp_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [20,21,22,42]:
                q = q + a.multiple_choice_answer.quotation
    return q

@register.simple_tag
def bsi_depressao_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [9,16,17,18,35,50]:
                q = q + a.multiple_choice_answer.quotation
    return q

@register.simple_tag
def bsi_ansiedade_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [1,12,19,38,45,49]:
                q = q + a.multiple_choice_answer.quotation
    return q

@register.simple_tag
def bsi_hostilidade_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [6,13,40,41,46]:
                q = q + a.multiple_choice_answer.quotation
    return q

@register.simple_tag
def bsi_ansiedade_fob_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [8,28,31,43,47]:
                q = q + a.multiple_choice_answer.quotation
    return q

@register.simple_tag
def bsi_ideacao_paranoide_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [4,10,24,48,51]:
                q = q + a.multiple_choice_answer.quotation
    return q

@register.simple_tag
def bsi_psicoticismo_quotation(answers):
    q = 0
    for a in answers:
        if a.instrument == 'BSI':
            if a.question.order in [3,14,34,44,53]:
                q = q + a.multiple_choice_answer.quotation
    return q

@register.simple_tag
def gds_evaluation(answers):
    for a in answers:
        if a.instrument == 'GDS':
            if 'Estadio' in a.question.name:
                return f"Nível {a.quotation}: {a.multiple_choice_answer.name}"

@register.simple_tag
def exist_answers(instrument, answers):
    for a in answers:
        if a.instrument == instrument:
            return True

@register.simple_tag
def mmse_evaluation(patient, quotation):
    #True = Com declinio
    #False = Sem declinio
    if patient.escolaridade == '0':
        return quotation <= 15
    elif patient.escolaridade in ['0-4','5-9','10-12']:
        return quotation <= 22
    else:
        return quotation <=27
