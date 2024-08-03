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

import argparse
import sys

from __init__ import PROG_NAME
from taskman import TaskManager


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
    sub.add_argument('indices', metavar='TASK NUMBER', nargs='+', type=int, help='task index (multiple allowed)')

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
        tm.delete_tasks(args.indices)
        tm.save()

    else:
        parser.print_help()


if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        sys.exit(1)
