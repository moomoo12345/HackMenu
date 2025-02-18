#!/bin/bash

# Import color definitions
source "$(dirname "$0")/Tool/Colors"

# Configuration
declare -A CONFIG=(
    ["VERSION"]="2.7.4"
    ["INSTALL_DIR"]="/opt/security-toolkit"
    ["DATA_DIR"]="$HOME/.security_toolkit"
    ["LOG_DIR"]="/var/log/security_toolkit"
    ["BACKUP_DIR"]="$HOME/.security_toolkit/backup"
)

# Tool categories for cleanup
declare -A TOOLS=(
    ["network"]="nmap wireshark tcpdump netcat"
    ["web"]="dirb nikto burpsuite sqlmap"
    ["forensics"]="volatility autopsy sleuthkit"
    ["crypto"]="john hashcat hydra"
)

# Function to display banner
display_banner() {
    clear
    print_gradient "Security Toolkit Uninstaller v${CONFIG[VERSION]}"
    print_color "CYAN" "Removing Security Tools..."
    echo
}

# Function to backup configuration
backup_config() {
    print_info "Backing up configuration..."
    
    local backup_dir="${CONFIG[BACKUP_DIR]}/config_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    if [[ -d "${CONFIG[DATA_DIR]}" ]]; then
        cp -r "${CONFIG[DATA_DIR]}/config.yml" "$backup_dir/"
        cp -r "${CONFIG[DATA_DIR]}/profiles" "$backup_dir/" 2>/dev/null || true
    fi
}

# Function to remove installed tools
remove_tools() {
    print_info "Removing installed tools..."
    
    if command -v apt-get >/dev/null; then
        for category in "${!TOOLS[@]}"; do
            print_info "Removing $category tools..."
            sudo apt-get remove -y ${TOOLS[$category]} 2>/dev/null || true
        done
        sudo apt-get autoremove -y
    elif command -v yum >/dev/null; then
        for category in "${!TOOLS[@]}"; do
            print_info "Removing $category tools..."
            sudo yum remove -y ${TOOLS[$category]} 2>/dev/null || true
        done
        sudo yum autoremove -y
    fi
}

# Function to remove Python packages
remove_python_packages() {
    print_info "Removing Python packages..."
    
    if [[ -f "requirements.txt" ]]; then
        while read -r package; do
            pip3 uninstall -y "$package" 2>/dev/null || true
        done < "requirements.txt"
    fi
}

# Function to remove directories
remove_directories() {
    print_info "Removing toolkit directories..."
    
    local dirs=(
        "${CONFIG[INSTALL_DIR]}"
        "${CONFIG[DATA_DIR]}"
        "${CONFIG[LOG_DIR]}"
    )
    
    for dir in "${dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            print_info "Removing $dir..."
            rm -rf "$dir"
        fi
    done
}

# Function to remove system configurations
remove_system_configs() {
    print_info "Removing system configurations..."
    
    # Remove systemd service if exists
    if [[ -f "/etc/systemd/system/security-toolkit.service" ]]; then
        sudo systemctl stop security-toolkit 2>/dev/null || true
        sudo systemctl disable security-toolkit 2>/dev/null || true
        sudo rm -f "/etc/systemd/system/security-toolkit.service"
        sudo systemctl daemon-reload
    fi
    
    # Remove bash completion
    sudo rm -f "/etc/bash_completion.d/security-toolkit"
    
    # Remove man pages
    sudo rm -f "/usr/share/man/man1/security-toolkit.1"
}

# Function to verify uninstallation
verify_uninstallation() {
    print_info "Verifying uninstallation..."
    
    local failed=0
    
    # Check if directories are removed
    for dir in "${CONFIG[INSTALL_DIR]}" "${CONFIG[DATA_DIR]}" "${CONFIG[LOG_DIR]}"; do
        if [[ -d "$dir" ]]; then
            print_error "Directory still exists: $dir"
            ((failed++))
        fi
    done
    
    # Check if services are removed
    if systemctl list-units --full -all | grep -Fq "security-toolkit"; then
        print_error "Service still exists"
        ((failed++))
    fi
    
    if [[ $failed -eq 0 ]]; then
        print_success "Uninstallation verified successfully"
        return 0
    else
        print_error "Uninstallation verification failed"
        return 1
    fi
}

# Function to clean environment
clean_environment() {
    print_info "Cleaning environment..."
    
    # Remove environment variables
    unset SECURITY_TOOLKIT_*
    
    # Remove aliases
    unalias security-toolkit 2>/dev/null || true
    
    # Clean shell history
    history -c
    
    # Remove temporary files
    rm -rf /tmp/security-toolkit-*
}

# Main uninstallation function
main() {
    display_banner
    
    # Check if running as root
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root"
        exit 1
    fi
    
    # Confirm uninstallation
    print_warning "This will remove all toolkit components and data"
    read -p "Continue with uninstallation? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Uninstallation cancelled"
        exit 0
    fi
    
    # Uninstallation steps
    backup_config
    remove_tools
    remove_python_packages
    remove_directories
    remove_system_configs
    clean_environment
    verify_uninstallation
    
    print_success "Uninstallation completed successfully!"
}

# Error handling
set -e
trap 'print_error "Uninstallation failed at line $LINENO"' ERR

# Start uninstallation
main "$@" 