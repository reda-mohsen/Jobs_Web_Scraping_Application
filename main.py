# ------------------------------------------
# Name: Reda Mohsen Reda
# Project Title: Github Repositories Web Scraping Application
# Description: This script is a simple GUI application that takes a GitHub username as input,
# scrapes the user's public repositories, and generates a CSV file with the repository names.
# It then opens the CSV file with the default associated program.
# ------------------------------------------

# Import necessary modules
import re
import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import messagebox
import os, sys


def main():
    # Create a main application window
    root = tk.Tk()
    root.title("Github Repositories Application")
    root.geometry("350x150")

    # Load the icon image file
    icon = tk.PhotoImage(file="assets/github.png")

    # Set the icon for the window
    root.tk.call("wm", "iconphoto", root._w, icon)

    # Create a Frame to hold the Entry widget
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(side="top")

    # Create a label widget
    input_username_label = tk.Label(frame, text="Enter Github Username", padx=10, pady=10)
    input_username_label.pack()

    # Create an Entry widget within the Frame to get input edges
    input_username_entry = tk.Entry(frame, width=50)
    input_username_entry.pack()

    def on_button_selected():
        try:
            # Get GitHub username from the input and fetch repository data
            username = get_user(input_username_entry.get())
            data = get_repo_names(get_response_content(username))

            # Write repository names to CSV file and open the file
            path = "repo_names.csv"
            bool = write_on_csv(path, data)

            if bool:
                # Ask the user if they want to open the file
                response = messagebox.askquestion("File created successfully", "Do you want to open file?")

                if response == 'yes':
                    open_csv_file(path)
                    sys.exit()
                else:
                    sys.exit()
            else:
                messagebox.showerror("Error", "File Creation Failed")
        except ValueError as err:
            # Display an error message in case of an exception
            print(err)
            messagebox.showerror("Error", err)
            pass

    # Create margin
    tk.Label(frame, text="").pack()

    # Create a Button widget within the Frame to start the search
    button = tk.Button(frame, text="Generate CSV File", padx=30, pady=5, command=on_button_selected)
    button.pack()

    # Start the main event loop
    root.mainloop()


# Validate GitHub username using a regular expression
def get_user(input_username):
    user_name = input_username.strip()
    if match := re.search(r"^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}[a-zA-Z0-9]$", user_name, re.IGNORECASE):
        return user_name
    else:
        raise ValueError("Invalid username")


# Fetch HTML content of the user's GitHub repository page
def get_response_content(username):
    if username:
        url = f"https://github.com/{username}?tab=repositories"
        response = requests.get(url)
        if not response.status_code == 200:
            raise ValueError("Denied Access")
        return response.content


# Extract repository names from the HTML content using BeautifulSoup
def get_repo_names(response_content):
    try:
        soup = BeautifulSoup(response_content, "lxml")
        repositories = soup.find(id="user-repositories-list")
        repo_names = []
        repos = repositories.find_all("li",
                                      class_="col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public source")
        for repo in repos:
            repo_name = repo.find("a", {"itemprop": "name codeRepository"}).text.strip()
            if repo_name:
                repo_names.append({"Repository Name": repo_name})
        return repo_names
    except Exception as err:
        raise ValueError(err)


# Write repository names to a CSV file
def write_on_csv(path, data):
    try:
        if data:
            keys = ["Repository Name"]
            with open(path, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
            return True
        else:
            return False
    except Exception as err:
        raise ValueError(err)


# Open a CSV file using the default associated program
def open_csv_file(file_path):
    try:
        os.startfile(file_path)
    except FileNotFoundError as err:
        raise ValueError(err)


if __name__ == "__main__":
    main()
