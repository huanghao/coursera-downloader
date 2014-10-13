import os
import argparse

import requests




class DL(object):

    LECTURE = 'https://class.coursera.org/%s/lecture'
    LOGIN = 'https://accounts.coursera.org/api/v1/login'

    def __init__(self, path, user, password, cid):
        self.path = path
        self.user = user
        self.password = password
        self.cid = cid
        self.lecture = self.LECTURE % self.cid
        self.cookie = os.path.join(path, 'cookie')
        self._session = None
        self._csrf = None

    def check_cookie(self):
        if os.path.exists(self.cookie):
            return
        self._session = requests.Session()
        r = self._session.get(self.lecture)
        if not 'csrf_token' in self._session.cookies:
            raise Exception("Can't get csrf_token: %s" % r)
        self._csrf = self._session.cookies['csrf_token']
        self._login()

    def _login(self):
        s = requests.Session()
        r = s.get(self.lecture)
        print r
        print s.cookies.items()
        self._csrf = s.cookies['csrf_token']
        print self._csrf

        r = s.post(self.LOGIN, {
                'email': self.user,
                'password': self.password,
                'webrequest': 'true',
                }, headers={
                'X-CSRFToken': self._csrf,
                })
        print r
        print self._session.cookies.items()
        print r.content


def download(args):
    path = args.directory if args.directory else os.path.join(os.getcwd(), args.cid)
    dl = DL(path, args.user, args.password, args.cid)
    dl._login()
    #dl.check_cookie()
    #dl.build_index()
    #dl.start()


def list_courses(args):
    print args


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')

    subs = parser.add_subparsers(title='actions')

    dl = subs.add_parser('d', help='download')
    dl.set_defaults(func=download)
    dl.add_argument('cid')
    dl.add_argument('-d', '--directory',
                    type=os.path.abspath,
                    help='download directory')

    li = subs.add_parser('l', help='list')
    li.set_defaults(func=list_courses)
    li.add_argument('-a', '--all')
    li.add_argument('-c', '--current')
    li.add_argument('-u', '--upcomming')

    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
