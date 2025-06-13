#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nlxpy.dl.models.model
========

Desc: Model factory and register for deep learning models.
Author: Neolux Lee
Date: 2025-06-13
Email: neolux_lee@outlook.com
Ver: 0.0.1
"""
import os
from typing import Callable


MODULE_REGISTRY: dict = {}


class Model:
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def register(cls, name:str) -> Callable:
        """Register the model with a given name."""

        def register_model(mcls):
            if name in MODULE_REGISTRY:
                raise ValueError(f"Model '{name}' is already registered.")
            MODULE_REGISTRY[name] = mcls
            return cls

        return register_model

    @classmethod
    def unregister(cls, name: str) -> Callable:
        """Unregister the model with a given name."""

        def unregister_model():
            if name not in MODULE_REGISTRY:
                raise ValueError(f"Model '{name}' is not registered.")
            del MODULE_REGISTRY[name]
            return cls

        return unregister_model


if __name__ == "__main__":
    # Example usage
    @Model.register("example_model")
    class ExampleModel(Model):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            print("ExampleModel initialized.")

    print(f"Current registered models: {MODULE_REGISTRY.keys()}")

    # Access the registered model
    model_instance = MODULE_REGISTRY["example_model"]()
    print(f"Registered model: {model_instance.__class__.__name__}")

    # Unregister the model
    Model.unregister("example_model")
    print("Model 'example_model' unregistered.")

    print(f"Current registered models: {MODULE_REGISTRY.keys()}")
