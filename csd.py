import requests
from bs4 import BeautifulSoup
import zipfile
import tkinter as tk
from tkinter import filedialog


def yes_no_input():
    while True:
        choice = input("You want to research again? [y/n]: ").lower()
        if choice in ["y", "ye", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False


def folder_select():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    return folder_path


while True:
    while True:
        # Search Movie
        search_movietitle = input("Movie Title: ").replace(" ", "+").lower()
        search_url = "https://subdl.com/subtitle_search.php?q=" + search_movietitle
        print(search_url)
        html = requests.get(search_url).content

        soup = BeautifulSoup(html, "lxml")

        titles = list()
        totals = list()
        for head in soup.find_all("div", class_="box_head_text"):
            h2 = head.find("div", class_="tile").find("h2")
            if h2.text == "Other Results" or h2.text == "Popular":
                for row in head.find_all("div", class_="row"):
                    for a in row.find_all("a"):
                        if "subtitles" in a.text:
                            totals.append(a)
                        else:
                            titles.append(a)
        for i in range(len(titles)):
            print(str(i) + ":", titles[i].text, ":", totals[i].text)
        if yes_no_input():
            pass
        else:
            selected_row = int(input("Select Movie: "))
            break

    # Select Subtitle
    html = requests.get("https://subdl.com/" + titles[selected_row]["href"]).content

    soup = BeautifulSoup(html, "lxml")

    sub_titles = list()
    # Get A Tags
    for row_en in soup.find_all("div", class_="row subtitle_row English"):
        for a in row_en.find_all("a"):
            if "subtitles" in a.text:
                pass
            else:
                sub_titles.append(a)
    for row_en in soup.find_all("div", class_="subtileRowWrapper English"):
        for a in row_en.find("div", class_="subtileList").find_all("a"):
            sub_titles.append(a)

    for i in range(len(sub_titles)):
        print(str(i) + ":", sub_titles[i].text)
    selected_row = int(input("Select Subtitle: "))

    print("Download start.")
    # Download Zip file
    if sub_titles[selected_row]["href"].startswith("https://"):
        download_url = sub_titles[selected_row]["href"]
    else:
        download_url = "https://subdl.com/" + sub_titles[selected_row]["href"]
    zip_data = requests.get(download_url).content
    zip_path = (
        "./"
        + sub_titles[selected_row]
        .text.replace(":", "")
        .replace("<", "")
        .replace(">", "")
        .replace("?", "")
        + ".zip"
    )
    with open(zip_path, mode="wb") as file:
        file.write(zip_data)
    print("Download completed.")
    print("Unzipping...")
    # Unzip file

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(folder_select() + "/" + zip_path.replace(".zip", ""))
    print("Extracted.")
