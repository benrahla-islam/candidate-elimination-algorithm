#define MyAppName "Candidate Elimination Algorithm Tool"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "AI Learning Project"
#define MyAppExeName "CandidateEliminationTool.exe"
#define MyAppURL "https://github.com/yourname/candidate-elimination-tool"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{C4E5A8B2-9D3F-4A7E-8B2C-1E9F6D4A5C8B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=
InfoBeforeFile=
InfoAfterFile=
OutputDir=installer_output
OutputBaseFilename=CandidateEliminationTool_Setup_{#MyAppVersion}
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
; Main application files
Source: "app.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "main.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

; Sample data files
Source: "data.csv"; DestDir: "{app}\sample_data"; Flags: ignoreversion
Source: "driving_behavior.csv"; DestDir: "{app}\sample_data"; Flags: ignoreversion
Source: "test_data.csv"; DestDir: "{app}\sample_data"; Flags: ignoreversion

; Python embedded distribution (if included)
Source: "python_embedded\*"; DestDir: "{app}\python"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: PythonEmbeddedExists

; Batch file to run the application
Source: "run_app.bat"; DestDir: "{app}"; Flags: ignoreversion

; License and documentation
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "CHANGELOG.md"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\run_app.bat"; IconFilename: "{app}\app.ico"; WorkingDir: "{app}"; Comment: "Run Candidate Elimination Algorithm Tool"
Name: "{group}\Sample Data Folder"; Filename: "{app}\sample_data"; Comment: "Sample CSV files for testing"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\run_app.bat"; IconFilename: "{app}\app.ico"; WorkingDir: "{app}"; Tasks: desktopicon; Comment: "Run Candidate Elimination Algorithm Tool"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\run_app.bat"; Tasks: quicklaunchicon; WorkingDir: "{app}"

[Dirs]
Name: "{app}\results"; Permissions: users-modify
Name: "{app}\sample_data"
Name: "{app}\logs"; Permissions: users-modify

[Run]
Filename: "{app}\run_app.bat"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent shellexec

[Code]
function PythonEmbeddedExists: Boolean;
begin
  Result := DirExists(ExpandConstant('{src}\python_embedded'));
end;

function PythonInstalled: Boolean;
var
  ResultCode: Integer;
begin
  Result := Exec('python', '--version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0);
end;

function GetPythonPath: String;
var
  PythonPath: String;
  ResultCode: Integer;
begin
  if Exec('where', 'python', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    // This is a simplified approach - in practice you'd want to capture the output
    Result := 'python';
  end
  else
    Result := '';
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
  PythonCmd: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Install Python dependencies if Python is available
    if PythonInstalled then
    begin
      PythonCmd := 'python';
      if not PythonEmbeddedExists then
      begin
        // Install required packages
        Exec(PythonCmd, '-m pip install pandas', ExpandConstant('{app}'), SW_SHOW, ewWaitUntilTerminated, ResultCode);
        Exec(PythonCmd, '-m pip install tk', ExpandConstant('{app}'), SW_SHOW, ewWaitUntilTerminated, ResultCode);
      end;
    end;
  end;
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
  
  // Check if Python is installed
  if not PythonInstalled and not PythonEmbeddedExists then
  begin
    if MsgBox('Python is not detected on your system. This application requires Python 3.7 or later.' + #13#10 + #13#10 + 
              'Would you like to continue the installation anyway?' + #13#10 + 
              '(You will need to install Python manually later)', 
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;
end;

[Messages]
WelcomeLabel2=This will install [name/ver] on your computer.%n%nThis application provides a professional GUI for the Candidate Elimination Algorithm, allowing you to process CSV data and visualize learning results.%n%nIt is recommended that you close all other applications before continuing.

[CustomMessages]
PythonNotFound=Python not found. Please install Python 3.7+ from https://python.org
PythonFound=Python installation detected
DependenciesInstalling=Installing Python dependencies...
DependenciesInstalled=Dependencies installed successfully