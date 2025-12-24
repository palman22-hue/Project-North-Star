[Setup]
AppName=PDA Agent
AppVersion=1.0
DefaultDirName={pf}\PDA_Agent
DefaultGroupName=PDA Agent
OutputDir=.
OutputBaseFilename=PDA_Agent_Installer
Compression=lzma
SolidCompression=yes

[Files]
; Hoofdbestanden
Source: "api.py"; DestDir: "{app}"
Source: "main.py"; DestDir: "{app}"
Source: "cli.py"; DestDir: "{app}"
Source: "engine.py"; DestDir: "{app}"
Source: "ethics.py"; DestDir: "{app}"
Source: "gpu_test.py"; DestDir: "{app}"
Source: "pda_mistral.py"; DestDir: "{app}"
Source: "pda32d_base.py"; DestDir: "{app}"
Source: "agent_state.py"; DestDir: "{app}"
Source: "emotion_probe.py"; DestDir: "{app}"
Source: "session_logger.py"; DestDir: "{app}"
Source: "requirements.txt"; DestDir: "{app}"
Source: "README.md"; DestDir: "{app}"
Source: "pda_agent_gui.ps1"; DestDir: "{app}"
Source: "pda_launcher.ps1"; DestDir: "{app}"
Source: "PDA_Agent_Installer.iss"; DestDir: "{app}"
Source: "logo.PNG"; DestDir: "{app}"

; Configuratiebestanden
Source: ".env"; DestDir: "{app}"
Source: ".webui_secret_key"; DestDir: "{app}"

; JSON logs
Source: "emotion_probe_log.jsonl"; DestDir: "{app}"
Source: "session_log.jsonl"; DestDir: "{app}"

; Submappen
Source: "core\*"; DestDir: "{app}\core"; Flags: recursesubdirs
Source: "static\*"; DestDir: "{app}\static"; Flags: recursesubdirs
Source: "Backup\*"; DestDir: "{app}\Backup"; Flags: recursesubdirs


[Icons]
Name: "{group}\PDA Agent"; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\pda_agent_gui.ps1"""
Name: "{commondesktop}\PDA Agent"; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\pda_agent_gui.ps1"""

[Run]
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\pda_agent_gui.ps1"""; Flags: postinstall nowait
