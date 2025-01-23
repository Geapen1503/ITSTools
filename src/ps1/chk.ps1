Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name Wallpaper -Value "C:\Users\Theo\PycharmProjects\ITSTools\src\img\wallpaper.jpg"
Start-Process rundll32.exe -ArgumentList "user32.dll, UpdatePerUserSystemParameters"
