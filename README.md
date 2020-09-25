# librus-presence

### A project that I made to get attendance at e-lessons without replying to teachers messages

#### Requirements

* [Python 3](https://www.python.org/)
* [Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* [Google Chrome](https://www.google.com/chrome/)

#### Installation
1. `git clone https://github.com/kko7/librus-presence.git`
2. `cd librus-presence`
3. `pip3 install -r requirements.txt`

#### Usage
`python3 presence.py -u LIBRUS_USERNAME -p LIBRUS_PASSWORD`

#### Required arguments
* -p/--password - librus password
* -u/--username - librus username

#### Optional arguments
* -v/--verbose - debug mode
* -hl/--headless - run environment without the full browser UI
