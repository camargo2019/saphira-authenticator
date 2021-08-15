#!/usr/bin/python3.8
##################################
# Gabriel CMR - Desenvolvimentos #
#      Saphira Authenticator     #
#  Todos os Direitos Reservados! #
##################################
import os
import sys
import json
import time
from tkinter import *
from PIL import ImageTk, Image
from threading import Thread
import psutil
import subprocess
import mysql.connector as mysql
import win32com.shell.shell as shell
import json
import urllib.request
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz

pid = os.getpid()
for proc in psutil.process_iter(['pid', 'name']):
    inf = json.dumps(proc.info)
    inf2 = json.loads(inf)
    if(inf2['name'] == 'SaphiraAuthenticator.exe' and inf2['pid'] != pid):
        subprocess.call(['taskkill /F /PID '+str(inf2['pid'])], shell=False)

class GetIP:
    def __init__(self):
        self.url = 'http://ipinfo.io/json'
        self.response = urllib.request.urlopen(self.url).read()
        self.data = json.loads(self.response.decode('utf-8'))

    def result(self):
        return self.data['ip']


class run_command:
    def __init__(self, Comando, Shell=True):
        self.Comando = Comando.split()
        self.Shell = Shell
        subprocess.Popen(self.Comando, shell=self.Shell)

