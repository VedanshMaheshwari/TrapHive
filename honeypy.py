# Import library dependencies.
import argparse
import threading
import time
# Import project python file dependencies.
from ssh_honeypot import *
from web_honeypot import *

def start_ssh_honeypot(address, port, username, password, tarpit):
    print(f"[-] Running SSH Honeypot on {address}:{port}")
    honeypot(address, port, username, password, tarpit)

def start_http_honeypot(port, username, password):
    print(f'[-] Running HTTP Wordpress Honeypot on port {port}')
    # Use threaded=False to avoid the signal handler issue
    app = baseline_web_honeypot(input_username=username, input_password=password)
    app.run(debug=False, port=port, host="0.0.0.0", threaded=True, use_reloader=False)

def start_dashboard(port):
    try:
        # Import dashboard components only when needed - without wildcard imports
        import dashboard_data_parser
        from web_app import app as dashboard_app
        print(f'[-] Running Dashboard on port {port}')
        dashboard_app.run(debug=False, host="0.0.0.0", port=port, threaded=True, use_reloader=False)
    except ImportError as e:
        print(f"[!] Error loading dashboard: {e}")
        print("[!] To use the dashboard, install required packages with:")
        print("    pip install dash dash-bootstrap-components dash-bootstrap-templates plotly")

if __name__ == "__main__":
    # Create parser and add arguments.
    parser = argparse.ArgumentParser() 
    parser.add_argument('-a','--address', type=str, required=True)
    parser.add_argument('-sp','--ssh_port', type=int, help='Port for SSH honeypot')
    parser.add_argument('-wp','--web_port', type=int, help='Port for HTTP honeypot')
    parser.add_argument('-dp','--dashboard_port', type=int, help='Port for Dashboard')
    parser.add_argument('-u', '--username', type=str)
    parser.add_argument('-pw', '--password', type=str)
    parser.add_argument('-s', '--ssh', action="store_true", help='Enable SSH honeypot')
    parser.add_argument('-t', '--tarpit', action="store_true")
    parser.add_argument('-wh', '--http', action="store_true", help='Enable HTTP honeypot')
    parser.add_argument('-d', '--dashboard', action="store_true", help='Enable Dashboard')
    
    args = parser.parse_args()
    
    threads = []
    
    # Parse the arguments based on user-supplied argument.
    try:
        if not args.ssh and not args.http and not args.dashboard:
            print("[!] You must choose at least one: SSH (-s), HTTP (-wh), or Dashboard (-d)")
            exit(1)
            
        if args.ssh:
            if not args.ssh_port:
                print("[!] SSH honeypot requires a port (use -sp or --ssh_port)")
                exit(1)
            # Create SSH honeypot thread
            ssh_thread = threading.Thread(
                target=start_ssh_honeypot, 
                args=(args.address, args.ssh_port, args.username, args.password, args.tarpit)
            )
            threads.append(ssh_thread)

        if args.http:
            if not args.web_port:
                print("[!] HTTP honeypot requires a port (use -wp or --web_port)")
                exit(1)
                
            # Set default credentials for HTTP honeypot if not provided
            http_username = args.username if args.username else "admin"
            http_password = args.password if args.password else "deeboodah"
            print(f"[-] HTTP honeypot using username: {http_username}, password: {http_password}")
            
            # For HTTP, we'll handle it differently due to Flask threading issues
            if len(threads) == 0:  # If no other services are running
                # Run directly in the main thread
                start_http_honeypot(args.web_port, http_username, http_password)
            else:
                # Create HTTP honeypot thread
                http_thread = threading.Thread(
                    target=start_http_honeypot, 
                    args=(args.web_port, http_username, http_password)
                )
                threads.append(http_thread)
            
        if args.dashboard:
            if not args.dashboard_port:
                print("[!] Dashboard requires a port (use -dp or --dashboard_port)")
                exit(1)
                
            # Create Dashboard thread
            dashboard_thread = threading.Thread(
                target=start_dashboard, 
                args=(args.dashboard_port,)
            )
            threads.append(dashboard_thread)
        
        # Start all threads
        for thread in threads:
            thread.daemon = True  # This ensures threads exit when main program exits
            thread.start()
            
        # Keep main thread running to prevent program from exiting immediately
        print("[+] All services started. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nProgram exited.")