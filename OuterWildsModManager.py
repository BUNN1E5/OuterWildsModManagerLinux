import os
import urllib.request
import progressbar
import tarfile
import time
import tkinter
from tkinter import filedialog

#This is such a terrible script, but all that matters is that it seems to work
#if you want to make it better/ good in any way feel free to make a PR

WINEPREFIX = os.getenv('WINEPREFIX')

#Shamelessly stolen from https:/www.anycodings.com/1questions/53584/how-to-use-progressbar-module-with-urlretrieve
pbar = None
def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

def fake_progress(wait):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=wait)
        pbar.start()
        
    progress = 0
    for i in range(wait):
        pbar.update(progress)
        time.sleep(1)
        progress += 1
    pbar.finish()
    pbar = None
    

def tar_progress(members):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=len(members.getmembers()))
        pbar.start()
                                       
    downloaded = 0
    for member in members:
        pbar.update(downloaded)
        print(member.name)
        yield member
        downloaded+=1
    pbar.finish()
    pbar = None

def run_setup():
    proton_string = 'Proton 5.0'
    compat_mounts = os.getenv('STEAM_COMPAT_MOUNTS')
    return proton_string in compat_mounts

#check for startup file
#if startup file is found, just start the mod manager
#os.system("C:/\"Program Files\"/OuterWildsModManager/OuterWildsModManager.exe")
def setup():
    current_user = os.getenv('USER')
    c_roaming = 'C:/users/steamuser/AppData/Roaming'

    home_path = '/home/' + current_user

    steamapps_path = 'Z:' + home_path + '/.steam/steam/steamapps'

    default_outer_wilds_path = steamapps_path + '/compatdata/753640/pfx/drive_c'

    outer_wilds_compatdata = default_outer_wilds_path

    while not os.path.exists(outer_wilds_compatdata):
        print("Outer Wilds compatdata not found!!\n")
        print("Please locate and input Outer Wilds compatdata folder\n")
        print("usually found under ~/.steam/steam/steamapps/compatdata/753640\n")
        tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
        outer_wilds_compatdata = filedialog.askdirectory()
    
    print('If asked to delete something just type yes\n')
    print('Don\'t worry about any error messages, those are normal\n\n')
    
    os.system("del " + outer_wilds_compatdata + '/users/steamuser/AppData/Roaming')
    os.system("rmdir " + outer_wilds_compatdata + '/users/steamuser/AppData/Roaming')
    
    os.system("del " + outer_wilds_compatdata + '/users/steamuser/ApplicationData')
    os.system("rmdir " + outer_wilds_compatdata + '/users/steamuser/ApplicationData')
    
    
    #if Symbolic link
    os.system('rmdir C:/"Program Files (x86)"/Steam/steamapps')
    
    #if normal folder
    os.system('del C:/"Program Files (x86)"/Steam/steamapps')
    os.system('rmdir C:/"Program Files (x86)"/Steam/steamapps')
    
    os.system('rmdir ' + outer_wilds_compatdata + '/\"Program Files (x86)\"/Steam/steamapps')
    os.system('del ' + outer_wilds_compatdata + '/\"Program Files (x86)\"/Steam/steamapps')
    os.system('rmdir ' + outer_wilds_compatdata + '/\"Program Files (x86)\"/Steam/steamapps')

    print('Downloading Outer Wilds Mod Manager\n')
    urllib.request.urlretrieve('https://github.com/ow-mods/ow-mod-manager/releases/latest/download/OuterWildsModManager-Installer.exe', 'C:/OWMMInstaller.exe', show_progress)
  
#    print('Downloading dotnet47 installer\n')
#    urllib.request.urlretrieve('https://go.microsoft.com/fwlink/?LinkId=863262', 'C:/ndp47-web.exe', show_progress)
  
#    print('Downloading dotnet48 installer\n')
#    urllib.request.urlretrieve('https://download.visualstudio.microsoft.com/download/pr/7afca223-55d2-470a-8edc-6a1739ae3252/abd170b4b0ec15ad0222a809b761a036/ndp48-x86-x64-allos-enu.exe', 'C:/ndp48-web.exe', show_progress)
    
    ln_command = "mklink /D " + c_roaming + ' C:/users/steamuser/\"Application Data\"'
    os.system(ln_command)

    ln_command = "mklink /D " + outer_wilds_compatdata + '/users/steamuser/AppData/Roaming ' + c_roaming
    os.system(ln_command)
    
    ln_command = "mklink /D " + outer_wilds_compatdata + '/\"Program Files (x86)\"/Steam/steamapps ' + steamapps_path
    os.system(ln_command)

    ln_command = "mklink /D " + "C:/\"Program Files (x86)\"/Steam/steamapps " + steamapps_path
    os.system(ln_command)
    
#    os.system('C:/ndp47-web.exe')
#    os.system('C:/ndp48-web.exe')
    os.system('C:/OWMMInstaller.exe')

    cache_var = os.getenv('MESA_SHADER_CACHE_DIR')
    cache_var = cache_var.split('/')
    cache_var = cache_var[len(cache_var)-1]

    print('For the following instructions you need to stop the installer\n')
    print('THIS WILL CLOSE THIS WINDOW SO WRITE THESE COMMANDS DOWN OR SOMETHING!!\n\n\n')

    print('You still need to install .NET 4.8!\n')
    print('You can do that by installing protontricks\n')   
    print('By running the following command\n')   
    print('protontricks ' + cache_var + ' dotnet48\n')
    print('\n')
    print('If you are running a steamdeck run the following commands\n')
    print('flatpak run com.github.Matoking.protontricks ' + cache_var + ' dotnet48\n')
    
    print('Once you have completed the dotnet install\n')
    print('Switch to a proton version of 6.3 or greater\n')
    input("Press Enter to Close Setup...")
    

#os.system("start cmd /k echo Debug")

if run_setup():
    input("Press Enter to Start Setup...")
    setup()
else:
    if not os.path.exists('C:/Program Files/OuterWildsModManager/OuterWildsModManager.exe'):
        if os.path.exists('C:/OWMMInstaller.exe'):
            os.system('C:/OWMMInstaller.exe')
        else:
            print("\n\n")
            print("Outer Wilds Mod Manager not installed, run using Proton 5.0 to run installer")
            input("Press Enter to Close...")
    else:
        os.system('C:/"Program Files"/OuterWildsModManager/OuterWildsModManager.exe')
