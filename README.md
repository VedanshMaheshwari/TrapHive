# TrapHive

TrapHive is a modular honeypot framework designed to collect and analyze attack patterns through simulated SSH and HTTP (WordPress) vulnerable services. This tool enables security researchers and professionals to gather threat intelligence by monitoring attacker behavior in a controlled environment.

![TrapHive Logo](assets/images/honeypy-logo-white.png)

## Features

- **SSH Honeypot**: Emulates an SSH server that captures login credentials and records executed commands
- **HTTP Honeypot**: Simulates a WordPress admin login page to track web-based attacks
- **Interactive Dashboard**: Visualizes attack data including:
  - Top attacker IP addresses
  - Most common usernames and passwords
  - Frequently used commands
  - Geographic distribution of attacks (optional)
- **Tarpit Mode**: Capability to slow down attackers and waste their resources
- **Configurable Authentication**: Choose between logging all attempts or specific credential sets

## Prerequisites

- Python 3.7+
- Required Python packages (see [Installation](#installation))
- Internet connection (for country code lookup - optional)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TrapHive.git
   cd TrapHive
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Linux/Mac
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Generate an SSH key for the honeypot:
   ```bash
   mkdir -p ssh_honeypy/static
   ssh-keygen -t rsa -b 2048 -f ssh_honeypy/static/server.key
   # When prompted, don't set a passphrase (just press Enter)
   ```

5. Create log directories:
   ```bash
   mkdir -p ssh_honeypy/log_files
   ```

## Usage

TrapHive can run its SSH honeypot, HTTP honeypot, and Dashboard components independently or simultaneously.

### Basic Usage

```bash
# Run SSH honeypot on localhost:2222
python honeypy.py -a 127.0.0.1 -sp 2222 -s

# Run HTTP honeypot on port 8080
python honeypy.py -a 127.0.0.1 -wp 8080 -wh

# Run the dashboard on port 8050
python honeypy.py -a 127.0.0.1 -dp 8050 -d

# Run all components together
python honeypy.py -a 127.0.0.1 -sp 2222 -s -wp 8080 -wh -dp 8050 -d
```

### Command-Line Arguments

| Argument | Description |
|----------|-------------|
| `-a`, `--address` | IP address to bind services to (required) |
| `-sp`, `--ssh_port` | Port for SSH honeypot |
| `-wp`, `--web_port` | Port for HTTP honeypot |
| `-dp`, `--dashboard_port` | Port for Dashboard |
| `-u`, `--username` | Username for authentication (default: none for SSH, "admin" for HTTP) |
| `-w`, `--password` | Password for authentication (default: none for SSH, "deeboodah" for HTTP) |
| `-s`, `--ssh` | Enable SSH honeypot |
| `-t`, `--tarpit` | Enable tarpit mode (slows down attackers) |
| `-wh`, `--http` | Enable HTTP honeypot |
| `-d`, `--dashboard` | Enable Dashboard |

### Example Scenarios

1. **SSH Honeypot with custom credentials**:
   ```bash
   python honeypy.py -a 0.0.0.0 -sp 2222 -u root -w password123 -s
   ```

2. **HTTP Honeypot with tarpit mode**:
   ```bash
   python honeypy.py -a 0.0.0.0 -wp 8080 -u admin -w password123 -wh -t
   ```

3. **Full deployment on a server**:
   ```bash
   python honeypy.py -a 0.0.0.0 -sp 22 -wp 80 -dp 8050 -s -wh -d
   ```

## Architecture

TrapHive consists of three main components:

1. **SSH Honeypot** (`ssh_honeypot.py`)
   - Uses Paramiko to implement SSH server functionality
   - Logs authentication attempts and command execution
   - Provides an emulated shell environment

2. **HTTP Honeypot** (`web_honeypot.py`)
   - Uses Flask to create a web server
   - Simulates a WordPress admin login page
   - Logs login attempts

3. **Dashboard** (`web_app.py` and `dashboard_data_parser.py`)
   - Built with Dash and Plotly
   - Visualizes attack data in real-time
   - Displays tables of captured credentials

## Logging

TrapHive generates several log files in the `ssh_honeypy/log_files/` directory:

- `creds_audits.log`: SSH login attempts (IP address, username, password)
- `cmd_audits.log`: Commands executed by attackers
- `http_audit.log`: HTTP login attempts

## Dashboard

The dashboard provides visual analytics of attack data and can be accessed by navigating to `http://[your-server-ip]:[dashboard-port]` in a web browser.

![Dashboard Screenshot](assets/images/dashboard-screenshot.png)

## Security Considerations

- **Do not** run TrapHive on production systems without proper isolation
- Consider running the honeypot in a dedicated virtual machine or container
- Be aware that honeypots can attract malicious traffic to your network
- Review and comply with local laws regarding network monitoring and entrapment

## Customization

### Country Code Lookup

Edit the `public.env` file to enable or disable country code lookup:

```
COUNTRY=True  # Enable country lookup
COUNTRY=False  # Disable country lookup
```

### Emulated Commands

You can customize the emulated shell responses by modifying the `emulated_shell` function in `ssh_honeypot.py`.

## Development

### Project Structure

```
TrapHive/
├── honeypy.py            # Main entry point
├── ssh_honeypot.py       # SSH honeypot implementation
├── web_honeypot.py       # HTTP honeypot implementation
├── web_app.py            # Dashboard application
├── dashboard_data_parser.py  # Data processing for dashboard
├── templates/            # HTML templates for HTTP honeypot
│   └── wp-admin.html     # WordPress login page template
├── assets/               # Static assets for dashboard
│   └── images/           # Images used in the application
├── ssh_honeypy/          # Runtime directory
│   ├── static/           # SSH keys
│   └── log_files/        # Log storage
├── requirements.txt      # Python dependencies
└── public.env            # Environment configuration
```

## Troubleshooting

### Common Issues

1. **Port binding error**: Make sure the ports you're using are not already in use and you have sufficient permissions.

   Solution: Use different ports or run with elevated privileges.

2. **Missing templates**: If you see template errors, check that the directory structure is correct.

   Solution: Verify the `templates` folder is in the same directory as `web_honeypot.py`.

3. **Dashboard not showing data**: This could be due to empty log files.

   Solution: Generate some test data by attempting logins to the honeypots.

## Future Enhancements

- FTP honeypot implementation
- SMTP honeypot implementation
- Integration with threat intelligence platforms
- Machine learning-based attack pattern recognition
- Attack simulation based on collected data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Paramiko](https://www.paramiko.org/) for SSH protocol implementation
- [Flask](https://flask.palletsprojects.com/) for HTTP server functionality
- [Dash](https://dash.plotly.com/) for the analytics dashboard
