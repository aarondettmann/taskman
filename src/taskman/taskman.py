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
from pathlib import Path
import argparse
import os
import sys

import pandas as pd


PROG_NAME = "taskman"
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
        task['created'] = str(datetime.now())
        self.df_tasks.loc[len(self.df_tasks)] = task

    def mark_task_done(self, index):
        if self.df_tasks.loc[index, 'finished'] is not None:
            print(f"task '{self.df_tasks.loc[index, 'descr']}' already finished...")
            return

        self.df_tasks.loc[index, 'finished'] = str(datetime.now())
        print(f"task '{self.df_tasks.loc[index, 'descr']}' done...")

    def delete_task(self, index):
        self.df_tasks = self.df_tasks.drop(index=index)

    def sort_by_due_date():
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

        def get_timedelta(date_str):
            if pd.isna(date_str):
                return None

            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
            delta = datetime.now() - date_obj

            days = delta.days
            seconds = delta.seconds
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{days} d, {hours} h, {minutes} m"

        # Dates
        f.loc[:, 'created'] = f['created'].apply(get_timedelta)
        f.loc[:, 'finished'] = f['finished'].apply(get_timedelta)

        print(f.to_markdown())


def cli():
    """Command line interface"""

    parser = argparse.ArgumentParser(prog=f'{PROG_NAME}')
    subparsers = parser.add_subparsers(help='execution modes', dest='exec_mode')

    # ----- Mode 'list' -----
    sub = subparsers.add_parser('list', help='list tasks')
    sub.add_argument('type', metavar='TYPE', nargs='?', type=str, help='todo or done', default="todo")
    sub.add_argument('--project', '-p', metavar='PROJECT', type=str, help='project')
    sub.add_argument('--tags', '-t', metavar='TAGS', nargs='+', type=str, help='tags')

    # ----- Mode 'add' -----
    sub = subparsers.add_parser('add', help='create a new todo item')
    sub.add_argument("descr", metavar='DESCRIPTION', help="a description of the task", type=str)
    sub.add_argument('--project', '-p', metavar='PROJECT', type=str, help='project')
    sub.add_argument('--tags', '-t', metavar='TAGS', nargs='+', type=str, help='tags')

    # ----- Mode 'done' -----
    sub = subparsers.add_parser('done', help='mark task as done')
    sub.add_argument('index', metavar='TASK NUMBER', type=int, help='task index', default=1)

    # ----- Mode 'modify' -----
    # TODO

    # ----- Mode 'delete' -----
    sub = subparsers.add_parser('delete', help='delete task from database')
    sub.add_argument('index', metavar='TASK NUMBER', type=int, help='task index', default=1)

    args = parser.parse_args()

    tm = TaskManager()

    # MODE: list
    if args.exec_mode == 'list':
        tags = args.tags if isinstance(args.tags, list) else []
        tm.print_list(
            args.type,
            filter_project=args.project,
            filter_tags=tags
        )

    # MODE: add
    elif args.exec_mode == 'add':
        tm.add_task({
            "descr": args.descr,
            "project": args.project,
            "tags": args.tags
        })
        tm.save()

    # MODE: done
    elif args.exec_mode == 'done':
        tm.mark_task_done(args.index)
        tm.save()

    # MODE: remove
    elif args.exec_mode == 'delete':
        tm.delete_task(args.index)
        tm.save()

    else:
        parser.print_help()


if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        sys.exit(1)
