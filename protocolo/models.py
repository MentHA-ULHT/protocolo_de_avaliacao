from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

SMALL_LEN = 50
MEDIUM_LEN = 150
LONG_LEN = 500


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
    image = models.ImageField


class PossibleAnswer(Common):
    quotation = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Answer(models.Model):
    question = models.ForeignKey('Question',
                                 on_delete=models.CASCADE)
    multiple_choice_answer = models.ForeignKey('PossibleAnswer',
                                               on_delete=models.CASCADE,
                                               unique=False,
                                               blank= True)
    submitted_answer = models.ImageField
    text_answer = models.TextField(max_length=LONG_LEN, blank=True)
    quotation = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.question.name} >> {self.multiple_choice_answer.name}"


class Resolution(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL,  # estou a ir buscar isto à tabela user do django
                                on_delete=models.CASCADE)
    part = models.ForeignKey('Part', on_delete=models.CASCADE)
    answers = models.ManyToManyField('Answer',
                                     default=None,
                                     related_name='answers',
                                     blank=True)
    date = models.DateTimeField(default=timezone.now)

    #statistics = models.JSONField(encoder='utf-8')  # verifica se enconder garante q tens ç, é, etc...

    def __str__(self):
        name = " ".join([self.patient.first_name, self.patient.last_name])
        return f"{name} - {self.part.name} " \
               f"({self.date.day}/{self.date.month}/{self.date.year}, {self.date.hour}:{self.date.minute})"

    #def __int__(self):
     #   self.estatisticas = {}
      #  self.estatisticas['answered'] = 0
        # parte.areas is a QuerySet of objects
       # for area in parte.areas:
        #    self.estatisticas[area.id] = {}
         #   self.estatisticas[area.id]['answered'] = 0
          #  for dimension in area.dimension_set:
           #     self.estatisticas[area][dimensao] = {}
            #    self.estatisticas[dimensao]['answered'] = 0
             #   for instrumento in dimensao.instrumentos:
              #      self.estatisticas[area][dimensao] = {}
               #     self.estatisticas[area][dimensao][instrumento]['answered'] = 0
                #    for seccao in instrumento.seccoes:
                 #       self.estatisticas[area][dimensao][instrumento][seccao] = {}
                  #      self.estatisticas[area][dimensao][instrumento][seccao]['answered'] = 0
                   #     for pergunta in seccao.perguntas:
                    #        self.estatisticas[area][dimensao][instrumento][seccao][pergunta]['answered'] = 0
        #self.save()


