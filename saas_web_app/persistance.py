from django.db import models
from typing import ClassVar, TypeVar, Generic

T = TypeVar('T', bound='BaseModel')

class BaseModel(models.Model, Generic[T]):
    id = models.AutoField(primary_key=True)
    
    objects: ClassVar[models.Manager[T]]

    class Meta:
        abstract = True

