import pickle
import os.path
import sys
from time import localtime

file_path = "/Users/vincent/Code/Py/Budget/bud"


class Transaction:
    def __init__(self, val, comments):
        self.val = val
        self.time = localtime()
        self.comments = comments

    def __str__(self):
        return '%-8.2f|%4d.%2d.%2d  |%s' % (
            self.val, self.time.tm_year, self.time.tm_mon, self.time.tm_mday, self.comments)


class Pool:
    def __init__(self, val):
        self.v = val

    def __str__(self):
        return '%s: %d' % (
            str(self.__class__).split('.')[1], self.v)


class Account:
    def __init__(self, a, b, c):
        self.Ps = a, b, c
        self.setupTime = localtime()
        self.tList = []

    def __str__(self):
        string = [i.__str__() for i in self.Ps]
        return str(string)

    def add_transaction(self, t):
        self.tList.append(t)

    def hint(self):
        print '%4d.%02d.%02d' % (localtime().tm_year, localtime().tm_mon, localtime().tm_mday)
        print "Semester: %8.2f" % (self.Ps[2].v - sum([t.val for t in self.tList]))
        print "Monthly:  %8.2f" % (self.Ps[1].v - sum([t.val for t in self.tList
                                                       if t.time.tm_mon == localtime().tm_mon]))
        print "AccDaily: %8.2f" % (self.Ps[0].v * localtime().tm_mday - sum([t.val for t in self.tList
                                                                             if t.time.tm_mon == localtime().tm_mon]))
        print "Daily:    %8.2f" % (self.Ps[0].v - sum([t.val for t in self.tList
                                                       if t.time.tm_mday == localtime().tm_mday]))


def load(path=file_path):
    if not os.path.isfile(path):
        dump(({}, None))
    with open(path, 'rb') as f:
        return pickle.load(f)


def dump(data, path=file_path):
    with open(path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def shell():
    accounts, head = load()
    print "Budget Shell (alpha)\nHEAD -->", head
    while True:
        p = raw_input(">>>").strip().lower()
        if p == "":
            continue
        p = p.split()
        if p[0] == "q":
            print "Quit Budget Shell"
            break
        elif p[0] == "re-build":
            if raw_input("Please input reset code:") == "Imsurere":
                print "\r\nData cleaned!"
                sys.stdout.flush()
                accounts = {}
                head = None
            else:
                print "Wrong!"
                continue
        elif p[0] == "new_":
            name = raw_input("Account name:")
            sp = Pool(float(raw_input("Semester Budget:")))
            mp = Pool(float(raw_input("Monthly  Budget:")))
            dp = Pool(float(raw_input("Daily    Budget:")))
            accounts[name] = Account(dp, mp, sp)
            head = name
        elif p[0] == 'all':
            for k in accounts.keys():
                if head == k:
                    print '*',
                else:
                    print ' ',
                print k
        elif p[0] == 'checkout' or p[0] == '-c':
            if p[1] in accounts.keys():
                head = p[1]
                print "Now HEAD --> %s" % head
            else:
                print "No such %s account" % p.split()[1]
        elif p[0] == 'add' or p[0] == 'a':
            if len(p) == 3:
                comm = p[2]
            elif len(p) == 2:
                comm = raw_input("comment:")
            else:
                continue
            accounts[head].add_transaction(Transaction(float(p[1]), comm))
            dump((accounts, head))

        elif p[0] == 'detail' or p[0] == 'd':
            tmp=accounts[head].tList
            tmp.reverse()
            for i in tmp:
                print i
            tmp.reverse()
        elif p[0] == "budget" or p[0] == "b":
            accounts[head].hint()
        elif p[0] == "admin":
            if raw_input("enter code:") == "admin":
                while True:
                    try:
                        command = raw_input(">>_:")
                        if not command == "quit":
                            exec command
                        else:
                            break
                    except Exception:
                        print "cannot solve command!"

            else:
                print "Wrong!"
        else:
            print "Unknown command!"
    dump((accounts, head))


if __name__ == "__main__":
    shell()
