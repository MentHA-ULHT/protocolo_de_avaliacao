import json

from django.db import models
from django.utils import timezone
from django.conf import settings
from .functions import percentage

# Create your models here.

SMALL_LEN = 50
MEDIUM_LEN = 150
LONG_LEN = 500

HELPING_IMAGES_DIR = "helping_images/"


# É possivel criar um modelo "Common"
# Que terá name, description, order e talvez note (apontamento)
# Uma vez que sao comuns a todas as classes

class Common(models.Model):
    name = models.CharField(max_length=MEDIUM_LEN)
    description = models.CharField(max_length=LONG_LEN,
                                   blank=True,
                                   null=True)
    order = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Protocol(Common):

    def __str__(self):
        return f"{self.name}"


class Part(Common):
    protocol = models.ForeignKey('Protocol', on_delete=models.CASCADE)
    part_number = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

    @property
    def number_of_areas(self):
        return len(Area.objects.filter(part=self))

    @property
    def number_of_questions(self):
        n = 0
        a = Area.objects.filter(part=self)
        for area in a:
            i = Instrument.objects.filter(area=area)
            for inst in i:
                d = Dimension.objects.filter(instrument=inst)
                for dim in d:
                    s = Section.objects.filter(dimension=dim)
                    for sec in s:
                        n += sec.number_of_questions
        return n


class Area(Common):
    part = models.ManyToManyField('Part',
                                  default=None,
                                  related_name='areas')

    def __str__(self):
        part_list = ", ".join(str(p.name) for p in self.part.all())
        return f' {part_list} >> {self.order}. {self.name}'

    @property
    def number_of_instruments(self):
        return len(Instrument.objects.filter(area=self))

    @property
    def number_of_questions(self):
        count = 0
        instruments = Instrument.objects.filter(area=self)
        for i in instruments:
            dimensions = Dimension.objects.filter(instrument=i)
            for d in dimensions:
                sections = Section.objects.filter(dimension=d)
                for s in sections:
                    count += s.number_of_questions
        return count


class Instrument(Common):
    area = models.ForeignKey('Area', on_delete=models.CASCADE, related_name='instruments')

    def __str__(self):
        return f"{self.area.name} >> {self.name}"

    @property
    def number_of_dimensions(self):
        return len(Dimension.objects.filter(instrument=self.id))

    @property
    def number_of_questions(self):
        count = 0
        dimensions = Dimension.objects.filter(instrument=self)
        for d in dimensions:
            sections = Section.objects.filter(dimension=d)
            for s in sections:
                count += s.number_of_questions

        return count


class Dimension(Common):
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE)

    @property
    def number_of_sections(self):
        return len(Section.objects.filter(dimension=self.id))

    @property
    def number_of_questions(self):
        count = 0
        sections = Section.objects.filter(dimension=self)
        for s in sections:
            count += s.number_of_questions

        return count

    def __str__(self):
        return f"{self.instrument.name} >> {self.name}"


class Section(Common):
    dimension = models.ForeignKey('Dimension', on_delete=models.CASCADE)

    @property
    def number_of_questions(self):
        return len(Question.objects.filter(section=self.id))

    def __str__(self):
        return f"{self.dimension.name} >> {self.name}"


class Question(Common):
    instruction = models.CharField(max_length=LONG_LEN,
                                   blank=True)
    helping_images = models.ManyToManyField('QuestionImage',
                                            default=None,
                                            related_name='images',
                                            blank=True)
    section = models.ForeignKey('Section',
                                on_delete=models.CASCADE)
    possible_answers = models.ManyToManyField('PossibleAnswer',
                                              default=None,
                                              related_name='possible_answers',
                                              blank=True)
    quotation_max = models.IntegerField(default=0)
    quotation_min = models.IntegerField(default=1)

    @property
    def allow_submission(self):
        if len(self.possible_answers) <= 0:
            return True
        return False

    def __str__(self):
        return f"{self.name}"


class QuestionImage(models.Model):
    name = models.CharField(max_length=MEDIUM_LEN)
    description = models.CharField(max_length=LONG_LEN,
                                   blank=True)
    image = models.ImageField(upload_to=HELPING_IMAGES_DIR,
                              default=None,
                              blank=True)

    def __str__(self):
        return f"{self.name}"


