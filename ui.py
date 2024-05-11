from tkinter import *
from tkinter import messagebox,ttk,filedialog
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import requests
from Youtube import *
import threading
from io import BytesIO
import threading


def hook(dic):
    global progress, top1

    if dic['status'] == 'downloading':
        p = dic['_percent_str']
        p = p.replace('%', '')
        progress.set(float(p))
    elif dic['status'] == 'finished':
        confirm = Label(top1, text="Downloaded Successfully", fg="white", font=("Arial", 16), background="#353640")
        confirm.pack()

def top_hook():

    global progress, text, top1
    top1 = Toplevel(root)
    top1.attributes('-topmost', True)
    top1.title("Downloading")
    top1.geometry("300x100")
    top1.configure(background="#353640")
    text = Label(top1, text="Please wait..", fg="white", font=("Arial", 16), background="#353640")
    text.pack()
    progress = DoubleVar()
    progress_bar = ttk.Progressbar(top1, variable=progress, maximum=100, length=200)
    progress_bar.pack()

def start_download():
    global progress, text, top1
    thread = threading.Thread(target=top_hook)
    thread.start()
    decision = selected_option.get()

    if decision == "Select From Here":
        messagebox.showerror(title="Error", message="Please Choose a Format.")
        return
    
    downloadPath = filedialog.askdirectory()

    order = int(decision[:decision.index('-')])

    if "Video" in decision:
        cnt = 1
        for i,j in yt[2].items():
            if cnt == order:
                format_num = i
                break
            cnt += 1
    
    elif "Audio" in decision:
        cnt = len(yt[2])
        for i,j in yt[1].items():
            if cnt == order:
                format_num = i
                break
            cnt += 1

    
    
    try:

        thread2 = threading.Thread(target = lambda: YoutubeDL({'format':format_num,'outtmpl':downloadPath+f"\\{yt[0][0]}{decision[decision.index('.'):]}", 'progress_hooks':[hook],}).download(link))
        thread2.start()
    
    except:
        top1.destroy()
        messagebox.showerror("Error", "Something went wrong, please select another format")



def go_back():

    #going back for choosing another video.
    vid_img_lab.grid_forget()
    vid_title.grid_forget()
    download.grid_forget()
    down_btn.grid(row=2,column=5,pady=20)
    down_other.grid_forget()
    decis_frame.grid_forget()
    choose_frame.grid_forget()
    thumb_frame.grid_forget()
    
def youtube_check(load):
    global yt
    #Searching for the video through a function in main.py that call a class in YouTube_Downloader.py

    global link
    link = video_link.get()
    yt = get_info(link)

    if yt == None:
        #if video not found
        messagebox.showerror(title="Error", message="Invalid Link or Video is not available.")
        load.grid_remove()
        down_btn.grid(row=2,column=5,pady=20)
        return
    
    else:
            #if video is found
            #https://www.youtube.com/watch?v=9phByW13cUE
            try:
                global vid_img_lab
                global vid_title
                global down_other
                global download
                global decis_frame
                global choose_frame
                global thumb_frame
                print(yt)
                #returns the video thumbnail
                thumbnail = Image.open(BytesIO(requests.get(yt[0][1]).content))
                thumbnail = thumbnail.resize((200, 125))
                vid_img = ImageTk.PhotoImage(thumbnail)
                
                #processing video page html to get the title of the video
                video_title = yt[0][0]

                #wraping title text 
                ok = False
                for i in range(1,len(video_title)+1):
                    if i%50==0:
                        ok = True
                    if ok and video_title[i-1]==' ':
                        video_title = video_title[:i-1] + '\n' + video_title[i-1:]
                        ok = False

                #put all above information in the UI
                thumb_frame = ttk.Frame(root)
                thumb_frame.grid(row=2,column=0,rowspan=2,padx=60,pady=20)
                vid_img_lab = Label(thumb_frame, image=vid_img,anchor=W)
                vid_img_lab.image = vid_img
                load.grid_remove()
                vid_title = ttk.Label(thumb_frame, text=video_title,foreground="white",background="#353640",font=("Arial",10,"bold"),anchor=W,padding=(30,0,0,0))
                vid_img_lab.grid(row = 0, column = 0,rowspan=2)
                vid_title.grid(row = 0,column=1)

                #make buttons for go back to choose another video or proceed for downloading
                decis_frame = ttk.Frame(root, padding = (100,20,100,20))
                down_other = Button(decis_frame,text="Go Back",fg="white",background="gray",relief="flat",width=15,height=2,overrelief="ridge", activebackground="grey", activeforeground="white",command=go_back)
                download = Button(decis_frame,text="Download",fg="white",background="red",relief="flat",width=15,height=2,overrelief="ridge", activebackground="#8f0f06", activeforeground="white",command=start_download)
                choose_frame = ttk.Frame(root, padding = (60,20,0,0))
                style.configure('TFrame',bordercolor="#FFFFFF",background="#353640")
                choose_frame.grid(row=4,column=0,sticky=W)
                choose_lb = Label(choose_frame, text="Choose video format: ",foreground="white", background="#353640", font=("Arial",12),anchor=W)
                choose_lb.grid(row=0,column=0)
                
                options = []

                cnt = 1
                for i,j in yt[2].items():
                    options.append(f"{cnt}- Video: {j['Quality']}.{j['Extension']}");cnt+=1
                for i,j in yt[1].items():
                    options.append(f"{cnt}- Audio: {int(float(j['Bitrate']))}kbps .{j['Extension']}");cnt+=1

                # create a variable to store the selected option
                global selected_option
                selected_option = StringVar()

                # set the initial value of the variable to the first option
                selected_option.set("Select From Here")
                
                
                # create the OptionMenu widget
                dropdown = ttk.Combobox(choose_frame, values=options, textvariable=selected_option,width=20,state='readonly')

                dropdown.grid(row=0,column=1)
                decis_frame.grid(row=5,column=0)
                down_other.grid(row=0,column=0,sticky=W,padx=60,pady=20)
                download.grid(row=0,column=1,pady=20)



            except :
                #happens if the internet connection is weak.
                messagebox.showerror(title="Error", message="Connection time out")
                load.grid_remove()
                down_btn.grid(row=2,column=5,pady=20)
                return

def init_down_btn():
    #makeing a waiting gif after pressin on download and start another thread for getting the requested video
    load = Label(root, text="Please wait...", font=("Arial",12,"bold"), background="#353640",pady = 30, fg="white")
    down_btn.grid_remove()
    load.grid(row=2,column=5)

    root.update()
    
    thread = threading.Thread(target=lambda :youtube_check(load))
    thread.start()


root = Tk()
root.title("YouTube Video Downloader")
root.configure(background="#353640")
#root.geometry("800x300")
root.resizable(0,0)

global style
style = ttk.Style()
#main page.
header = Label(root, text="Download Your YouTube Video!", fg="white", font=("Arial", 20), bg="#353640",pady=40,padx=200)
header.grid(row=0,column=0,columnspan=6)

frame_link = LabelFrame(root, text="Enter YouTube Video Link",pady=10,padx=10,background="#353640",fg="white",relief="ridge")
frame_link.grid(row=1, column=0,columnspan=6, padx=20)
video_link = Entry(frame_link, width=90,borderwidth=10,relief="flat",font=("Arial",10,"bold"))
video_link.grid()

down_btn = Button(root, text="Proceed",fg="white",background="red",relief="flat",width=15,height=2,overrelief="ridge", activebackground="#8f0f06", activeforeground="white",command=init_down_btn)
down_btn.grid(row=2,column=5,pady=20)




root.mainloop()