; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "ImageDiff"
#define MyAppVersion "1.0"
#define MyAppPublisher "TestPlant UK Ltd"
#define MyAppURL "http://www.testplant.com/"
#define MyAppExeName "ImageDiff.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{0CC8EFC6-946B-49EA-B044-42626321A22B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputBaseFilename=ImageDiff_Setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Source: "vcredist_x86_2010.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: "vcredist_x86.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: ".\distwin32\imageDiff.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\distwin32\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\distwin32\bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\distwin32\PyQt4.QtCore.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\distwin32\PyQt4.QtGui.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\distwin32\python27.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\distwin32\QtCore4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\distwin32\QtGui4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\distwin32\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\distwin32\sip.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\distwin32\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\distwin32\imageformats\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: ".\distwin32\_socket.pyd"; DestDir: "{app}";
;NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{tmp}\vcredist_x86.exe"; Parameters: "/q"; Check: VCRedistNeedsInstall
; Filename: "{tmp}\vcredist_x86_2010.exe"; Parameters: "/q"
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
#IFDEF UNICODE
  #DEFINE AW "W"
#ELSE
  #DEFINE AW "A"
#ENDIF
type
  INSTALLSTATE = Longint;
const
  INSTALLSTATE_INVALIDARG = -2;  // An invalid parameter was passed to the function.
  INSTALLSTATE_UNKNOWN = -1;     // The product is neither advertised or installed.
  INSTALLSTATE_ADVERTISED = 1;   // The product is advertised but not installed.
  INSTALLSTATE_ABSENT = 2;       // The product is installed for a different user.
  INSTALLSTATE_DEFAULT = 5;      // The product is installed for the current user.

  VC_2008_REDIST_X86 = '{FF66E9F6-83E7-3A3E-AF14-8DE9A809A6A4}';
  VC_2008_SP1_REDIST_X86 = '{9A25302D-30C0-39D9-BD6F-21E6EC160475}';


function MsiQueryProductState(szProduct: string): INSTALLSTATE;
  external 'MsiQueryProductState{#AW}@msi.dll stdcall';

function VCVersionInstalled(const ProductID: string): Boolean;
begin
  Result := MsiQueryProductState(ProductID) = INSTALLSTATE_DEFAULT;
end;

function VCRedistNeedsInstall: Boolean;
begin
  Result := not (VCVersionInstalled(VC_2008_REDIST_X86) and VCVersionInstalled(VC_2008_SP1_REDIST_X86));
end;