class PossibleAnswer(Common):
    quotation = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Resolution(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL,  # estou a ir buscar isto à tabela user do django
                                on_delete=models.CASCADE)
    part = models.ForeignKey('Part', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    statistics = models.JSONField(blank=True, default=dict)

    def __str__(self):
        name = " ".join([self.patient.first_name, self.patient.last_name])
        return f"{name} - {self.part.name} " \
               f"({self.date.day}/{self.date.month}/{self.date.year}, {self.date.hour}:{self.date.minute})"

    def initialize_statistics(self):
        self.statistics['total_answered'] = 0
        self.statistics['total_percentage'] = 0
        areas = Area.objects.filter(part=self.part)
        for area in areas:
            self.statistics[area.id] = {}
            self.statistics[area.id]['name'] = area.name
            self.statistics[area.id]['answered'] = 0
            self.statistics[area.id]['percentage'] = 0
            instruments = Instrument.objects.filter(area=area)
            for instrument in instruments:
                self.statistics[area.id][instrument.id] = {}
                self.statistics[area.id][instrument.id]['name'] = instrument.name
                self.statistics[area.id][instrument.id]['answered'] = 0
                self.statistics[area.id][instrument.id]['percentage'] = 0
                dimensions = Dimension.objects.filter(instrument=instrument)
                for dimension in dimensions:
                    self.statistics[area.id][instrument.id][dimension.id] = {}
                    self.statistics[area.id][instrument.id][dimension.id]['name'] = dimension.name
                    self.statistics[area.id][instrument.id][dimension.id]['answered'] = 0
                    self.statistics[area.id][instrument.id][dimension.id]['percentage'] = 0
                    sections = Section.objects.filter(dimension=dimension)
                    for section in sections:
                        self.statistics[area.id][instrument.id][dimension.id][section.id] = {}
                        self.statistics[area.id][instrument.id][dimension.id][section.id]['name'] = section.name
                        self.statistics[area.id][instrument.id][dimension.id][section.id]['answered'] = 0
                        self.statistics[area.id][instrument.id][dimension.id][section.id]['percentage'] = 0
        self.save()

    def increment_statistics(self, part_id: int, area_id: int, instrument_id: int, dimension_id: int, section_id: int):
        part = Part.objects.get(pk=part_id)
        self.statistics['total_answered'] += 1
        self.statistics['total_percentage'] = percentage \
            (total=part.number_of_questions,
             partial=self.statistics['total_answered'])

        area = Area.objects.get(pk=area_id)
        self.statistics[area_id]['answered'] += 1
        self.statistics[area_id]['percentage'] = \
            percentage(total=area.number_of_questions,
                       partial=self.statistics[area_id]['answered'])

        instrument = Instrument.objects.get(pk=instrument_id)
        self.statistics[area_id][instrument_id]['answered'] += 1
        self.statistics[area_id][instrument_id]['percentage'] = \
            percentage(total=instrument.number_of_questions,
                       partial=self.statistics[area_id][instrument_id]['answered'])

        dimension = Dimension.objects.get(pk=dimension_id)
        self.statistics[area_id][instrument_id][dimension_id]['answered'] += 1
        self.statistics[area_id][instrument_id][dimension_id]['percentage'] = \
            percentage(total=dimension.number_of_questions,
                       partial=self.statistics[area_id][instrument_id][dimension_id]['answered'])

        section = Section.objects.get(pk=section_id)
        self.statistics[area_id][instrument_id][dimension_id][section_id]['answered'] += 1
        self.statistics[area_id][instrument_id][dimension_id][section_id]['percentage'] = \
            percentage(total=section.number_of_questions,
                       partial=self.statistics[area_id][instrument_id][dimension_id][section_id]['answered'])

        self.save()


def resolution_path(instance, filename):
    return f'users/{instance.resolution.patient.id}/resolutions/{instance.resolution.id}/{filename}'


class Answer(models.Model):
    question = models.ForeignKey('Question',
                                 on_delete=models.CASCADE)
    multiple_choice_answer = models.ForeignKey('PossibleAnswer',
                                               on_delete=models.CASCADE,
                                               unique=False,
                                               blank=True, null=True)
    text_answer = models.TextField(max_length=LONG_LEN, blank=True)
    quotation = models.IntegerField(default=0, null=True, blank=True)
    notes = models.TextField(max_length=LONG_LEN, blank=True, null=True)
    resolution = models.ForeignKey('Resolution', on_delete=models.CASCADE)
    submitted_answer = models.ImageField(upload_to=resolution_path,blank=True, null=True)

    @property
    def quotation_max(self):
        return int(self.question.quotation_max)

    @property
    def quotation_min(self):
        return int(self.question.quotation_min)

    @property
    def quotation_range(self):
        return [i for i in range(self.quotation_min, self.quotation_max + 1)]

    def __str__(self):
        if self.multiple_choice_answer is not None:
            return f"{self.question.name} >> {self.multiple_choice_answer.name}"
        elif self.text_answer is not None:
            return f"{self.question.name} >> {self.text_answer[0:10]}"
        elif self.submitted_answer is not None:
            return f"{self.question.name} >> Reposta com imágem"
        else:
            return f"{self.question.name} >> Sem Resposta"
