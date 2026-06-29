import argparse
import  json
from json import JSONDecodeError
from datetime import datetime


#check and find dict keys with duplicate values in each tasks where the first task might be swimming and what if the user enter the second task with the same task name also swimming, how doi preven that 
#?? check cases of arguments, enforce it within function 

def add_task(task_desc:str):
    #!ensure everything is lowercased even for distinct characters aggressive 
    try:
        with open("tasks.json","r") as task_file:
            data = json.load(task_file) 
        #?the key is a str, need to convert to int to compute the next id 
            nums = [int(tid) for tid in data]

        #?check if the nums has existing numbers, if not reset uid to 1 
        #?Need to convert back to string as JSON keys are strings after calcualtion of the next number 
            if nums:
                uid = str(len(nums) + 1)
            else:
                uid = "1" 

    except FileNotFoundError: #?firsst task approach here, NOT AN ERROR, expected situation
        data = {}
        uid = 1 
        #?local handling for first task 

    now = datetime.now().isoformat(sep = " ")

    #?check and find dict kets with duplciate values, we wanna check the values,

    unique_desc = [vals["description"] for vals in data.values()] #?extract from actual dict, added tasks descriptions


    if task_desc not in unique_desc:
        #?task identifiable by ID 
        #? populating
        print("Adding task....")

        data[uid] = {
            "description": task_desc,
            "status":"todo",
            "createdAt": now,
            "updatedAt": now
        }

        #?Write the entire updated list back to the file, alwasy writing the full list back,searlize it 
        with open("tasks.json","w") as wf:
            #?write it back to JSON obj 
            json.dump(data,wf,indent=4)
    
    else:
        raise ValueError("Duplication of tasks is not allowed")

#!when user fill in invalid id, enforce it
#!maybe add status option
def update_task(tid: str,task_desc: str):
    with open("tasks.json","r") as ut:
        all_data = json.load(ut) #? dicts of dicts

        valid_ids = [key for key in all_data if key == tid]
        if tid not in valid_ids:
            #!propograte up the call stack 
            raise IndexError(f"Task with ID {tid} does not exists")
        
        for values in all_data.values():
            values["description"] = task_desc
    
    #?write the wholestructure back 
    with open("tasks.json","w") as wf:
        json.dump(all_data,wf,indent=4)


#!id should be unique and stable, do not change the ids of other tasks after deletio to avoid confusion for other functionalities
#?do not expect the user enters the id 
def delete_task(task_id:str):
    with open("tasks.json") as dt:
        data = json.load(dt) #!dicts of dicts 

        aid = [key for key in data if key == task_id]
        if task_id not in aid:
            raise IndexError(f"Deletion not possible as Task with ID {task_id} does not exist")
        
        for id in aid:
            del data[id]

    #?Overwriting it 
    with open("tasks.json","w") as sf:
        json.dump(data,sf,indent=4)

#?the list created a separate object, static copy
#?the status option is enforced in paarsing before every entering this function 
#!what if the task to be marked does not exists,what happen, think 
def marking_status_task(tid:str, status:str):
    #?Be specific i guess

    with open("tasks.json","r") as rf:
        data = json.load(rf)

        for task_id, desc_vals in data.items():
            if task_id == tid:
                desc_vals["status"] = status

    with open("tasks.json","w") as ws:
        json.dump(data,ws,indent=4)



#?internal logic
#?shold be dynamic
#?the parsing handles if the user typed the correct arguments
#?the validation checks if what the user typed currently exists in the database itself, subtle difference 
def task_listing_based_on_status(status: str) :
    with open("tasks.json") as fw:
        data = json.load(fw)        
        tasks = [vals for vals in data.values() if vals["status"] == status] #!output the task that satisfy the status provided 

        #!this means if the status the user provide is absent or does not exists , 
        if not tasks:
            print(f"There are currently no task with status --> {status}")
            return 
        
        for task in tasks:
            print(f"Status: {task['status']} --> {task['description']}")
        

if __name__ == "__main__":
    #!only execute when executed directly on this file 
    #?top level parser
    #?dest is the name of the attribute under which subcommand name will be stored 
    #?Splitting up functionality 
    parser = argparse.ArgumentParser(description="task-cli")
    sub_parsers = parser.add_subparsers(dest="subcommands") #! store the subcommand name into args.subcommands

    #?Create the parse for the "add" command 
    #?generate ID automatically 
    parser_add = sub_parsers.add_parser("add",help="Add a task") #?command 
    parser_add.add_argument("task", help="description of the task",type =  str.lower) #? positional args, convert as early as possible in the command line 

    #?Create the parser for the "update" command
    parser_update = sub_parsers.add_parser("update",help="Update a task") #?command
    parser_update.add_argument("id", help="ID of task to update") 
    parser_update.add_argument("description",help= "description of the new task") #?args
    #?some logic will invovle here when user type this command 

    #?Create the parser for the "delete command"
    parser_delete = sub_parsers.add_parser("delete",help="delete a task") #?command 
    parser_delete.add_argument("id",help="The task id to delete") #?args
    #?some logic will invovle here when user type this command 

    #?Create the parse for the mark in progress task
    #?on off flags 
     
    parser_mark = sub_parsers.add_parser("mark",help="Markinig a task as in progress or done") #command 
    parser_mark.add_argument("id",help="Task id to mark") #? the id has to be a string 
    parser_mark.add_argument("status", choices = ("in progress","done","todo"), help="Either mark it as in progress or done") #?flags

    
    #?Create the parser for the "list" command
    parser_list = sub_parsers.add_parser('list',help="list available tasks") #command
    parser_list.add_argument("status", choices = ("in progress","done","todo"), help="Task filtered by status")

    args = parser.parse_args()
    
    try:
        if args.subcommands == "add":
            add_task(args.task)
            print(f"Task named {args.task} added ")
    
        elif args.subcommands == "update":
            update_task(args.id,args.description)
            print(f"Task {args.id} updated successfully")

        elif args.subcommands == "delete":
            delete_task(args.id)
            print(f"Task {args.id} deleted")
    
        elif args.subcommands == "mark":
            marking_status_task(args.id,args.status)
            print(f"Task {args.id} changed to {args.status}")
    
        elif args.subcommands == "list":
            task_listing_based_on_status(args.status)

#!if the user request a status that did not populate inside the JSON file
    
    except JSONDecodeError as jsonerr: 
        print(f"{jsonerr}: The file being loaded is invalid JSON and corrupted")
    
    except Exception as err: #?all other exceptions from bugs in code 
        print(f"Error: {err}")