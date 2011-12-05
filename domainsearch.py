#!/usr/bin/env python
#
# Free random domain search utility
# Copyright (c) 2010 Martynas Jocius <martynas@idiles.com>
#
# This is free software. Use at your own risk.
#

import random
import string
import socket
import commands

vowels = 'aeiou'
consonants = 'bcdefghklmnprsvzw'

def random_word():
    length = random.randint(3, 6)
    letters = []
    last = ''
    for i in range(length):
        if last in vowels:
            l = random.choice(consonants)
        else:
            l = random.choice(vowels)
        last = l
        letters.append(l)
    word = ''.join(letters)
    return word
    
def main():
    domains = []
    # Load existing generated domains that are found to be free
    try:
        domains = map(string.strip, open('domains.txt', 'r').readlines())
    except IOError:
        pass
        
    tries = 500
    found = 0
        
    for i in range(tries):
        domain = '%s.com' % random_word()
        if domain in domains:
            continue
            
        try:
            socket.gethostbyname(domain)
        except Exception, e:
            output = commands.getoutput('whois %s' % domain)
            if 'No match for' in output:
                print domain
                domains.append(domain)
                found += 1
        
    fd = open('domains.txt', 'w')
    for d in domains:
        fd.write('%s\n' % d)
    fd.close()
    
    print '---'
    percent = int(float(found) / tries * 100)
    print '%i new domains in %i tries (%i%%).' % (found, tries, percent)
    print '%i free domains on your list.' % len(domains)
    
if __name__ == '__main__':
    main()
    
