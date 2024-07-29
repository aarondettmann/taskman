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

# Author: Aaron Dettmann


from datetime import datetime
from uuid import uuid4


class Task:

    def __init__(self, descr, tags=None, project=None, due=None):
        self.descr = descr
        self.tags = tags
        self.project = project
        self.due = due

        self._time_created = datetime.now()
        self._uuid = uuid4()

    @property
    def uuid(self):
        return self._uuid

    @property
    def time_created(self):
        return self._time_created


class TaskManager:

    def __init__(self, todo=[], done=[]):
        self.tasks_todo = todo
        self.tasks_done = done

    @classmethod
    def load_from_file(file):
        raise NotImplementedError

    def add_todo(self, task):
        self.tasks_todo.append(task)

    def remove_todo(self, number):
        if number < 0 or number > len(self.tasks_todo)-1:
            raise ValueError("invalid task number")

        done = self.tasks_todo.pop(number)
        self.tasks_done.append(done)

    def sort_by_due_date():
        raise NotImplementedError

    def list_tasks_todo(self):
        out = ""
        for i, task in enumerate(self.tasks_todo):
            out += f"{i:2d}: {task.descr:30s} {task.time_created} ({task.uuid})\n"

        return out

    def list_tasks_done(self):
        out = ""
        for i, task in enumerate(self.tasks_done):
            out += f"{i:2d}: {task.descr:30s} {task.time_created} ({task.uuid})\n"

        return out


if __name__ == '__main__':
    tm = TaskManager()

    tm.add_todo(Task("buy groceries"))
    tm.add_todo(Task("feed cat"))
    tm.add_todo(Task("clean kitchen"))

    print("-----")

    print(tm.list_tasks_todo())
    tm.remove_todo(1)

    print("-----")

    print(tm.list_tasks_todo())

    print("-----")

    print(tm.list_tasks_done())
