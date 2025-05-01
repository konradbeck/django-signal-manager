import logging
from unittest.mock import MagicMock

import pytest
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save

from django_signal_manager.managers import SignalManager


class MockModel:
    """
    A mock model class to simulate Django model instances.

    This class is used in the tests to mimic the behavior of a Django model instance
    without needing to interact with an actual database.
    """

    def __init__(self, pk=None):
        self.pk = pk


@pytest.fixture
def signal_manager():
    """
    Fixture that provides a SignalManager instance for the tests.

    This ensures a new instance of SignalManager is available for each test case.
    """
    return SignalManager()


@pytest.fixture
def mock_instance():
    """
    Fixture that provides a mock instance of MockModel for testing.

    This creates a mock model instance that can be passed into the SignalManager's methods.
    """
    return MockModel()


def test_run_pre_save_new(signal_manager, mock_instance):
    signal_manager.pre_create = MagicMock()
    signal_manager.run(MockModel, mock_instance, signal=pre_save)
    signal_manager.pre_create.assert_called_once_with(mock_instance, signal=pre_save)


def test_run_pre_save_update(signal_manager, mock_instance):
    mock_instance.pk = 1
    signal_manager.pre_update = MagicMock()
    signal_manager.run(MockModel, mock_instance, signal=pre_save)
    signal_manager.pre_update.assert_called_once_with(mock_instance, signal=pre_save)


def test_run_post_save_new(signal_manager, mock_instance):
    signal_manager.post_create = MagicMock()
    signal_manager.run(MockModel, mock_instance, signal=post_save, created=True)
    signal_manager.post_create.assert_called_once_with(
        mock_instance, signal=post_save, created=True
    )


def test_run_post_save_update(signal_manager, mock_instance):
    signal_manager.post_update = MagicMock()
    signal_manager.run(MockModel, mock_instance, signal=post_save, created=False)
    signal_manager.post_update.assert_called_once_with(
        mock_instance, signal=post_save, created=False
    )


def test_run_pre_delete(signal_manager, mock_instance):
    signal_manager.pre_delete = MagicMock()
    signal_manager.run(MockModel, mock_instance, signal=pre_delete)
    signal_manager.pre_delete.assert_called_once_with(mock_instance, signal=pre_delete)


def test_run_post_delete(signal_manager, mock_instance):
    signal_manager.post_delete = MagicMock()
    signal_manager.run(MockModel, mock_instance, signal=post_delete)
    signal_manager.post_delete.assert_called_once_with(
        mock_instance, signal=post_delete
    )


def test_run_unknown_signal(signal_manager, mock_instance, caplog):
    unknown_signal = "unknown_signal"
    with caplog.at_level(logging.WARNING):
        signal_manager.run(MockModel, mock_instance, signal=unknown_signal)
    assert f"Unknown or missing signal in kwargs: {unknown_signal}" in caplog.text


def test_default_pre_create(signal_manager, mock_instance):
    signal_manager.pre_create(mock_instance)


def test_default_post_create(signal_manager, mock_instance):
    signal_manager.post_create(mock_instance)


def test_default_pre_update(signal_manager, mock_instance):
    signal_manager.pre_update(mock_instance)


def test_default_post_update(signal_manager, mock_instance):
    signal_manager.post_update(mock_instance)


def test_default_pre_delete(signal_manager, mock_instance):
    signal_manager.pre_delete(mock_instance)


def test_default_post_delete(signal_manager, mock_instance):
    signal_manager.post_delete(mock_instance)
