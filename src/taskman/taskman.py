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
from pathlib import Path
import os

import pandas as pd

from util import P, get_timedelta


FILE_TASKS = Path(os.path.expanduser(("~/.taskman.json")))


class TaskManager:
    """A simple todo manager"""

    def __init__(self):
        cols = ['descr', 'project', 'tags', 'due', 'created', 'finished']
        self.df_tasks = pd.DataFrame(columns=cols)

        if not FILE_TASKS.is_file() or FILE_TASKS.stat().st_size==0:
            self.save()
        else:
            self.df_tasks = pd.concat([self.df_tasks, pd.read_json(FILE_TASKS)], ignore_index=True)

    def save(self):
        self.df_tasks.to_json(FILE_TASKS, orient='records', indent=4)

    def add_task(self, task):
        P.info(f"adding task '{task['descr']}'...")
        task['created'] = str(datetime.now())
        index = len(self.df_tasks)
        self.df_tasks.loc[index] = task
        print(self.df_tasks.iloc[index].to_markdown())

    def mark_task_done(self, index):
        if self.df_tasks.loc[index, 'finished'] is not None:
            P.error(f"task '{self.df_tasks.loc[index, 'descr']}' already finished...")
            return

        self.df_tasks.loc[index, 'finished'] = str(datetime.now())
        P.info(f"task '{self.df_tasks.loc[index, 'descr']}' done...")

    def delete_task(self, index):
        try:
            P.warning(f"deleting task {index} '{self.df_tasks.loc[index, 'descr']}'...")
            self.df_tasks = self.df_tasks.drop(index=index)
        except KeyError:
            P.warning(f"task {index} does not exist")

    def delete_tasks(self, indices):
        for index in indices:
            self.delete_task(index)

    def modify_task(self):
        raise NotImplementedError

    def sort_by_due_date(self):
        raise NotImplementedError

    def print_list(self, task_type, filter_project="", filter_tags=[]):
        if task_type == "todo":
            f = self.df_tasks[self.df_tasks['finished'].isna()]
        elif task_type == "done":
            f = self.df_tasks[self.df_tasks['finished'].notna()]

        # Project
        if filter_project:
            f = f[f['project'] == filter_project]

        # Tags
        for tag in filter_tags:
            f = f[f['tags'].apply(lambda x: x is not None and tag in x)]

        # Dates
        f.loc[:, 'created'] = f['created'].apply(get_timedelta)
        f.loc[:, 'finished'] = f['finished'].apply(get_timedelta)

        print(f.to_markdown())
