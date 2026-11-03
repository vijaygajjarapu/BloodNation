# Blood Nation

A blood donor and emergency blood-request platform. India first, designed for other countries later. It will ship as a responsive web app (with an installable web app), Android and iOS apps, and a separate web admin portal.

> **Status: workspace ready, local services blocked on the setup computer.** No application features exist yet. This README documents how to prepare a Windows computer and is updated as each setup step is completed and verified.
>
> Steps marked **(not yet verified)** were taken from official documentation but have not been confirmed on a real machine yet.

---

## 1. Approved technology

| AREA | CHOICE |
|---|---|
| Web app | React with Next.js, including the installable web app (PWA) |
| Admin portal | A separate React single-page app (Vite) |
| Backend | Python with Django |
| Background jobs | Celery with Redis |
| Database | PostgreSQL with PostGIS |
| Cache and job broker | Redis |
| Mobile | Flutter (Android and iOS, built together with the web) |
| Repository | One repository with clearly separated areas |
| JavaScript tooling | pnpm workspaces |
| Python tooling | uv |
| Local services | Docker Desktop (PostgreSQL with PostGIS, Redis, local S3-compatible storage) |
| Cloud (planned) | AWS. Hosting is still an open item. |

Outside services (SMS, email, push, maps, payments, file scanning, protected calling) are **mocked locally** so nothing paid is needed to start. Protected (masked) calling is a **placeholder only**, and no provider has been chosen.

## 2. Repository areas (names to be confirmed)

```
bloodnation/
├── backend/            Django server (managed with uv)
├── web/                Next.js website and installable web app
├── admin/              separate React (Vite) admin portal
├── mobile/             Flutter app for Android and iOS
├── shared/
│   ├── api-contract/   OpenAPI description of how the apps talk to the server
│   └── design-tokens/  shared colors, spacing and type sizes
├── docs/               Master Spec, architecture, decisions, open questions
├── infra/              local service configuration (database, cache)
├── scripts/            planned check and setup scripts
├── pnpm-workspace.yaml, package.json, .gitignore, .env.example
```

Each folder currently holds only a short placeholder file. No application code exists yet.

## 3. Windows setup (PowerShell)

### 3.1 Use PowerShell, not Command Prompt

Every command below is **PowerShell**. The prompt of a PowerShell window starts with `PS`, for example `PS C:\Users\you>`. A Command Prompt window shows `C:\Users\you>` with no `PS`, and it does not understand these commands.

To open PowerShell: press the Windows key, type **PowerShell**, and open **Windows PowerShell**. A normal window is enough unless a step says otherwise.

### 3.2 Check what is already installed (read-only)

Nothing here installs or changes anything. "NOT FOUND" simply means a tool is missing.

```powershell
"=== WINDOWS AND HARDWARE ==="
$env:PROCESSOR_ARCHITECTURE
(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory
(Get-CimInstance Win32_ComputerSystem).HypervisorPresent
(Get-CimInstance Win32_Processor).VirtualizationFirmwareEnabled
Get-PSDrive -Name C | Select-Object Used, Free

"=== GIT ==="
try { git --version } catch { "NOT FOUND" }

"=== NODE ==="
try { node --version } catch { "NOT FOUND" }

"=== PNPM ==="
try { pnpm --version } catch { "NOT FOUND" }

"=== UV ==="
try { uv --version } catch { "NOT FOUND" }

"=== DOCKER ==="
try { docker --version } catch { "NOT FOUND" }

"=== WSL ==="
try { wsl --status } catch { "NOT FOUND" }

"=== FLUTTER (optional) ==="
try { flutter --version } catch { "NOT FOUND" }

"=== ANDROID STUDIO AND SDK (optional) ==="
Test-Path "C:\Program Files\Android\Android Studio"
Test-Path "$env:LOCALAPPDATA\Android\Sdk"

"=== VS CODE (optional) ==="
try { code --version } catch { "NOT FOUND" }
```

Notes:
- `Get-ComputerInfo` is avoided on purpose, because it can take minutes on recent Windows 11 builds.
- Hardware virtualization must be turned **on in the BIOS/UEFI**. The line `VirtualizationFirmwareEnabled` should print `True`. `HypervisorPresent` may print `False` until WSL is installed, and that is fine.
- A Python message that points to the Microsoft Store is **not an error**. uv provides the Python the project needs, so do not install Python from the Store.

### 3.3 Install the tools, one at a time

Install in this order. After each tool, **close PowerShell and open a new window** before checking its version, because new tools only appear in new windows.

Before starting, move out of the project folder so nothing is created there by accident:

```powershell
cd $HOME
```

