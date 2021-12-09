#!/bin/python
from pynput.keyboard import *
import dmenu, os, sys
import pyperclip as pc

passwords_store= os.listdir(os.path.join(os.path.expanduser('~'), '.password-store')); passwords_store.remove('.git'); passwords_store.remove('.gpg-id')
passwords= []
for pw in passwords_store:
    if os.path.isfile(os.path.join(os.path.expanduser('~'), '.password-store', pw)):
        passwords.append(pw[:len(pw)- 4])
    else:
        pw, dir_name= os.listdir(os.path.join(os.path.expanduser('~'), '.password-store', pw)), pw
        for i in range(len(pw)):
            passwords.append(dir_name+ '/'+ pw[i][:len(pw[i])- 4])

pw_file= dmenu.show(passwords, prompt= 'pass')

pw_file= os.popen(f'pass {pw_file}').read().split('\n'); pw_file= pw_file[:len(pw_file)- 1]
pw= pw_file[0]

# copy pw to clipboard
pc.copy(pw)

# select option for autotype
option= dmenu.show(['autotype', 'pass', 'user'], prompt= 'option')
keyboard= Controller()

if option== 'pass':
    keyboard.type(pw)
    sys.exit()
else:
    user_index= pw_file[1]
    user= ''
    if user_index[:5]== 'user:':
        user= user_index[6:]
    else:
        user= user_index[10:]

    if option== 'user':
        print(user)
        keyboard.type(user)
        sys.exit()
    elif option== 'autotype':
        keyboard.type(user)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        keyboard.type(pw)
        sys.exit()
