import os
import subprocess
import sys
import multiprocessing
import time
import random

def print_menu():
    """Display the menu options."""
    print("\nMenu:")
    print("1. Show processes (ps)")
    print("2. Show today's date (date)")
    print("3. List files and directories (ls)")
    print("4. The Linux command of your choice")
    print("5. One child pings https://amazon.co.uk and the other child pings https://news.sky.com")
    print("6. The parent processes pauses the child and then it restarts the child.")
    print("7. Exit")
    print("Please select an option: ", end="")

def ping_amazon():
    """Ping www.amazon.co.uk"""
    print(f"Child 1 Process ID: {os.getpid()}")
    print("Child 1 is pinging https://www.amazon.co.uk/")
    os.execlp("ping", "ping", "-c", "4", "www.amazon.co.uk")

def ping_sky():
    """Ping news.sky.com"""
    print(f"Child 2 Process ID: {os.getpid()}")
    print("Child 2 is pinging https://news.sky.com/")
    os.execlp("ping", "ping", "-c", "4", "news.sky.com")

def pause_and_restart_child(child_process):
    """Pause the child for 2 seconds and then restart it."""
    print(f"Pausing the child process with PID {child_process.pid} for 2 seconds.")
    child_process.terminate()  # Terminate the child process
    time.sleep(2)  # Wait for 2 seconds
    print(f"Restarting the child process with PID {child_process.pid}.")
    child_process.start()  # Restart the child process

def main():
    """Main function to handle menu and execute commands."""
    while True:
        
        print_menu()
        
        while True:
            try:
                choice = int(input())  
                if choice in [1, 2, 3, 4, 5, 6, 7]:  
                    break
                else:
                    print("Invalid choice. Please select a valid option from 1 to 7.")
                    print_menu()
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 7.")
                print_menu()

        if choice == 7:
            print("Exiting the program.")
            break
        
        if choice == 6:
            # Option 6: The parent pauses and restarts the child
            print(f"Parent Process ID: {os.getpid()}")
            
            try:
                # Create child process using multiprocessing
                child_process = multiprocessing.Process(target=ping_amazon)
                child_process.start()  # Start the child process
                
                # Pause and restart the child process after 2 seconds
                pause_and_restart_child(child_process)
                
                # Wait for the child process to finish
                child_process.join()

            except Exception as e:
                print(f"Error occurred while pausing and restarting the child process: {e}")

        elif choice == 5:
            # Option 5: Show parent PID and spawn child processes for ping
            print(f"Parent Process ID: {os.getpid()}")
            
            try:
                # Create child processes using multiprocessing
                child1 = multiprocessing.Process(target=ping_amazon)
                child2 = multiprocessing.Process(target=ping_sky)
                
                # Start the child processes
                child1.start()
                child2.start()
                
                # Wait for both children to finish
                child1.join()
                child2.join()
                
            except Exception as e:
                print(f"Error occurred while creating child processes: {e}")

        elif choice == 1:
            command = "ps"
            command_desc = "shows the current processes."
        elif choice == 2:
            command = "date"
            command_desc = "shows today's date and time."
        elif choice == 3:
            command = "dir"  
            command_desc = "lists files and directories in the current directory."
        elif choice == 4:
            command = "uptime"
            command_desc = "shows how long the system has been running."

        # Output the action being performed
        print(f"Running '{command}' command - {command_desc}")
        print(f"Child Process ID: {os.getpid()}")

        try:
            if sys.platform == "win32":
                if command == "ps":
                    command = "tasklist"  
                elif command == "uptime":
                    command = "systeminfo | findstr /C:'System Boot Time'"  

                subprocess.run(command, shell=True)
            else:
                subprocess.run([command])

        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
