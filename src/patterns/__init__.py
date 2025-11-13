"""Design pattern implementations."""
from .resource_factory import ResourceFactory
from .resource_decorator import ResourceDecorator, LoggingDecorator

__all__ = ['ResourceFactory', 'ResourceDecorator', 'LoggingDecorator']
