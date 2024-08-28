import argparse
import csv
import requests
import time
import os
import re
import sys
from bs4 import BeautifulSoup
from logging import Logger, basicConfig, getLogger
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

def get_args():
    parser = argparse.ArgumentParser(description =
        """
            Score crawler for NTHUOJ.

            Prepare a csv file in following format:
            x        [pid_1] [pid_2] [pid_3] ...
            [user_1]
            [user_2]
            [user_3]
            ...
        """
    )
    parser.add_argument("file", help = "csv file to fill score.")
    parser.add_argument("--dest", default = "dump.csv", help = "File to dump the result. Default is dump.csv")
    parser.add_argument("--partial", action = "store_true", help = "Allow partial score (equally weighted for each testcase).")
    return parser.parse_args()

logger = getLogger(__name__)

if __name__ == "__main__":
    basicConfig(
        format = "%(asctime)s [%(levelname)s] %(message)s",
        datefmt = "%H:%M:%S",
        level = os.getenv("LOG_LEVEL", "INFO")
    )

    args = get_args()

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service = service)

    login_url = "https://acm.cs.nthu.edu.tw/users/login/?next=/"

    driver.get(login_url)
    input("請在瀏覽器中手動登入，然後在此處按Enter繼續...")

    with open(args.file, newline = "", mode = "r") as file, open(args.dest, mode = "w+", newline = "") as score_file:
        reader = csv.reader(file)
        writer = csv.writer(score_file)
        reader_rows = [row for row in reader]
        problem_list = reader_rows[0][1:]
        writer.writerow(["", *problem_list])
        usernames = [row[0] for row in reader_rows[1:]]
        logger.info(f"Number of users: {len(usernames)}")
        logger.info(f"Number of problems: {len(problem_list)}")
        for index, username in enumerate(usernames):
            logger.info(f"Finding {username} [{index + 1}/{len(usernames)}]")
            scores = []
            for problem_id in problem_list:
                url = f"https://acm.cs.nthu.edu.tw/status/?username={username}&pid={problem_id}&cid=&status="
                driver.get(url)
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")
                # Check if the username exist.
                if f"User {username} does not exist" in soup.prettify():
                    logger.info(f"User {username} does not exist!")
                    break
                # No submissions.
                if "No submissions found for the given query!" in soup.prettify():
                    logger.info(f"Username: {username}, Problem id: {problem_id}, No submissions found")
                    scores.append(0)
                else:
                    passed = 0
                    total = 0
                    pattern_regex = re.compile(r"\((\d+)/(\d+)\)")
                    for td in soup.find_all("td"):
                        match = pattern_regex.search(td.text)
                        if match:
                            passed = max(passed, int(match.group(1)))
                            total = max(total, int(match.group(2)))
                    if total == 0:
                        total = 1
                    if args.partial:
                        score = passed / total * 100
                    else:
                        score = 100 if passed == total else 0
                    logger.info(f"Username: {username}, Problem id: {problem_id}, Passed: {passed}, Total: {total}, Score: {score}")
                    scores.append(score)
                time.sleep(0.5)
            writer.writerow([username, *scores])

    driver.close()
