import argparse

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC


SIGNIN_URL = "https://accounts.coursera.org/signin"
TIMEOUT = 120

def signin(web, username, password):
    """
    Sign in with `username` and `password`
    Returns cookies after signed-in
    """
    web.get(SIGNIN_URL)

    email = wait(web, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "signin-email")))
    email.send_keys(username)

    pwd = web.find_element_by_id('signin-password')
    pwd.send_keys(password)

    btn = web.find_element_by_class_name('coursera-signin-button')
    btn.click()

    wait(web, TIMEOUT).until(EC.title_contains('Your Courses'))

    return web.get_cookies()


def get_cookie(args):
    """
    Launch a chrome to get cookies
    """
    chromeopts = ChromeOptions()
    if args.proxy:
        chromeopts.add_argument('--proxy-server=%s' % args.proxy)
    web = Chrome(chrome_options=chromeopts)
    try:
        return signin(web, args.user, args.password)
    finally:
        web.quit()


def main():
    args = parse_args()

    cookie = get_cookie(args)
    cookie_string = ' '.join(['%s=%s;' % (c['name'], c['value'])
        for c in cookie])

    if args.output:
        with open(args.output, 'w') as file:
            file.write(cookie_string)
        print 'Write COOKIE to', args.output
    else:
        print 'COOKIE:', cookie_string


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('user')
    parser.add_argument('password')
    parser.add_argument('--proxy')
    parser.add_argument('-O', '--output')
    return parser.parse_args()


if __name__ == '__main__':
    main()
