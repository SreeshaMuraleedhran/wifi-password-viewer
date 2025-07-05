import subprocess

# Get list of saved Wi-Fi profiles
profiles_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
profiles_data = profiles_data.decode('utf-8', errors="backslashreplace").split('\n')

profiles = []
for line in profiles_data:
    if "All User Profile" in line:
        profile = line.split(":")[1].strip()
        profiles.append(profile)

# Print the header
print("{:<30}| {:<}".format("Wi-Fi Name", "Password"))
print("-" * 45)

# Loop through profiles to get passwords
for profile in profiles:
    try:
        profile_info = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'])
        profile_info = profile_info.decode('utf-8', errors="backslashreplace").split('\n')
        
        password_line = [line.split(":")[1].strip() for line in profile_info if "Key Content" in line]
        
        password = password_line[0] if password_line else ""
        print("{:<30}| {:<}".format(profile, password))
    
    except subprocess.CalledProcessError:
        print("{:<30}| {:<}".format(profile, "Error retrieving password"))
