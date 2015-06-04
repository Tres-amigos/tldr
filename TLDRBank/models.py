from accounts import models
from TLDRBank import manager
import uuid

import hmac
from django.conf import settings

class Transfer(models.Transfer):
    objects = manager.PostingManager()

    def _generate_reference(self):
        #obj = hmac.new(key=str.encode(settings.SECRET_KEY),
        #               msg=self.id)
        return uuid.uuid4()

    class Meta:
        proxy = True
