#!/usr/bin/env python3
"""
Termius SSH Setup for GenX Trading Platform
Generates SSH keys and configures Termius connection
"""

import os
import subprocess
import json
from pathlib import Path

def generate_ssh_key():
    """Generate SSH key pair for GenX Trading"""
    print("🔑 Generating SSH Key for GenX Trading Platform...")
    
    # Create SSH directory
    ssh_dir = Path.home() / ".ssh"
    ssh_dir.mkdir(exist_ok=True)
    
    # Key paths
    key_name = "genx_trading_ed25519"
    private_key = ssh_dir / key_name
    public_key = ssh_dir / f"{key_name}.pub"
    
    # Generate key if not exists
    if not private_key.exists():
        cmd = [
            "ssh-keygen",
            "-t", "ed25519",
            "-C", "genxapitrading@gmail.com",
            "-f", str(private_key),
            "-N", ""  # No passphrase
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("✅ SSH key generated successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ SSH key generation failed: {e.stderr}")
            return None, None
        except FileNotFoundError:
            print("❌ ssh-keygen not found. Using alternative method...")
            return generate_ssh_key_windows()
    else:
        print("✅ SSH key already exists")
    
    # Read keys
    try:
        with open(public_key, 'r') as f:
            pub_key_content = f.read().strip()
        
        with open(private_key, 'r') as f:
            priv_key_content = f.read().strip()
            
        return pub_key_content, priv_key_content
    except Exception as e:
        print(f"❌ Error reading SSH keys: {e}")
        return None, None

def generate_ssh_key_windows():
    """Alternative SSH key generation for Windows"""
    print("🔧 Using Windows alternative SSH key generation...")
    
    try:
        # Use PowerShell to generate SSH key
        powershell_cmd = """
        $sshDir = "$env:USERPROFILE\\.ssh"
        if (!(Test-Path $sshDir)) { New-Item -ItemType Directory -Path $sshDir -Force }
        
        $keyPath = "$sshDir\\genx_trading_ed25519"
        if (!(Test-Path $keyPath)) {
            ssh-keygen -t ed25519 -C "genxapitrading@gmail.com" -f $keyPath -N '""'
        }
        
        $pubKey = Get-Content "$keyPath.pub"
        $privKey = Get-Content $keyPath
        
        Write-Output "PUBLIC_KEY:$pubKey"
        Write-Output "PRIVATE_KEY_START"
        $privKey | ForEach-Object { Write-Output $_ }
        Write-Output "PRIVATE_KEY_END"
        """
        
        result = subprocess.run(
            ["powershell", "-Command", powershell_cmd],
            capture_output=True, text=True, check=True
        )
        
        output_lines = result.stdout.strip().split('\n')
        
        # Extract keys from output
        pub_key = None
        priv_key_lines = []
        in_private_key = False
        
        for line in output_lines:
            if line.startswith("PUBLIC_KEY:"):
                pub_key = line[11:]  # Remove "PUBLIC_KEY:" prefix
            elif line == "PRIVATE_KEY_START":
                in_private_key = True
            elif line == "PRIVATE_KEY_END":
                in_private_key = False
            elif in_private_key:
                priv_key_lines.append(line)
        
        priv_key = '\n'.join(priv_key_lines)
        return pub_key, priv_key
        
    except Exception as e:
        print(f"❌ Windows SSH key generation failed: {e}")
        return None, None

def create_termius_config(public_key, private_key):
    """Create Termius configuration"""
    print("📋 Creating Termius Configuration...")
    
    # Termius host configuration
    termius_config = {
        "host": {
            "name": "GenX Trading VPS",
            "hostname": "[TO_BE_SET_AFTER_VPS_DEPLOYMENT]",
            "port": 22,  # Standard SSH port (not 8080 for SSH)
            "username": "root",
            "authentication": "ssh_key"
        },
        "ssh_key": {
            "name": "GenX Trading ED25519",
            "type": "ed25519",
            "public_key": public_key,
            "private_key": private_key,
            "comment": "genxapitrading@gmail.com"
        },
        "connection_info": {
            "original_termius_url_port": 8080,
            "note": "Original Termius URL used port 8080, but SSH should use port 22"
        }
    }
    
    # Save configuration
    config_file = Path("termius_genx_config.json")
    with open(config_file, 'w') as f:
        json.dump(termius_config, f, indent=2)
    
    print(f"✅ Termius config saved to: {config_file}")
    return termius_config

def create_ssh_config():
    """Create SSH config file entry"""
    print("📝 Creating SSH Config Entry...")
    
    ssh_config = """
# GenX Trading VPS Configuration
Host genx-trading-vps
    HostName [VPS_IP_TO_BE_SET]
    Port 22
    User root
    IdentityFile ~/.ssh/genx_trading_ed25519
    IdentitiesOnly yes
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null

# Alternative with username ubuntu (for Ubuntu VPS)
Host genx-trading-ubuntu
    HostName [VPS_IP_TO_BE_SET]
    Port 22
    User ubuntu
    IdentityFile ~/.ssh/genx_trading_ed25519
    IdentitiesOnly yes
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
"""
    
    # Save SSH config
    with open("ssh_config_genx.txt", 'w') as f:
        f.write(ssh_config)
    
    print("✅ SSH config saved to: ssh_config_genx.txt")
    print("📋 Add this to your ~/.ssh/config file")

def display_termius_setup_instructions(config):
    """Display step-by-step Termius setup instructions"""
    print("\n" + "="*60)
    print("🚀 TERMIUS SETUP INSTRUCTIONS")
    print("="*60)
    
    print("\n📱 Step 1: Add Host in Termius")
    print("-" * 30)
    print(f"Host Name: {config['host']['name']}")
    print(f"Address: [SET AFTER VPS DEPLOYMENT]")
    print(f"Port: {config['host']['port']}")
    print(f"Username: {config['host']['username']}")
    
    print("\n🔑 Step 2: Add SSH Key in Termius")
    print("-" * 30)
    print(f"Key Name: {config['ssh_key']['name']}")
    print(f"Key Type: {config['ssh_key']['type'].upper()}")
    print("\nPublic Key:")
    print("-" * 20)
    print(config['ssh_key']['public_key'])
    print("-" * 20)
    
    print("\n⚠️  Step 3: Private Key")
    print("-" * 30)
    print("Private key saved in termius_genx_config.json")
    print("Import this into Termius when setting up the key pair")
    
    print("\n🌐 Step 4: After VPS Deployment")
    print("-" * 30)
    print("1. Get your VPS IP address from deployment")
    print("2. Update Termius host address")
    print("3. Test connection")
    
    print("\n✅ Connection Test Command:")
    print("ssh -i ~/.ssh/genx_trading_ed25519 root@[VPS_IP]")

def main():
    """Main setup function"""
    print("🚀 GenX Trading Platform - Termius SSH Setup")
    print("=" * 55)
    
    # Generate SSH keys
    public_key, private_key = generate_ssh_key()
    
    if not public_key or not private_key:
        print("❌ Failed to generate SSH keys")
        return False
    
    # Create configurations
    config = create_termius_config(public_key, private_key)
    create_ssh_config()
    
    # Display setup instructions
    display_termius_setup_instructions(config)
    
    print("\n🎯 Next Steps:")
    print("1. ✅ SSH keys generated")
    print("2. ✅ Termius config created") 
    print("3. 📋 Import keys into Termius app")
    print("4. 🚀 Deploy VPS and get IP address")
    print("5. 🔗 Update Termius with VPS IP")
    print("6. ✅ Connect to GenX Trading VPS!")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Termius SSH setup completed successfully!")
    else:
        print("\n❌ Termius SSH setup failed!")