# Django Signal Manager Framework

This package provides a base class, `SignalManager`, for simplifying the handling of Django model signals. It streamlines the process of responding to `pre_save`, `post_save`, `pre_delete`, and `post_delete` signals by categorizing them into more specific methods.

## Installation

You can install this framework using pip:

```bash
pip install django-signal-manager
```

## Usage

Create a subclass of `SignalManager`:

```python
import logging
from django.db.models import Model
from signal_manager import SignalManager
from your_app.models import MyModel

logger = logging.getLogger(__name__)

class MyModelSignalManager(SignalManager):
    def pre_create(self, instance: Model, **kwargs: Any) -> None:
        logger.info(f"Pre-create: {instance}")
        # Add your logic here

    def post_create(self, instance: Model, **kwargs: Any) -> None:
        logger.info(f"Post-create: {instance}")
        # Add your logic here

    def pre_update(self, instance: Model, **kwargs: Any) -> None:
        logger.info(f"Pre-update: {instance}")
        # Add your logic here

    def post_update(self, instance: Model, **kwargs: Any) -> None:
        logger.info(f"Post-update: {instance}")
        # Add your logic here

    def pre_delete(self, instance: Model, **kwargs: Any) -> None:
        logger.info(f"Pre-delete: {instance}")
        # Add your logic here

    def post_delete(self, instance: Model, **kwargs: Any) -> None:
        logger.info(f"Post-delete: {instance}")
        # Add your logic here
```

Connect the signal manager to your model:

```python
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from your_app.models import MyModel
from .signal_managers import MyModelSignalManager

manager = MyModelSignalManager()

@receiver(pre_save, sender=MyModel)
@receiver(post_save, sender=MyModel)
@receiver(pre_delete, sender=MyModel)
@receiver(post_delete, sender=MyModel)
def my_model_signals(sender, instance, **kwargs):
    manager.run(sender, instance, **kwargs)
```

## Class Overview

### `SignalManager`

- **`run(sender: type, instance: Model, **kwargs: Any) -> None`**: 
  - Determines the signal type and dispatches to the appropriate handler method.
- **`pre_create(instance: Model, **kwargs: Any) -> None`**: 
  - Handler for `pre_save` when a new instance is being created.
- **`post_create(instance: Model, **kwargs: Any) -> None`**: 
  - Handler for `post_save` when a new instance is created.
- **`pre_update(instance: Model, **kwargs: Any) -> None`**: 
  - Handler for `pre_save` when an existing instance is being updated.
- **`post_update(instance: Model, **kwargs: Any) -> None`**: 
  - Handler for `post_save` when an existing instance is updated.
- **`pre_delete(instance: Model, **kwargs: Any) -> None`**: 
  - Handler for `pre_delete`.
- **`post_delete(instance: Model, **kwargs: Any) -> None`**: 
  - Handler for `post_delete`.

## Benefits

- **Organization**: Separates signal handling logic into distinct methods, improving code readability and maintainability.
- **Clarity**: Makes it clear which signal is being handled (create vs. update).
- **Reusability**: The base class can be extended for different models, reducing code duplication.
- **Logging**: Includes basic logging for unknown or missing signals.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.
