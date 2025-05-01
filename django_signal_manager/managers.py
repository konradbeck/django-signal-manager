import logging
from typing import Any

from django.db.models import Model
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save

logger = logging.getLogger(__name__)


class SignalManager:
    """
    A base class for handling Django model signals.

    This class provides methods to handle Django signals related to model creating,
    updating, and deleting. It determines the appropriate handler based on the
    signal type and invokes the corresponding method.
    """

    def run(self, sender: type, instance: Model, **kwargs: Any) -> None:
        """
        Determines the signal type and calls the appropriate handler method.

        Based on the received signal (pre_save, post_save, pre_delete, post_delete),
        this method routes the execution to the appropriate handler method for either
        a new or existing instance.

        Args:
            sender (type): The model class that sent the signal.
            instance (Model): The instance of the model that is being processed.
            **kwargs (dict): Additional keyword arguments from the signal, such as the
                             signal itself and properties like 'created' for post_save.
        """
        signal_object = kwargs.get("signal")

        if signal_object == pre_save:
            if instance.pk is None:
                self.pre_create(instance, **kwargs)
            else:
                self.pre_update(instance, **kwargs)
        elif signal_object == post_save:
            if kwargs.get("created", False):
                self.post_create(instance, **kwargs)
            else:
                self.post_update(instance, **kwargs)
        elif signal_object == pre_delete:
            self.pre_delete(instance, **kwargs)
        elif signal_object == post_delete:
            self.post_delete(instance, **kwargs)
        else:
            logger.warning("Unknown or missing signal in kwargs: %s", signal_object)

    def pre_create(self, instance: Model, **kwargs: Any) -> None:
        """
        Handler called before a new instance is created.

        Args:
            instance (Model): The model instance about to be created.
            **kwargs (dict): Additional keyword arguments from the signal.
        """
        pass

    def post_create(self, instance: Model, **kwargs: Any) -> None:
        """
        Handler called after a new instance is created.

        Args:
            instance (Model): The model instance that was created.
            **kwargs (dict): Additional keyword arguments from the signal.
        """
        pass

    def pre_update(self, instance: Model, **kwargs: Any) -> None:
        """
        Handler called before an existing instance is updated.

        Args:
            instance (Model): The model instance about to be updated.
            **kwargs (dict): Additional keyword arguments from the signal.
        """
        pass

    def post_update(self, instance: Model, **kwargs: Any) -> None:
        """
        Handler called after an existing instance is updated.

        Args:
            instance (Model): The model instance that was updated.
            **kwargs (dict): Additional keyword arguments from the signal.
        """
        pass

    def pre_delete(self, instance: Model, **kwargs: Any) -> None:
        """
        Handler called before an instance is deleted.

        Args:
            instance (Model): The model instance about to be deleted.
            **kwargs (dict): Additional keyword arguments from the signal.
        """
        pass

    def post_delete(self, instance: Model, **kwargs: Any) -> None:
        """
        Handler called after an instance is deleted.

        Args:
            instance (Model): The model instance that was deleted.
            **kwargs (dict): Additional keyword arguments from the signal.
        """
        pass
