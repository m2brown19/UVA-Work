Buffer Overflow attack on Sync Breeze 10.0.28. 
I created this exploit with the following steps:
- installing Sync Breeze to a Windows virtual machine (virginia cyber range). 
- Allowing inbound connection to port 9121 so that I could connect to the Sync Breeze app. 
- Vulnerability analysis via fuzzing the login page
- Sent a HTTP GET request via my Metasploit fuzzer module to crash the app
- After crashing, I analyzed Sync Breeze with the Immunity debugger
- I found where it crashed in the app with a long username
- Inserted jmp esp instruction address and payload in username string so that I could get a reverse shell


Note
- The fuzzer module does not need to be used anymore. I built it first to help me analyze Sync Breeze but you only need the exploit module in the attack. 
- The modules have not been cleaned up so although they serve their purpose, they could be neater. 
