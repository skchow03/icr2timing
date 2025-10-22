===========================================================
  ICR2 TIMING OVERLAY – v0.5.1
  Author: SK Chow
===========================================================

Live timing overlays for IndyCar Racing II (ICR2).
Supports DOS (indycar.exe), Rendition (cart.exe), and Windows (WINDY.EXE) builds.

-----------------------------------------------------------
 QUICK START
-----------------------------------------------------------

1. Prerequisites
   - Windows 10/11 PC
   - IndyCar Racing II installed:
       • DOS version (indycar.exe inside DOSBox)
       • Rendition version (cart.exe)
       • Windows version (WINDY.EXE)
   - Place ICR2Timing.exe in its own folder.
   - Keep settings.ini and profiles.ini in the same folder as the exe.

2. First Launch
   - Before using, check settings.ini and that the correct version is set in settings.ini under [memory]:
     Possible values: DOS, REND32A, WINDY
     window_keywords are probably "dosbox, cart" or "dosbox, indycar" for REND32A and "CART Racing" for Windy
   - Start IndyCar Racing II.
   - Run ICR2Timing.exe.
   - On first run, click "Select EXE" in the Control Panel and browse
     to the game executable (indycar.exe, cart.exe, or WINDY.EXE).
   - The path is saved automatically in settings.ini.

3. Connecting
   - The app will auto-attach to the game window.
   - If connection fails, check:
       • That the game is running
       • That the correct version is set in settings.ini under [memory]:
           DOS, REND32A, WINDY

4. Using the Overlays
   - Control Panel buttons:
       • Show Overlay → timing table with positions, laps, gaps
       • Show Radar   → proximity radar around your car
       • Show Track Map → bubble map of circuit with car positions
   - Overlays can be dragged and positioned freely on screen.

5. Saving Your Setup
   - Last session is saved automatically on exit.
   - Profiles can be created, saved, and reloaded for custom layouts.

-----------------------------------------------------------
 VERSION HISTORY
-----------------------------------------------------------
v0.5.1 - fixed issues with error logging

v0.5.0 - Various fixes an added telemetry viewer and logging

v0.4.1 - fixed car numbers/driver names and track names for Windy

v0.4.0  – Initial packaged release (October 2025)
         • Control Panel with overlay management
         • Running order table overlay
         • Proximity radar overlay
         • Track map overlay
         • Profile save/load
         • Configurable via settings.ini