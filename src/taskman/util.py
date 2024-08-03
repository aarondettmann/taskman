#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2024 Aaron Dettmann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

from datetime import datetime

from rich.console import Console
from rich.text import Text
import pandas as pd


class P:
    console = Console()

    @staticmethod
    def _print(string, color):
        text = Text()
        text.append(string, style=f"{color}")
        __class__.console.print(text)

    @staticmethod
    def info(string):
        __class__._print(string, "blue")

    @staticmethod
    def warning(string):
        __class__._print(string, "yellow")

    @staticmethod
    def error(string):
        __class__._print(string, "red")


def get_timedelta(date_str):
    if pd.isna(date_str):
        return None

    date_obj = datetime.fromisoformat(date_str)
    delta = datetime.now() - date_obj

    days = delta.days
    seconds = delta.seconds
    hours, remainder = divmod(seconds, 3600)
    return f"{days} d, {hours} h"
