import os
import subprocess
import sys

class FUNCTIONS:
    """FUNCTIONS is for, well the functions that are needed to run this quick setup."""
    def __init__(self):
        super(FUNCTIONS, self).__init__()
        self.version = "v1.2.2"
        self.NmPr = {}
        self.NMlst = []
        self.DIRs = os.listdir("/home")
        self.COMMANDS = {
            #Make group AMEC for each user created, for easier organization
            "GrpMake":["sudo", "groupadd", "AMEC"],
            #Make users by appending name to end
            "UsrMake":["sudo", "useradd", "-s", "/bin/bash", "-m", "-g", "AMEC", "USER", "-p", "PASS", "-G", "GROUP"],
            #Create directory COMMUNITY_BOWL for each user to access
            "DirMake":["sudo", "mkdir", "/home/COMMUNITY_BOWL"],
            #Set permissions for each user upon user directories
            "UsrPLvl":["sudo", "setfacl", "--recursive", "-m", "NAME", "DIR"],
            #Set up soft-link to COMMUNITY_BOWL
            "SftLink":["sudo", "ln", "-s", "/home/COMMUNITY_BOWL", "DIR"],
            #Set permissions for each user to be able to access COMMUNITY_BOWL
            "ComBowl":["sudo", "chgrp", "-R", "-H", "AMEC", "/home/COMMUNITY_BOWL"]
        }
        self.PERM = [0, 1, 2]
        self.NameLen = 0
        self.HELP = '\n\nEnter NAME or \"?\" for list of commands\n\n'
        self.LOG = open('AMEC.log', 'a')
        self.GROUPS = ['AMEC-Administrator', 'AMEC-Supervisor', 'AMEC-Employee']

    def start(self):
        print("._        ._    ._   ._______  ._______")
        print("| \\       | \\   | \\   \\ _____\\ \\  _____\\")
        print("||\\\\      ||\\\\  ||\\\\   \\\\____   \\ \\")
        print("|| \\\\     || \\\\ || \\\\   \\ ___\\   \\ \\")
        print("||__\\\\    ||  \\\\||  \\\\   \\\\_____  \\ \\_____")
        print("||   \\\\   ||   \\`|   \\\\   \\     \\  \\      \\")
        print("|/    \\|  |/    \\/    \\|   \\_____\\  \______\\ \n")
        print(self.version)
        print("FlakeyKarma\n\n")

    def menu(self):
        chc = ['0', 'e']
        while(True):
            #Start
            self.start()
            print("[0] Add user")
            print("[E] Exit")
            inpt = input("FK> ").lower()
            if inpt in chc:
                if inpt == '0':
                    #Make the names for the object
                    self.NameMake()
                if inpt == 'e':
                    break
            else:
                print("Please enter a choice presented")

    def finish(self):
        print("Done.\n\n")
        print("AMEC " + self.version)
        print("By FlakeyKarma")

    def setPerms(self):
        print("Setting permissions...")
        for usr in self.NmPr:
            print("Setting permissions for %s..." % (usr))
            #For Administrator
            if self.NmPr[usr] == 0:
                #Allow Administrator to have RWX permissions to all home dir's
                for j in self.NmPr:
                    CMD = self.COMMANDS['UsrPLvl']
                    CMD[len(CMD)-2] = str('u:%s:rwx' % (usr))
                    CMD[len(CMD)-1] = str("/home/%s" % (j))
                    self.LOG.write(" ".join(CMD) + '\n')
                    subprocess.run(CMD)

            #For Supervisor
            if self.NmPr[usr] == 1:
                for i in self.NmPr:
                    #If current user is Employee
                    if self.NmPr[i] <= 1:
                        CMD = self.COMMANDS['UsrPLvl']
                        CMD[len(CMD)-2] = str('u:%s:0' % (usr))
                    #If current user is Supervisor or Admin
                    else:
                        CMD = self.COMMANDS['UsrPLvl']
                        CMD[len(CMD)-2] = str('u:%s:rwx' % (usr))
                    CMD[len(CMD)-1] = str("/home/%s" % (i))
                    self.LOG.write(" ".join(CMD) + '\n')
                    #print("\n\nB" + str(CMD) + "\n" + j + "\n" + usr + "\n\n")

                    subprocess.run(CMD)

            #For Employee
            if self.NmPr[usr] == 2:
                for i in self.NmPr:
                    CMD = self.COMMANDS['UsrPLvl']
                    CMD[len(CMD)-2] = str('u:%s:0'% (usr))
                    CMD[len(CMD)-1] = str("/home/%s" % (i))
                    self.LOG.write(" ".join(CMD) + '\n')

                    subprocess.run(CMD)
            #Give each user RWX to own directory
            CMD = self.COMMANDS['UsrPLvl']
            CMD[len(CMD)-2] = str('u:%s:rwx' % (usr))
            CMD[len(CMD)-1] = str("/home/%s" % (usr))
            self.LOG.write(" ".join(CMD) + '\n')
            subprocess.run(CMD)
            #Give each user access to COMMUNITY_BOWL
            CMD[len(CMD)-1] = str("/home/COMMUNITY_BOWL")
            self.LOG.write(" ".join(CMD) + '\n')
            subprocess.run(CMD)
            #Set up soft-link to COMMUNITY_BOWL
            CMD = self.COMMANDS['SftLink']
            CMD[len(CMD)-1] = str('/home/%s/Desktop/COMMUNITY_BOWL' % (usr))
            self.LOG.write(" ".join(CMD) + '\n')
            subprocess.run(CMD)
            print("Done setting for %s..." % (usr))
        print("Done setting permissions.")

    def userPrint(self):
        HEAD = "USER"
        for i in range(self.NameLen):
            HEAD += " "
        print("%s%s" % (HEAD, "PERM"))
        if len(self.NmPr) > 0:
            for user in self.NmPr:
                USR = user
                for i in range((self.NameLen + 4) - len(user)):
                    USR += " "

                print("%s%d" % (USR, self.NmPr[user]))
        else:
            print("None entered.")

    def listCommands(self):
        CMDchr = {'E':'Indicate being finished with entering names.',
                  'B':'Remove last entry.',
                  'L':'List current entries.'}

        for c in CMDchr:
            print("%s %s" % (c, CMDchr[c]))

    #Create users
    def NameMake(self):
        try:
            print(self.HELP)
            while(True):
                while(True):
                    while(True):
                        NAME = input("FK:user> ").split(" ")[0].lower()
                        if NAME != None and NAME != " " or NAME == 'e' or NAME == 'help':
                            break

                    if NAME == "e" or NAME == 'b' or NAME == 'l' or NAME == '?' or NAME == 'help':
                        if NAME == 'b' and len(self.NmPr) > 0:
                            del self.NmPr[list(self.NmPr)[len(self.NmPr)-1]]
                        if NAME == 'l':
                            self.userPrint()
                        if NAME == '?':
                            self.listCommands()
                        if NAME == 'help':
                            print(self.HELP)
                        break

                    while(True):
                        print("PERMISSIONS\n-----------\n\n[0] Administrator\n[1] Supervisor - Parent\n[2] Employee - Child\n")
                        while(True):
                            try:
                                PERM = int(input("FK:perm> ").split(" ")[0])
                            except Exception as e:
                                print("Please enter 0, 1, or 2\n")
                                continue
                            break
                        if PERM != None and PERM in self.PERM:
                            break
                        else:
                            print("Please enter 0, 1, or 2\n")


                    self.NMlst = [i for i in self.NmPr]

                    if NAME in self.NMlst:
                        print("\n\nPlease reassign Name and permission:\n-->%s is currently being added or already exists.\n\n" % NAME)
                    else:
                        break

                if NAME == "e":
                    self.CMD()
                    self.finish()
                    break

                if NAME != 'b' and NAME != 'l' and NAME != '?' and NAME != 'help':
                    if self.NameLen < len(NAME):
                        self.NameLen = len(NAME)
                    self.NmPr[NAME] = PERM

        except (ValueError, KeyboardInterrupt):
            print("\nLog Saved.\n")
            self.LOG.close()
            sys.exit()

    #Run commands with users created
    def CMD(self):
        print("Running constructed commands...")
        #Create group AMEC
        print("Creating group AMEC...")
        CMD = self.COMMANDS['GrpMake']
        subprocess.run(CMD)
        self.LOG.write(" ".join(CMD) + '\n')

        #Create supplimentary groups
        for group in self.GROUPS:
            print("Creating group %s..." % (group))
            CMD[len(CMD)-1] = group
            subprocess.run(CMD)
            self.LOG.write(" ".join(CMD) + '\n')

        #Create users
        for user in self.NmPr:
            print("Creating user %s..." % (user))
            CMD = self.COMMANDS['UsrMake']
            CMD[len(CMD)-5] = user
            CMD[len(CMD)-3] = user + "123"
            CMD[len(CMD)-1] = self.GROUPS[self.NmPr[user]]
            subprocess.run(CMD)
            self.LOG.write(" ".join(CMD) + '\n')

        #Make directory COMMUNITY_BOWL for everyone to access
        print("Making COMMUNITY_BOWL...")
        CMD = self.COMMANDS['DirMake']
        subprocess.run(CMD)
        self.LOG.write(" ".join(CMD) + '\n')

        #Allow COMMUNITY_BOWL to be accessed by all in AMEC group
        print("Adjusting permissions to COMMUNITY_BOWL...")
        CMD = self.COMMANDS['ComBowl']
        subprocess.run(CMD)
        self.LOG.write(" ".join(CMD) + '\n')

        #Set up permissions
        print("Setting permissions for each user...")
        self.setPerms()
        self.LOG.close()
