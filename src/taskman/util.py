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
        __class__._print(string, "green")

    @staticmethod
    def warning(string):
        __class__._print(string, "yellow")

    @staticmethod
    def error(string):
        __class__._print(string, "red")


def now():
    """Return current date and time as string (iso format)"""

    return datetime.now().isoformat()


def timedelta(start_date, end_date):
    """
    Return a human-readable time delta

    Args:
        :start_date: start date as string (iso format)
        :end_date:   end date as string (iso format)

    Returns:
        Time delta as string '<days> d, <hours> h'
    """

    if pd.isna(start_date) or pd.isna(end_date):
        return None

    start_date = datetime.fromisoformat(start_date)
    end_date   = datetime.fromisoformat(end_date)

    delta = end_date - start_date

    days = delta.days
    hours = delta.seconds // 3600
    return f"{days} d, {hours} h"


def timedelta_until(until):
    return timedelta(now(), until)


def timedelta_since(since):
    return timedelta(since, now())
