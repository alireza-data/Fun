# -*- coding: utf-8 -*-
"""This code is generated merelly for fun purposes to push a random number in Github repository on a weekly basis."""

#!/usr/bin/env python3
import os
import random
import subprocess
from datetime import datetime, timedelta
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def read_number():
    with open('number.txt', 'r') as f:
        return int(f.read().strip())


def write_number(num):
    with open('number.txt', 'w') as f:
        f.write(str(num))


def git_commit():
    # Stage the changes
    subprocess.run(['git', 'add', 'number.txt'])

    # Create commit with current date
    date = datetime.now().strftime('%Y-%m-%d')
    commit_message = f"Update number: {date}"
    subprocess.run(['git', 'commit', '-m', commit_message])


def git_push():
    # Push the committed changes to GitHub
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Changes pushed to GitHub successfully.")
    else:
        print("Error pushing to GitHub:")
        print(result.stderr)


def update_cron_with_random_time():
    # Generate random day of the week (0-6, where 0 is Sunday)
    random_day = random.randint(0, 6)
    # Generate random hour (0-23) and minute (0-59)
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)

    # Define the new cron job command
    new_cron_command = f"{random_minute} {random_hour} * * {random_day} cd {script_dir} && python3 {os.path.join(script_dir, 'update_for_fun.py')}\n"

    # Get the current crontab
    cron_file = "/tmp/current_cron"
    os.system(f"crontab -l > {cron_file} 2>/dev/null || true")  # Save current crontab, or create a new one if empty

    # Update the crontab file
    with open(cron_file, "r") as file:
        lines = file.readlines()

    with open(cron_file, "w") as file:
        for line in lines:
            # Remove existing entry for `update_for_fun.py` if it exists
            if "update_for_fun.py" not in line:
                file.write(line)
        # Add the new cron job at the random time
        file.write(new_cron_command)

    # Load the updated crontab
    os.system(f"crontab {cron_file}")
    os.remove(cron_file)

    print(f"Cron job updated to run at {random_hour}:{random_minute} on day {random_day} of the week.")

def main():
    try:
        current_number = read_number()
        new_number = current_number + 1
        write_number(new_number)

        git_commit()
        git_push()

        update_cron_with_random_time()

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    # Use sys.argv[0] if __file__ is not defined
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0] if '__file__' not in globals() else __file__))
    os.chdir(script_dir)
    main()