**Step 1: Git** (official source: https://git-scm.com/install/windows)

```powershell
winget --version
winget install --id Git.Git -e --source winget
```

Windows may ask for permission (choose Yes). Verify in a new window:

```powershell
git --version
```

**Step 2: pnpm** (official source: https://pnpm.io/installation)

pnpm's documentation currently recommends installing it through npm on Windows. Use the stable **11** line. `npm.cmd` is used on purpose to avoid a common Windows restriction on script files.

```powershell
npm.cmd install -g pnpm@latest-11
```

Verify in a new window:

```powershell
pnpm --version
```

**Step 3: uv** (official source: https://docs.astral.sh/uv/getting-started/installation/)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

The bypass setting applies to this single run only. Verify in a new window:

```powershell
uv --version
```

**Step 4: WSL** (official source: Microsoft Learn, "Install WSL")

> **WARNING: known boot problem on some computers. Read section 4.1 before running this step.** On one tested computer (Dell Inspiron 3558, Intel Core i3-5015U, Windows 10 Pro build 19045, BIOS A07 from 2015), `wsl --install` followed by the restart left Windows stuck on the blue recovery menu ("Continue / Use a device / Troubleshoot / Turn off your PC"). A System Restore fixed it. Not every computer is affected.

Docker Desktop on Windows normally runs on WSL 2. This step needs an **administrator** PowerShell window and a **restart**.

Before running it:
1. Save all work and make sure you know where your BitLocker recovery key is, if the disk is encrypted.
2. Make sure **System Protection** is on for drive C: (Windows search: "Create a restore point"), then create a restore point named "Before WSL". Without a restore point, System Restore cannot undo the install.
3. Have a phone or second computer nearby to read this README if the PC will not start.

```powershell
wsl --install
```

**Step 5: Docker Desktop** (not yet verified; official source: https://docs.docker.com/desktop/setup/install/windows-install.md)

Download the installer from the official page and choose the WSL 2 backend when asked. **Check Docker's licensing terms first.** Docker's documentation states that commercial use in larger enterprises (more than 250 employees or more than 10 million USD annual revenue) requires a paid subscription.

After installing, start Docker Desktop and verify:

```powershell
docker --version
```

**Later, only when needed:** VS Code (or any editor), Flutter, and Android Studio. Mobile tools are needed when mobile work begins, not to create the workspace.

### 3.4 Choose the project folder

Use a normal development folder on a fixed **NTFS** drive. Do not use the Downloads folder, a temporary folder, or a cloud-synced folder (such as OneDrive), because they can cause file-locking and sync errors.

Check a drive (replace `F` with your drive letter):

```powershell
Get-Volume -DriveLetter F | Select-Object DriveLetter, FileSystem, DriveType, HealthStatus, SizeRemaining, Size
```

You want `NTFS`, `Fixed` and `Healthy`. If the project folder already exists, look inside before using it:

```powershell
Get-ChildItem "<your-project-folder>" -Force
```

## 4. Troubleshooting

| SYMPTOM | CAUSE AND FIX |
|---|---|
| `'Get-ComputerInfo' is not recognized as an internal or external command` | You are in **Command Prompt**. Open Windows PowerShell and check that the prompt starts with `PS`. |
| Strange errors after pasting an error message | The error text was pasted into PowerShell as if it were a command. Paste only the commands. |
| A new tool is "not recognized" right after installing | Close the window and open a **new** PowerShell window. |
| `Get-ComputerInfo` seems stuck on "Loading hot-patch information" | It is slow on recent Windows 11. Press Ctrl+C and use the CIM commands in section 3.2. |
| "Running scripts is disabled on this system" (for example `pnpm.ps1 cannot be loaded`) | Do not change your security settings blindly. Either type `pnpm.cmd` instead of `pnpm`, or allow locally created scripts for your Windows user only with `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`. Undo with `-ExecutionPolicy Undefined`. |
| After `wsl --install` and a restart, Windows shows "Continue / Use a device / Troubleshoot / Turn off your PC" | See section 4.1. |
| Python message about the Microsoft Store | Not an error. uv installs the Python this project needs. |
| WSL or Docker will not start | Check that virtualization is enabled in the BIOS/UEFI, and restart after installing WSL. |

### 4.1 Known blocker: Windows will not start after `wsl --install`

**What happened.** On a Dell Inspiron 3558 (Intel Core i3-5015U, about 12 GB memory, Windows 10 Pro build 19045, BIOS A07 dated December 2015), `wsl --install` was run, the computer restarted, and Windows then showed only the blue recovery menu. "Continue" returned to the same menu. Choosing **Troubleshoot, Advanced options, System Restore** restored a working Windows. Personal files and the F: drive were not affected.

**Why it happens (honest status).** The exact cause on this computer is **not confirmed**. It is an Intel computer with a very old BIOS, so the AMD-specific reports below do not explain it. `wsl --install` turns on Windows virtualization features (Virtual Machine Platform and the Windows hypervisor), and the hypervisor loads at the next start. Public reports describe the same symptom on some computers and point at an unconfirmed interaction between the Windows hypervisor and certain hardware, BIOS or firmware versions, including AMD systems with SVM turned on and a few Dell and ASUS models. No official fix is known. Sources:
- [Microsoft Q&A: Automatic Repair after enabling WSL with AMD SVM enabled](https://learn.microsoft.com/en-us/answers/questions/5888212/windows-11-enters-automatic-repair-after-enabling)
- [WSL issue 14392: boot failures after enabling WSL 2 / Virtual Machine Platform](https://github.com/microsoft/WSL/issues/14392)
- [Windows 11 Forum: boot loop after enabling Virtual Machine Platform](https://www.elevenforum.com/t/windows-11-goes-into-boot-loop-after-enabling-virtual-machine-platform.41483/latest)

**Staged retry result (same computer).** The features were enabled one at a time, with a restart after each:
1. `dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart`, then restart: **Windows started normally.** The hypervisor stayed off (`HypervisorPresent` was `False`).
2. `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart`, then restart: **Windows did not start** and the recovery menu appeared again. System Restore fixed it.

So the **Virtual Machine Platform feature (which loads the Windows hypervisor) is what breaks the start-up on this computer.** The WSL feature alone is harmless. This also means anything that needs the hypervisor (WSL 2, Docker Desktop, the Android emulator) cannot be used on this computer until the cause is found. Before enabling Virtual Machine Platform on any computer, create a restore point.

**How to get out of it (safe, no data loss).**
1. Choose **Troubleshoot, then Advanced options, then System Restore** and pick the restore point from before the install.
2. If there is no restore point: try **Startup Repair**, then **Startup Settings, Restart, press 4** (Safe Mode), then **Uninstall Updates**.
3. Do **not** use "Reset this PC" or "Remove everything".
4. If asked for a BitLocker recovery key, find it at https://account.microsoft.com/devices/recoverykey.

**What to do afterwards.**
- Do **not** run `wsl --install` again and do **not** install Docker Desktop until the options below have been decided.
- Everything that needs virtualization is affected, not only WSL: Docker Desktop (WSL 2 or Hyper-V backend) and the Android emulator.
- Read-only checks to run before any retry (they change nothing):

```powershell
(Get-CimInstance Win32_Processor).Name
(Get-CimInstance Win32_BIOS) | Select-Object Manufacturer, SMBIOSBIOSVersion, ReleaseDate
(Get-CimInstance Win32_OperatingSystem) | Select-Object Caption, Version, BuildNumber
wsl --status
```

**Options for people who hit this (a project decision is pending):**
- **Update the BIOS/UEFI** from the computer maker's official support page, make a restore point, and retry once.
- **Skip WSL and Docker on this computer.** Prepare the repository and front-end and back-end code with Git, pnpm and uv only, and run the database and cache somewhere else (another computer that works, or a cloud development environment) until the hardware issue is solved.
- **Turn off hardware virtualization in the BIOS** (reported to let Windows start, but WSL 2 and Docker then cannot run). This is a workaround for starting Windows, not a way to run Docker.

## 5. Cautions

- **Secrets:** never commit real credentials. Local configuration uses a `.env.example` file with variable names and safe placeholder values only. The real `.env` file is never committed.
- **Memory:** Docker, an Android emulator, a browser and an editor together can use a lot of memory. On a computer with about 12 GB, expect to limit Docker's memory.
- **Personal data:** use only synthetic data in development. Never copy real donor or patient information into a local or test environment.

## 6. Setup progress (update as you go)

- [x] Windows 10 Pro 22H2 (build 19045), 64-bit, about 12 GB memory, virtualization enabled in the BIOS (the setup computer is a 2015 dual-core laptop, so expect it to be slow with Docker)
- [x] Node.js installed
- [x] Project drive is NTFS, fixed and healthy, with plenty of free space
- [x] Git installed and verified (2.56.0)
- [x] pnpm installed and verified (11.28.9)
- [x] uv installed and verified (0.13.6)
- [ ] WSL installed (restart done). **BLOCKED on the tested computer, see section 4.1**
- [ ] Docker Desktop installed and verified (licensing terms checked). Depends on WSL, see section 4.1
- [x] Repository initialized on `main` and pushed to GitHub, with no secrets committed (`.env` is not tracked)
- [x] Workspace foundation created and verified (folder tree, pnpm workspace file, `.gitignore`, `.env.example`)
- [ ] Local services (PostgreSQL with PostGIS, Redis) running. **Not possible yet on the setup computer, see section 4.1**
- [ ] Android emulator. Depends on the same virtualization feature, see section 4.1

### Open items

- Local services cannot run on the first setup computer (Windows 10 Pro, Intel Core i3-5015U, BIOS from 2015) because the Virtual Machine Platform feature stops Windows from starting. Options (BIOS update, another way to run the database, or another machine) are undecided.
- Windows 10 no longer receives regular security updates unless enrolled in Microsoft's extended updates. Docker Desktop support for Windows 10 is not yet verified.
- Availability of the Blood Nation domain, app store names and trademark has not been checked.
- Hosting is still undecided.

## 7. Project documents to keep in the `docs` area

Master Specification · Architecture · Database and data model · API contract · Security design · UX and design system reference · Decision register · Open questions.

## 8. Planned improvement (proposed, not yet approved)

A read-only **check script** that reports READY or MISSING for each tool with official links, and a **safe setup script** that installs project-level dependencies, copies `.env.example` to `.env` when missing, and starts the local services. Large system tools (Git, Docker, WSL) would be guided with official links and installed only after confirmation.
