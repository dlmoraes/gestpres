#coding=utf-8
import PIL
from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse_lazy
from django.utils.six import StringIO

from io import BytesIO

from core.models import ControleTemporal

class Perfil(ControleTemporal):
    user = models.OneToOneField(User, related_name='profile')
    pessoa = models.ForeignKey('cat.Pessoa', related_name='pes_user', null=True, blank=True)
    empresa = models.ForeignKey('cag.Empresa', related_name='emp_user')
    regional = models.ForeignKey('cag.Regional', related_name='reg_user', null=True, blank=True)
    baseregional = models.ForeignKey('cag.BaseRegional', related_name='basereg_user', null=True, blank=True)
    avatar = models.ImageField(upload_to='images/usuario/perfil',
                               null=True,
                               default='images/usuario/no-image.jpg')

    class Meta:
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    def get_absolute_url(self):
        return reverse_lazy('accounts:alterar_avatar', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.avatar != None:
                largura_base = 300
                img = Image.open(self.avatar)
                exif = None

                if 'exif' in img.info:
                    exif = img.info['exif']
                percentual_largura = (largura_base / float(img.size[0]))
                altura = int((float(img.size[1]) * float(percentual_largura)))
                img = img.resize((largura_base, altura), PIL.Image.ANTIALIAS)
                saida = BytesIO()
                if exif:
                    img.save(saida, format='JPEG', exif=exif, quality=90)
                else:
                    img.save(saida, format='JPEG', quality=90)
                saida.seek(0)
                self.avatar = InMemoryUploadedFile(saida,
                                                   'ImageField',
                                                   "%s.jpg" % self.avatar.name,
                                                   'image/jpeg',
                                                    None,
                                                   None)
            else:
                self.avatar = None
        super(Perfil, self).save(*args, **kwargs)