class Main:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.TokenValida = False
        self.RunningSoftwareFirewalld = False
        self.StopThreadUpdate = False
        self.db = mysql.connect(
                    host="51.222.157.149",
                    port=3306,
                    user="root",
                    database="saphira-authenticator",
                    password="dPE4FtCJ3Npe")
        self.DbOn = self.db.cursor()
        self.StartTk = Tk()
        self.StartTk.title("Saphira Authenticator - LuraHosting")
        self.StartTk.wm_attributes("-topmost", True)
        self.StartTk.resizable(0, 0)
        self.StartTk.iconbitmap(self.dir_path+"\\media\\favicon.ico")
        self.ws2 = self.StartTk.winfo_screenwidth()
        self.hs2 = self.StartTk.winfo_screenheight()
        self.wid2 = 540
        self.hei2 = 142.5
        self.x2 = (self.ws2 / 2) - (self.wid2 / 2)
        self.y2 = (self.hs2 / 2) - (self.hei2 / 2)
        self.StartTk.geometry('%dx%d+%d+%d' % (self.wid2, self.hei2, self.x2, self.y2))
        self.StartTk.overrideredirect(True)

        self.ImagemLogo = ImageTk.PhotoImage(
            Image.open(self.dir_path + "\\media\\logo.png").resize((540, 142), Image.ANTIALIAS))

        self.ImgTemp = Label(self.StartTk, image=self.ImagemLogo)
        self.ImgTemp.config(bg='white')
        self.ImgTemp.pack()

        self.StartTk.after(10000, self.StartTk.destroy)
        self.StartTk.mainloop()

        ASADMIN = 'asadmin'
        """if sys.argv[-1] != ASADMIN:
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
            try:
                shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
            except:
                sys.exit(0)
            sys.exit(0)
        else:"""
        self.pedir_token()

    def pedir_token_check_hand_enter(self):
        self.Canvas.config(cursor="hand2")


    def pedir_token_check_hand_leave(self):
        self.Canvas.config(cursor="")

    def pedir_token(self):
        self.PedirToken = Tk()
        self.PedirToken.title("Saphira Authenticator - LuraHosting")
        self.PedirToken.iconbitmap(self.dir_path + "\\media\\favicon.ico")
        self.PedirToken.resizable(0, 0)
        self.ws2 = self.PedirToken.winfo_screenwidth()
        self.hs2 = self.PedirToken.winfo_screenheight()
        self.wid2 = 350
        self.hei2 = 250
        self.x2 = (self.ws2 / 2) - (self.wid2 / 2)
        self.y2 = (self.hs2 / 2) - (self.hei2 / 2)
        self.PedirToken.geometry('%dx%d+%d+%d' % (self.wid2, self.hei2, self.x2, self.y2))
        self.PedirToken.config(bg='white')

        self.FontTxt = ("Arial", 12)
        self.FontTxt2 = ("Arial", 10)

        self.Frame = Frame(self.PedirToken, width=350, height=40, bg="white")
        self.Frame.pack()

        self.ImagemLogo = ImageTk.PhotoImage(
            Image.open(self.dir_path + "\\media\\logo.png").resize((180, 39), Image.ANTIALIAS))

        self.ImgLogo = Label(self.Frame, image=self.ImagemLogo, bg="white")
        self.ImgLogo.pack(pady=15)

        self.Text = Label(self.Frame, text="Coloque seu Token: ", bg="white")
        self.Text.pack(pady=10)
        self.Text.configure(font=self.FontTxt)

        self.TextToken = Text(self.Frame, width=30, height=2)
        self.TextToken["relief"] = "groove"
        self.TextToken["borderwidth"] = 2
        self.TextToken["highlightcolor"] = "#808080"
        self.TextToken["highlightbackground"] = "#808080"
        self.TextToken.pack()
        self.TextToken.configure(font=self.FontTxt)

        self.Canvas = Canvas(self.PedirToken, width=350, height=150, bg="white", bd=0, highlightthickness=0,
                             relief='ridge')
        self.Canvas.pack()

        self.ImagemButton = ImageTk.PhotoImage(
            Image.open(self.dir_path + "\\media\\validar.png").resize((160, 55), Image.ANTIALIAS))

        self.CanvasImg = self.Canvas.create_image(170, 45, image=self.ImagemButton)

        self.Canvas.tag_bind(self.CanvasImg, "<Enter>", lambda event: self.pedir_token_check_hand_enter())
        self.Canvas.tag_bind(self.CanvasImg, "<Leave>", lambda event: self.pedir_token_check_hand_leave())
        self.Canvas.tag_bind(self.CanvasImg, "<Button-1>", self.ValidarToken)
        self.Canvas.tag_bind(self.CanvasImg, "<Key>", self.ValidarToken)

        self.CanvasTxt = self.Canvas.create_text(175, 10, text="", fill="white", font=self.FontTxt2)

        self.PedirToken.mainloop()

    def ValidarToken(self, event=None):
        self.db.commit()
        self.DbOn = self.db.cursor()
        self.Result = self.TextToken.get(1.0, "end-1c")
        self.TextToken.configure(highlightbackground="#808080", highlightcolor="#808080")
        self.Canvas.itemconfigure(self.CanvasTxt, text="",
                                  fill="white")
        self.Result = self.Result.replace(" ", "")
        self.Result = self.Result.replace("\n", "")
        self.DbOn.execute("SELECT * FROM cmr_servers WHERE token='"+self.Result+"' LIMIT 1")
        self.getIp = GetIP()
        self.resultIP = self.getIp.result()
        self.resultSelectTable = self.DbOn.fetchone()
        if self.resultSelectTable:
            if self.resultSelectTable[1] == self.resultIP:
                self.PedirToken.destroy()
                self.TokenValida = self.resultSelectTable[2]
                self.StartAndStopSystem()
            else:
                self.TextToken.configure(highlightbackground="red", highlightcolor="red")
                self.Canvas.itemconfigure(self.CanvasTxt, text="O Token não foi registrado para esse ip!", fill="red")
        else:
            self.TextToken.configure(highlightbackground="red", highlightcolor="red")
            self.Canvas.itemconfigure(self.CanvasTxt, text="O Token não foi encontrado!",
                                      fill="red")

    def StartAndStopSystem(self):
        self.StartAndStopTk = Tk()
        self.StartAndStopTk.title("Saphira Authenticator - LuraHosting")
        self.StartAndStopTk.iconbitmap(self.dir_path + "\\media\\favicon.ico")
        self.StartAndStopTk.resizable(0, 0)
        self.ws2 = self.StartAndStopTk.winfo_screenwidth()
        self.hs2 = self.StartAndStopTk.winfo_screenheight()
        self.wid2 = 350
        self.hei2 = 250
        self.x2 = (self.ws2 / 2) - (self.wid2 / 2)
        self.y2 = (self.hs2 / 2) - (self.hei2 / 2)
        self.StartAndStopTk.geometry('%dx%d+%d+%d' % (self.wid2, self.hei2, self.x2, self.y2))
        self.StartAndStopTk.config(bg='white')

        self.ImagemLogo = ImageTk.PhotoImage(
            Image.open(self.dir_path + "\\media\\logo.png").resize((180, 39), Image.ANTIALIAS))

        self.ImgLogo = Label(self.StartAndStopTk, image=self.ImagemLogo, bg="white")
        self.ImgLogo.pack(pady=15)

        self.Canvas = Canvas(self.StartAndStopTk, width=350, height=211, bg="white", bd=0, highlightthickness=0,
                             relief='ridge')
        self.Canvas.pack()

        self.ImgStart = ImageTk.PhotoImage(Image.open(self.dir_path+"\\media\\desligado.png").resize((105, 90), Image.ANTIALIAS))
        self.ImgStop = ImageTk.PhotoImage(
            Image.open(self.dir_path + "\\media\\ligado.png").resize((105, 90), Image.ANTIALIAS))

        self.CanvasStartAndStop = self.Canvas.create_image(175, 50, image=self.ImgStart)
        self.Canvas.tag_bind(self.CanvasStartAndStop, "<Enter>", lambda event: self.pedir_token_check_hand_enter())
        self.Canvas.tag_bind(self.CanvasStartAndStop, "<Leave>", lambda event: self.pedir_token_check_hand_leave())
        self.Canvas.tag_bind(self.CanvasStartAndStop, "<Button-1>", self.StartOrStopFirewall)
        self.Canvas.tag_bind(self.CanvasStartAndStop, "<Key>", self.StartOrStopFirewall)


        self.StartAndStopTk.mainloop()

    def StartOrStopFirewall(self, event=None):
        if self.RunningSoftwareFirewalld == False:
            self.Canvas.itemconfigure(self.CanvasStartAndStop, image=self.ImgStop)
            self.RunningSoftwareFirewalld = True
            self.StopThreadUpdate = False
            run_command("netsh firewall reset")
            run_command("netsh firewall set opmode enable")
            #run_command("netsh advfirewall firewall add rule name='NopenPorts' dir=in action=block remoteip=any protocol=TCP localport=0-65535")
            #run_command("netsh advfirewall firewall add rule name='NopenPortsUDP' dir=in action=block remoteip=any protocol=UDP localport=0-65535")
            time.sleep(0.01)
            self.StartFirewallUpdate = Thread(target=self.FirewallUpdate)
            self.StartFirewallUpdate.start()
        else:
            self.Canvas.itemconfigure(self.CanvasStartAndStop, image=self.ImgStart)
            self.RunningSoftwareFirewalld = False
            run_command("netsh firewall set opmode disable")
            #run_command("netsh advfirewall firewall delete rule name=all protocol=TCP localport=0-65535")
            #run_command("netsh advfirewall firewall delete rule name=all protocol=UDP localport=0-65535")
            time.sleep(0.01)
            self.StopThreadUpdate = True

    def FirewallUpdate(self):
        while True:
            self.db.commit()
            self.DbOn.execute("SELECT * FROM cmr_autenticado WHERE id_server='"+str(self.resultSelectTable[0])+"' and inserido='N'")
            all_dados = self.DbOn.fetchall()
            for x in all_dados:
                if x[2] or x[0]:
                    run_command(f'netsh advfirewall firewall add rule name="Open{x[2]}" remoteip={x[2]} protocol=TCP dir=in localport=0-65535 action=allow')
                    run_command(f'netsh advfirewall firewall add rule name="Open{x[2]}UDP" remoteip={x[2]} protocol=UDP dir=in localport=0-65535 action=allow')
                    self.DbOn.execute("UPDATE `cmr_autenticado` SET `inserido`='Y' WHERE id='"+str(x[0])+"'")
            self.db.commit()
            self.DbOn.execute("SELECT * FROM cmr_autenticado WHERE id_server='"+str(self.resultSelectTable[0])+"' and inserido='Y' and permanent='N'")
            dads_info = self.DbOn.fetchall()
            for x in dads_info:
                if x[0]:
                    st_datatimedb = datetime.strptime(str(x[3]), '%Y-%m-%d %H:%M:%S')
                    data_mais6hrs = st_datatimedb + relativedelta(hours=6)
                    data_mais6hrsaa = data_mais6hrs.strftime('%Y%m%d%H%M%S')
                    d = datetime.now()
                    timezone = pytz.timezone("America/Sao_Paulo")
                    d_aware = timezone.localize(d)
                    data_compare = d_aware.strftime('%Y%m%d%H%M%S')
                    if int(data_compare) >= int(data_mais6hrsaa):
                        run_command(f'netsh advfirewall firewall delete rule name=all remoteip={x[2]} protocol=TCP localport=0-65535')
                        run_command(f'netsh advfirewall firewall delete rule name=all remoteip={x[2]} protocol=UDP localport=0-65535')
                        self.DbOn.execute("DELETE FROM `cmr_autenticado` WHERE id='" + str(x[0]) + "'")
            if self.StopThreadUpdate == True:
                break
            time.sleep(0.1)

if __name__ == '__main__':
    Main()