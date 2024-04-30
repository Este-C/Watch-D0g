import subprocess
import os
from colorama import Fore, Style, Back

def clear_screen():
    # Clear the screen
    os.system('clear')

def print_banner():
    clear_screen()
    print(Fore.YELLOW + """

*****************************************************************************
 __          __     _       _           _____   ___        
 \ \        / /___ | |     | |         |  __ \ / _ \       
  \ \  /\  / / __ \| |_ ___| |__ ______| |  | | | | | __ _ 
   \ \/  \/ / / _` | __/ __| '_ \______| |  | | | | |/ _` |
    \  /\  / | (_| | || (__| | | |     | |__| | |_| | (_| |
     \/  \/ \ \__,_|\__\___|_| |_|     |_____/ \___/ \__, |
             \____/                 @@                __/ |                                                    
                             .     :d-h/     -       |___/                      
                      .      `+   +h```yo   /-      .                      
                      -/      h. ss :N/ os `d      ::                      
               .`      o+     oyy+ +MMMo /hys     /s       .               
                /:      ho  ` /N: ..6SCO.`:N+ `  +d`     :/                
                 :y-    .Ns /oh-`hMMy`sMMh`-ho+ oN.    .y/                 
         `:-      -ds` o./My+d..dMMo   +MMm.`hosM/`o``od-      -:.         
           -o+`   ``ym/-m+sMy`-mMN/     /NMN:`sMy+m-/mh.`   `/o-           
             :yy: :o:oNdyMms`/NMN:       -mMN+ omMyhNs:o: :sy:`            
     ---`     `:hdo/ddhMMM+ oNMm-         .dMMo`/NMMhdd/+dh/`      ---     
      `.+o+-` /+/+dNdNMMN:`sMMh.           `hMMy`:NMMMdNdo//. `-+o+-`      
         `-ohho+ydmNMMMm-`hMMy`             `sMMh..dMMMNmy+:+yho:`         
  ..`      .:/sdmmMMMMd..dMMo                 +NMm-`hMMMNdmds/:.       ..` 
  `.:+++/:--:ohdmMMMMy`:mMN/    .-://+//:-.`   /NMN:`sMMMMmdhs/--:/+++:.`  
      `.:+syhddmMMMMs`/NMm:`-+ydmNmmdddmmNmdy+-`-mMN+`oMMMMmdddhs+:.`      
         -:+oydMMMN+`oNMm+sdNMmy+:::----::/sdNNms+mMMo`/NMMMdys+:-         
..--::::::/+shNMMN:`sMMMmNMMmhyhdhhNNNNNdhhhyyhNMMmMMMy`:mMMNhs+/::::::--..
 ``..-:/+oshdmNMm-`hMMMMMMNdhosMo.yMMMMMm./Mh+ydNMMMMMMd..dMNmdyso+/:-..`` 
        `:+sydMh..dMMMMNs:-`  /Mo yMMMMMm :M/  `.:oNMMMMm-`hMdys+:.        
   ``..-:/oyhmy`:mMNsdMMd+.   `hN/./ydho.-mh    .+dMMmsNMN:`smdyo/:-..``   
.-:://+++++omo`/NMm: `/hNMNh/.``+dhs+//ohdo``./ymMNh/` -mMN+`omo+++++//::-.
         -om+`oMMd.     -odNMNds+:+oyyys+/+sdNMNdo-     .dMMs`/do-         
       `./h:`yMMh`         -/ydmNMMNmmmNMMNNdy+-         `yMMy`-h/.`       
  ``-/oohm-.hMMs`              .-:+oosoo+/-.               sMMd..ddoo/-``  
  ..` /y.-dMNo                                                +NMm-`y+ `..`  
      +y`:NMMmsssssssssssssssssssssssssssssssssssssssssssssssmMMN/`so`     
    `so :mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm: +y`    
   `hy--:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::--sh`   
   ./////////omd+/sdohMmyMNMMMMMMMMMMMMMMMMMMMMMNMhmMh+hs/+hmo/::::::::.   
           .+o-   .`oNs-mssMdmMmMMMMMMMMMNMmMNhMssm-oNs`.   -oo.           
         `-:`     `hh. o--Nh.NoyMoNmsMymN+Mh+M-hM:-s .yh.     `::`         
                 -h:    `mh`/o Nm d//M+:m dN`++ ym` `  :h-       `         
                :+`     yy  . -M: o -M: o -M: .  sh      +/                
               ..      /s     oh    `M.    ys     o+      `-               
                      .+      h.     N`    .d      +-                      
                      .      `s      h      o.      .                      
                             -`      +       :     By : 6sco
**************************************************___________****************

""" + Style.RESET_ALL)

def menu():
    print_banner()
    print(Back.YELLOW + "Menu:" + Style.RESET_ALL)
    print(Fore.CYAN + "1"+ Style.RESET_ALL + " - Run Audit")
    print(Fore.CYAN + "2"+ Style.RESET_ALL + " - Create personalized wordlist")
    print(Fore.CYAN + "3"+ Style.RESET_ALL + " - Check password vulnerability")
    print(Fore.RED + "4"+ Style.RESET_ALL + " - Exit")
    while True:
        choice = input(Back.GREEN + "Select your choice: " + Style.RESET_ALL)
        if choice == '1':
                Hostname = input("Enter the hostname of the target: ")
                Ip = input("Enter IP address: ")
                subprocess.call(['python3', 'dns_Recon.py', Hostname, Ip])
                break
        elif choice == '2':
                subprocess.call(['python3', 'tables_perso.py'])
                break
        elif choice == '3':
                subprocess.call(['python3', 'password_Strength.py'])
                break
        elif choice == '4':
                print("Bye !")
                break
        else:
                print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

menu()