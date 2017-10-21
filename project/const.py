from string import ascii_letters, ascii_uppercase, ascii_lowercase, digits

# creating multiple char dicts, so that initial links won't have many consecutive same characters
ALLCHARS = [None]*4
ALLCHARS[0] =  {i: char for i, char in enumerate(ascii_letters + digits)}
ALLCHARS[1] =  {i: char for i, char in enumerate(ascii_letters[::-1] + digits[::-1])}
ALLCHARS[2] =  {i: char for i, char in enumerate(digits + ascii_letters[::-1])}
ALLCHARS[3] =  {i: char for i, char in enumerate(ascii_lowercase + digits + ascii_uppercase)}