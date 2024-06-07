import argparse
import xml.etree.ElementTree as ET
import subprocess

print("   _____              _    _          \n"
"  / ____|            | |  | |         \n"
" | (_____      ____ _| | _| | ___   _ \n"
"  \___ \ \ /\ / / _` | |/ / |/ / | | |\n"
"  ____) \ V  V / (_| |   <|   <| |_| |\n"
" |_____/ \_/\_/ \__,_|_|\_\_|\_\\__, |\n"
"                                 __/ |\n"
"                                |___/ \n"
"SMTP goes brrrrr \n")
def parse_nmap_xml(xml_file):
    hosts_with_smtp = {}

    tree = ET.parse(xml_file)
    root = tree.getroot()

    for host in root.findall(".//host"):
        for port in host.findall(".//port"):
            service = port.find(".//service[@name='smtp']")
            if service is not None:
                address = host.find(".//address[@addrtype='ipv4']").attrib['addr']
                smtp_port = port.attrib['portid']
                hosts_with_smtp[address] = smtp_port

    return hosts_with_smtp

def execute_command_on_smtp_hosts(hosts, to_internal, from_internal,  prompt):
    for address, smtp_port in hosts.items():
        if to_internal is not None and from_internal is not None:
            print(f"\nTesting internal to internal on {address}")
            command = f"swaks --to {to_internal} --from {from_internal} --timeout 5s --server {address}:{smtp_port} --body \"{body} SENT FROM:{address}\" --header Subject:\"{subject}\""
            execute_command(command, prompt, address, smtp_port)

        if to_internal is not None and from_external is not None:
            print(f"\nTesting external to internal on {address}")
            command = f"swaks --to {to_internal} --from {from_external} --timeout 5s  --server {address}:{smtp_port} --body \"{body} SENT FROM:{address}\" --header Subject:\"{subject}\""
            execute_command(command, prompt, address, smtp_port)

        if to_external is not None and from_internal is not None:
            print(f"\nTesting internal to external on {address}")
            command = f"swaks --to {to_external} --from {from_internal} --timeout 5s  --server {address}:{smtp_port} --body \"{body} SENT FROM:{address}\" --header Subject:\"{subject}\""
            execute_command(command, prompt, address, smtp_port)

def execute_command(command, prompt, address, smtp_port):
    print(command)
    if prompt:
        user_input = input(f"Do you want to execute the command on {address} ({smtp_port})? (Y/n): ").lower()
        if user_input == 'n':
            print(f"Skipping command execution on {address} ({smtp_port})")
            return

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command on {address} ({smtp_port}): {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute a command on hosts with open SMTP ports or a specific server.")
    parser.add_argument("--file", help="Path to the Nmap XML file")
    parser.add_argument("--to-internal", help="Target to send emails to internally")
    parser.add_argument("--from-internal", help="Internal source email address to spoof messages from")
    parser.add_argument("--to-external", help="Target to send emails to externally")
    parser.add_argument("--from-external", help="External source email address to spoof messages from")
    parser.add_argument("--subject", help="Email subject")
    parser.add_argument("--body", help="Message body for the email")
    parser.add_argument("--prompt", action="store_true", help="Prompt before executing each command")

    args = parser.parse_args()

    nmap_xml_file = args.file
    to_internal = args.to_internal
    from_internal = args.from_internal
    subject = args.subject
    body = args.body
    from_external = args.from_external
    to_external = args.to_external
    prompt = args.prompt

    try:
        if nmap_xml_file:
            smtp_hosts = parse_nmap_xml(nmap_xml_file)
            if smtp_hosts:
                execute_command_on_smtp_hosts(smtp_hosts, to_internal, from_internal, prompt)
            else:
                print("No hosts with SMTP open found in the Nmap file.")
        elif server:
            print("When specifying a single server, please provide an Nmap file to identify SMTP hosts.")
        else:
            print("The --file parameter must be specified.")
    except Exception as e:
        print(f"Error: {e}")
