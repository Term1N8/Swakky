SMTP goes brrrrr 

usage: swakky.py [-h] [--file FILE] [--to-internal TO_INTERNAL] [--from-internal FROM_INTERNAL] [--to-external TO_EXTERNAL] [--from-external FROM_EXTERNAL] [--subject SUBJECT] [--body BODY] [--prompt]

Execute a command on hosts with open SMTP ports or a specific server.

options:
  -h, --help            show this help message and exit
  --file FILE           Path to the Nmap XML file
  --to-internal TO_INTERNAL
                        Target to send emails to internally
  --from-internal FROM_INTERNAL
                        Internal source email address to spoof messages from
  --to-external TO_EXTERNAL
                        Target to send emails to externally
  --from-external FROM_EXTERNAL
                        External source email address to spoof messages from
  --subject SUBJECT     Email subject
  --body BODY           Message body for the email
  --prompt              Prompt before executing each command

