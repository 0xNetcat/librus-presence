# librus-presence

## I am not sure if this is working. I will test this later this week

### Requirements

1. [Python 3](https://www.python.org/)
2. [Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
3. [Google Chrome](https://www.google.com/chrome/)

### Installation
1. `git clone https://github.com/kko7/librus-presence.git`
2. `cd librus-presence`
3. `pip3 install -r requirements.txt`

### Usage
`python3 presence.py -u LIBRUS_USERNAME -p LIBRUS_PASSWORD`

### Required arguments
* -p/--password - librus password
* -u/--username - librus username

### Optional arguments
* -v/--verbose - debug mode
* -hl/--headless - run environment without the full browser UI
