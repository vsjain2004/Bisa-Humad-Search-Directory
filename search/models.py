""" Search Directory for the Bisa Humad Jain Samaj
    Copyright (C) 2021  Varun Jain

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

# Create your models here.
class People(models.Model):
    class Mar(models.TextChoices):
        MARRIED = 'MR', _('Married')
        UNMARRIED = 'UM', _('Unmarried')
        DIVORCEE = 'DE', _('Divorcee')
        WIDOWER = 'WR', _('Widower')
        WIDOW = 'WW', _('Widow')

    class G(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')

    SurName = models.TextField()
    Name = models.TextField()
    MiddleName = models.TextField(blank=True, null=True)
    DOB = models.DateField(blank=True, null=True)
    Age = models.PositiveIntegerField(default=0)
    Gender = models.CharField(max_length=1, choices=G.choices, default=G.MALE)
    MaritalStatus = models.CharField(max_length=2, choices=Mar.choices, default=Mar.UNMARRIED)
    FamilyNo = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    Head = models.BooleanField(default=False)

    def __str__(self):
        if self.MiddleName == '':
            return f"{self.Name} {self.SurName}"
        else:
            return f"{self.Name} {self.MiddleName} {self.SurName}"

    def serialize(self):
        for p in People.G.choices:
            if self.Gender in list(p):
                break
        s = p[1]
        for p in People.Mar.choices:
            if self.MaritalStatus in list(p):
                f = p[1]
        if self.DOB:
            v = self.DOB.strftime('%d/%m/%Y')
        else:
            v = self.DOB
        return {
            "id": self.id,
            "SurName": self.SurName,
            "Name": self.Name,
            "MiddleName": self.MiddleName,
            "DOB": v,
            "Age": self.Age,
            "Gender": s,
            "MaritalStatus": f,
            "Head": self.Head,
            "FamilyNo": self.FamilyNo
        }