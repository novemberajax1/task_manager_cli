# Task_tracker

A command line task manager

## Functionalities

- Add a task
- Update a task, change the description of the task
- Mark a task done or in progress
- delete a task by ID
- List task based on status

## Usage

- Add a task -- add -h description
- Updating a task -- update [-h] id  description
= Deleting a task -- delete [-h] id
- Marking a task its statuses -- mark [-h] id {in progress, done, todo}
- listing task based on statuses -- list [-h] {in progress, done,todo}

## Running it

```bash
python3 taskcli.py add Groceries
python3 taskcli.py add "Refill water for baby"
python3 taskcli.py update 2 Swimming
python3 taskcli.py delete 5
python3 taskcli.py mark 4 "in progress"
python3 taskcli.py mark 8 done 
python3 taskcli.py list done 
```
