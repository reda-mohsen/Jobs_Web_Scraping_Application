import requests
from bs4 import BeautifulSoup
import csv


def main():
    response_content = get_response_content()
    if response_content:
        write_on_csv(get_repo_names(response_content))


def get_user():
    try:
        user_name = input("Enter GitHub Username: ")
        return user_name
    except KeyboardInterrupt:
        print("\nInput canceled by the user.")
        return None
    except Exception as err:
        print(f"An error occurred: {str(err)}")
        return None


def get_response_content():
    try:
        username = get_user()
        if username:
            url = f"https://github.com/{username}?tab=repositories"
            response = requests.get(url)
            if not response.status_code == 200:
                raise ValueError("Status code is not equal to 200")
            return response.content
    except Exception as err:
        print(f"An error occurred: {str(err)}")
        return None


def get_repo_names(response_content):
    try:
        soup = BeautifulSoup(response_content, "lxml")
        repositories = soup.find(id="user-repositories-list")
        repo_names = []
        repos = repositories.find_all("li", class_="col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public source")
        for repo in repos:
            repo_name = repo.find("a", {"itemprop": "name codeRepository"}).text.strip()
            if repo_name:
                repo_names.append({"Repository Name": repo_name})
        return repo_names
    except Exception as err:
        print(f"An error occurred: {str(err)}")
        return None


def write_on_csv(data):
    try:
        keys = ["Repository Name"]
        with open("repo_names.csv", 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        print("file created successfully")
    except Exception as err:
        print(f"An error occurred: {str(err)}")


if __name__ == "__main__":
    main()
