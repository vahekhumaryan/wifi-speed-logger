package main

import (
	"os/exec"
	"runtime"
	"strings"
)

// GetConnectionType detects the current network connection type (Wi-Fi, Ethernet, etc.)
func GetConnectionType() string {
	switch runtime.GOOS {
	case "darwin":
		return getConnectionTypeDarwin()
	case "linux":
		return getConnectionTypeLinux()
	case "windows":
		return getConnectionTypeWindows()
	default:
		return "Unknown"
	}
}

// GetWiFiSSID retrieves the current Wi-Fi network name.
func GetWiFiSSID() string {
	switch runtime.GOOS {
	case "darwin":
		return getWiFiSSIDDarwin()
	case "linux":
		return getWiFiSSIDLinux()
	case "windows":
		return getWiFiSSIDWindows()
	default:
		return "Unknown"
	}
}

// macOS implementations

func getConnectionTypeDarwin() string {
	out, err := exec.Command("route", "get", "default").Output()
	if err != nil {
		return "Unknown"
	}

	var iface string
	for _, line := range strings.Split(string(out), "\n") {
		line = strings.TrimSpace(line)
		if strings.HasPrefix(line, "interface:") {
			iface = strings.TrimSpace(strings.TrimPrefix(line, "interface:"))
			break
		}
	}
	if iface == "" {
		return "Unknown"
	}

	// Check if it's a Wi-Fi interface
	out, err = exec.Command("networksetup", "-listallhardwareports").Output()
	if err != nil {
		return "Unknown"
	}

	lines := strings.Split(string(out), "\n")
	for i, line := range lines {
		if strings.Contains(line, "Device: "+iface) && i > 0 {
			portLine := lines[i-1]
			if strings.Contains(portLine, "Wi-Fi") {
				return "Wi-Fi"
			}
			if strings.Contains(portLine, "Ethernet") || strings.Contains(portLine, "Thunderbolt") {
				return "Ethernet"
			}
			return strings.TrimPrefix(portLine, "Hardware Port: ")
		}
	}
	return "Unknown"
}

func getWiFiSSIDDarwin() string {
	out, err := exec.Command("system_profiler", "SPAirPortDataType").Output()
	if err != nil {
		return "N/A"
	}

	inCurrentNetwork := false
	for _, line := range strings.Split(string(out), "\n") {
		trimmed := strings.TrimSpace(line)
		if trimmed == "Current Network Information:" {
			inCurrentNetwork = true
			continue
		}
		if inCurrentNetwork && strings.HasSuffix(trimmed, ":") && !strings.Contains(trimmed, " ") {
			return strings.TrimSuffix(trimmed, ":")
		}
	}
	return "N/A"
}

// Linux implementations

func getConnectionTypeLinux() string {
	out, err := exec.Command("nmcli", "-t", "-f", "TYPE", "connection", "show", "--active").Output()
	if err != nil {
		return "Unknown"
	}

	connType := strings.TrimSpace(strings.Split(string(out), "\n")[0])
	switch {
	case strings.Contains(connType, "wireless") || strings.Contains(connType, "wifi"):
		return "Wi-Fi"
	case strings.Contains(connType, "ethernet"):
		return "Ethernet"
	default:
		return connType
	}
}

func getWiFiSSIDLinux() string {
	out, err := exec.Command("nmcli", "-t", "-f", "active,ssid", "dev", "wifi").Output()
	if err != nil {
		return "N/A"
	}

	for _, line := range strings.Split(string(out), "\n") {
		if strings.HasPrefix(line, "yes:") {
			return strings.TrimPrefix(line, "yes:")
		}
	}
	return "N/A"
}

// Windows implementations

func getConnectionTypeWindows() string {
	out, err := exec.Command("netsh", "interface", "show", "interface").Output()
	if err != nil {
		return "Unknown"
	}

	for _, line := range strings.Split(string(out), "\n") {
		if strings.Contains(line, "Connected") {
			if strings.Contains(line, "Wi-Fi") || strings.Contains(line, "Wireless") {
				return "Wi-Fi"
			}
			if strings.Contains(line, "Ethernet") {
				return "Ethernet"
			}
		}
	}
	return "Unknown"
}

func getWiFiSSIDWindows() string {
	out, err := exec.Command("netsh", "wlan", "show", "interfaces").Output()
	if err != nil {
		return "N/A"
	}

	for _, line := range strings.Split(string(out), "\n") {
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, "SSID") && !strings.Contains(trimmed, "BSSID") {
			parts := strings.SplitN(trimmed, ":", 2)
			if len(parts) == 2 {
				return strings.TrimSpace(parts[1])
			}
		}
	}
	return "N/A"
}
