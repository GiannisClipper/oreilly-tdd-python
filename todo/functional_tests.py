from selenium import webdriver

# a user visit todo url
browser = webdriver.Firefox()
browser.get('http://localhost:8000')

# verify through title that is in correct page
assert 'todo app' in browser.title

# invited to enter a new todo text item

# enter the text "Go for a walk"

# page updated and display the text entered

# still invited to enter a new todo text item

# enter "Go another walk"

# page updated again showing both texts entered

# user noticed page generated a unique url accessing previous entries

# visit unique url and access previous entries