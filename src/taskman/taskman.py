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
import sys

import pandas as pd

from util import P, now, timedelta_since, timedelta_until


FILE_TASKS = Path(os.path.expanduser(("~/.taskman.json")))


def datetime_string(string):
    try:
        return datetime.fromisoformat(string).isoformat()
    except (TypeError, ValueError) as e:
        P.error(f"invalid due date {string!r}. exit...")
        sys.exit(1)


class TaskManager:
    """A simple todo manager"""

    def __init__(self):
        # Pandas dataframe
        cols = ['descr', 'project', 'tags', 'due', 'created', 'finished']
        self.tasks = pd.DataFrame(columns=cols)

        if not FILE_TASKS.is_file() or FILE_TASKS.stat().st_size==0:
            self.save()
        else:
            self.tasks = pd.concat([self.tasks, pd.read_json(FILE_TASKS)], ignore_index=True)

    def save(self):
        self.tasks.to_json(FILE_TASKS, orient='records', indent=4)

    def add_task(self, task_dict):
        P.info(f"adding task {task_dict['descr']!r}...")
        task_dict['created'] = now()

        if task_dict['due']:
            task_dict['due'] = datetime_string(task_dict['due'])

        index = len(self.tasks)
        self.tasks.loc[index] = task_dict
        P.info("\n" + self.tasks.iloc[index].to_markdown())

    def mark_task_done(self, index):
        if not (len(self.tasks) > index):
            P.error(f"task {index} does not exist...")
            sys.exit(1)

        if not pd.isna(self.tasks.loc[index, 'finished']):
            P.error(f"task {self.tasks.loc[index, 'descr']!r} already finished...")
            sys.exit(1)

        self.tasks.loc[index, 'finished'] = now()
        P.info(f"task {self.tasks.loc[index, 'descr']!r} done...")

    def delete_task(self, index):
        try:
            P.warning(f"deleting task {index} {self.tasks.loc[index, 'descr']!r}...")
            P.warning("\n" + self.tasks.loc[index].to_markdown() + "\n")
            self.tasks = self.tasks.drop(index=index)
        except KeyError:
            P.warning(f"task {index} does not exist")

    def delete_tasks(self, indices):
        for index in indices:
            self.delete_task(index)

    def modify_task(self, index, task_dict):
        P.info(f"modifying task {index}...")
        P.warning("\n" + self.tasks.iloc[index].to_markdown())

        for key in ['descr', 'project', 'tags']:
            if task_dict[key]:
                self.tasks.loc[index, key] = task_dict[key]

        if task_dict['due']:
            self.tasks.loc[index, 'due'] = string2datetime(task_dict['due'])


        P.info("\n" + self.tasks.iloc[index].to_markdown())

    def sort_by_due_date(self):
        raise NotImplementedError

    def print_list(self, task_type, filter_project="", filter_tags=[]):
        f = None
        if task_type == "todo":
            f = self.tasks[self.tasks['finished'].isna()]
            f = f.drop(['finished'], axis=1)
        elif task_type == "done":
            f = self.tasks[self.tasks['finished'].notna()]
            f.loc[:, 'finished'] = f['finished'].apply(timedelta_since)
        else:
            P.error(f"invalid task type {task_type!r}")
            sys.exit(1)

        # Project
        if filter_project:
            f = f[f['project'] == filter_project]

        # Tags
        for tag in filter_tags:
            f = f[f['tags'].apply(lambda x: x is not None and tag in x)]

        # Dates
        f.loc[:, 'created'] = f['created'].apply(timedelta_since)
        f.loc[:, 'due'] = f['due'].apply(timedelta_until)

        P.info(f.to_markdown())
