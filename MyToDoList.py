
# this class imported from the datetime module will allow us to handle and format dates and times
from datetime import datetime
# this class imported from the datetime module will help us determine the difference in time
from datetime import timedelta
# this class imported from the datetime module can help us pause the time in order to help us calculate the duration
import time

# 2 lists to be used for storing completed and incomplete tasks and sorting them out
completed_tasks = []
incomplete_tasks = []

# dictionaries we will be using for the deadline and notes
notes_dict = {}
deadline_dict = {}


# introduction message

print("Here is our To Do List! Let us help you organize because no one likes missing things!")

# dictionary meant for storing the importance order and important variables
order_dict = {}
place = 0
print("Lets get you started! Just type 'No More' to stop")


# function that adds things to the list
def to_do():
	global place
	global order_dict

	while True:
		val = input("What do you want to add? ")
		if val == 'No More':
			break
		place += 1
		order_dict[place] = val

	return order_dict

#The following function will help us determine the deadline for given assignments 
def deadlines(): 
	for task in order_dict.items():
		while True:
			due_input = input(f"When is '{task}' due? Military time please! (e.g., 14:30): ")
			try:
				due_time = datetime.strptime(due_input, "%H:%M").time()
				now = datetime.now()
				due_datetime = datetime.combine(now.date(), due_time)

                # If the time has already passed today then it will be set for tomorrow
				if due_datetime < now:
					due_datetime += timedelta(days=1)

				deadline_dict[task] = due_datetime
				print(f"Deadline set for '{task}' at {due_datetime.strftime('%I:%M %p')}")
				break
			except ValueError:
				print("Please use military format (e.g., 14:30)")


#The following function will track the tasks after the deadline is reached and sorts them into completed/incomplete lists
def track_tasks():
	print("\nLet's see where you are at with the tasks \n")
	still_tracking = True

	while still_tracking and deadline_dict:
		now = datetime.now()

		for task in list(deadline_dict):
			if now >= deadline_dict[task]:
				print(f"\nTime is up for: '{task}'")
				done = input("Did you complete it? (yes/no): ").strip().lower()

				if done == "yes":
					completed_tasks.append(task)
				else:
					incomplete_tasks.append(task)

				deadline_dict.pop(task)

		# Ask if the user wants to keep checking if there are still tasks left
		if deadline_dict:
			answer = input("\nDo you want to continue tracking tasks? (yes/no): ").strip().lower()
			if answer != "yes":
				break

		time.sleep(25)

#The following function shows the completed and incomplete list sections
def show_results():

	print("\n Completed Tasks:")
	if completed_tasks:
		for task in completed_tasks:
			print(f" - {task}")
	else:
		print(" (none)")

	print("\n Incomplete Tasks:")
	if incomplete_tasks:
		for task in incomplete_tasks:
			print(f" - {task}")
	else:
		print(" (none)")

#The following function gives the user the opportunity to export their show_results() list to a private .txt file on their computer
def export():
    decision = input("Would you like to create a txt file with your list for better management? (yes/no): ").strip().lower()
    if decision == "yes":
        filename = input("What would you like to name your file? (do NOT include .txt): ").strip()
        filename += ".txt"

        with open(filename, "w") as file:
            file.write("Completed Tasks:\n")
            if completed_tasks:
                for task in completed_tasks:
                    file.write(f"\t- {task}\n")  
            else:
                file.write("\t(none)\n")
            
            file.write("\nIncomplete Tasks:\n")
            if incomplete_tasks:
                for task in incomplete_tasks:
                    file.write(f"\t- {task}\n")  
            else:
                file.write("\t(none)\n")

        print(f"Your list has been successfully saved as '{filename}'!")
    else:
        print("No file was created.")

# The following function removes any tasks you don't want to think about anymore
def remove_task():
    if not order_dict:
        print("\nNo tasks available to remove.\n")
        return

    print("\nHere are your tasks:")
    for key, task in order_dict.items():
        print(f"{key}: {task}")

    task_num = input("\nEnter the number of the task you want to remove:\n> ").strip()
    if task_num.isdigit():
        task_num = int(task_num)
        if task_num in order_dict:
            task_name = order_dict.pop(task_num)
            deadline_dict.pop(task_name, None)
            if task_name in incomplete_tasks:
                incomplete_tasks.remove(task_name)
            if task_name in completed_tasks:
                completed_tasks.remove(task_name)
            notes_dict.pop(task_name, None)
            print(f"'{task_name}' has been removed from your to do list.\n")
        else:
            print("Task number not found.\n")
    else:
        print("Invalid input. Please enter a number.\n")

#The following function adds a note to any task you have on your list
def add_notes():
    print("\nAdd a note to a task:")
    for key in order_dict:
        print(f"\t{key}: {order_dict[key]}")  
    try:
        task_num = int(input("Enter the number of the task you want to add a note to:\n> "))
        if task_num in order_dict:
            note = input("Enter your note:\n> ").strip()
            if note:
                notes_dict[order_dict[task_num]] = note
                print("Note added successfully.\n")
        else:
            print("Invalid task number.\n")
    except ValueError:
        print("Please enter a valid number.\n")
        
        
'''The following function displays your most current list of tasks including notes you might
have added for a better idea of where you are with your list '''

def full_task_list():
	if not order_dict:
		print("\n Your to-do list is currently empty.\n")
		return

	print("\n Full To Do List:\n")
	for key in sorted(order_dict):  
		task = order_dict[key]
		print(f"\t{key}: {task}")
        
        # Check if there is a note attached
		if task in notes_dict:
			print(f"\t\t Note: {notes_dict[task]}")

	print("\n")

#The main function with the menu to choose from
def main():
    while True:
        print("\n--- To-Do List Main Menu ---")
        print("1. Add New Tasks ")
        print("2. Add deadlines to your chosen tasks")
        print("3. Track Tasks (start monitoring)")
        print("4. Show the full list so far")
        print("5. Show Completed/Incomplete Tasks")
        print("6. Remove a Task")
        print("7. Add a note")
        print("8. Would you like to create a .txt file with your list?")
        print("9. Quit")

        choice = input("Enter your choice (1-9):\n> ").strip()

        if choice == '1':
            to_do()
        elif choice == '2':
            deadlines()
        elif choice == '3':
            track_tasks()
        elif choice == '4':
        	full_task_list()
        elif choice == '5':
            show_results()
        elif choice == '6':
            remove_task()
        elif choice == '7':
            add_notes()
        elif choice == '8':
            export()
        elif choice == '9':
            print("\nGoodbye! Thanks for using the To-Do List Organizer!\n")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 8.\n")
main()