from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime

# create a new Chrome driver
driver = webdriver.Chrome()

# navigate to the Google homepage
driver.get("https://www.google.com")

# find the search box element and enter "dhaka"
search_box = driver.find_element(By.NAME,"q")
search_box.send_keys("dhaka")

# wait for the suggestions to appear
driver.implicitly_wait(10)

# find all the suggestion elements
suggestions = driver.find_elements(By.CSS_SELECTOR,"#sug-list > div")

# initialize variables for the longest and shortest words
longest_word = ""
shortest_word = ""

# iterate through the suggestions
for suggestion in suggestions:
    # get the text of the suggestion
    suggestion_text = suggestion.text
    # split the text into words
    words = suggestion_text.split(" ")
    # iterate through the words
    for word in words:
        # check if the word is longer than the current longest word
        if len(word) > len(longest_word):
            longest_word = word
        # check if the word is shorter than the current shortest word
        if len(word) < len(shortest_word) or len(shortest_word) == 0:
            shortest_word = word

# get the current date and time
now = datetime.datetime.now()

# create a new text file and write the longest and shortest words and the search date and time
with open("search_results.txt", "w") as f:
    f.write("Longest suggestion: " + longest_word + "\n")
    f.write("Shortest suggestion: " + shortest_word + "\n")
    f.write("Searched on: " + now.strftime("%Y-%m-%d %H:%M:%S"))

# close the driver
driver.quit()
