from psychopy import visual, core, gui
from psychopy.hardware import keyboard
import os, csv, random
from datetime import datetime
from psychopy import sound, core, event, hardware

Accumulated_Data = csv.list_dialects()

#dialog
info = {"participant full name" : "",
        "participant ID" : "",
        "participant gender" : ["Male", "Female", "Other"]}
if not gui.DlgFromDict(info, title="Gesture Presence Recognition").OK:
    core.quit()

pid = "P002"
if info["participant ID"]:
    pid = info["participant ID"]

pgender = "P001"
if info["participant gender"]:
    pgender = info["participant gender"]

pname = "P000"
if info["participant full name"]:
    pname = info["participant full name"]

#Window and Textbox
win = visual.Window(size=[1920, 1080], units="pix", color="black", fullscr=True)
txt = visual.TextBox2(win, text="+", font="Arial", letterHeight=34, color="white", size=(1750, 500), alignment="center")
kb = keyboard.Keyboard()


def show(t):
    txt.text = t
    txt.draw()
    win.flip()

def wait_space_rt():
    kb.clearEvents()
    kb.clock.reset()
    while True:
        for k in kb.getKeys(keyList=["space", "escape"], waitRelease=False):
            if k.name == "escape":
                win.close()
                core.quit()
            if k.name == "space":
                return round(k.rt * 1000, 3)
        core.wait(0.001)



#content
Consent_Form = "Recognition of the Presence of Gestures in Telephone comunication \n\n\n" \
"Before you begin the experiment, please read the following information carefully: \n\n" \
"You are hereby invited to participate in a research study revolving the recogntion of the presence og gestures during telephone communication. In this experiment, you will be presented with a number of recorded sentences to which you will need to answer whether or not gesturing was done during recording. prequisites for participation includes being over the age of 18, the cognitive ability to consistently make independent judgements and uncompromised hearing ability (hearing aids compatible with headphones are allowed). \n" \
"The study is conducted by first semester cognitive science student Gabriel Kirkeby, who can be contacted on the following mail adress: au807234@uni.au.dk. \n\n" \
"Upon start of the experiment, you will be presented with an auditory recording. After hearing the entirety of it, you will be asked to guess whether or not you think the speaker gestured during recording. This will repeat 3 times, for a total of 4 recordings. When providing your answer, press M to indicate the presence gestures and Z to indicate the absence of gestures. \n" \
"The experiment is estimated to take no longer than 5 minutes and includes no other risks than those encountered in daily life. No compensation will be provided. \n\n" \
"Participation is voluntary and can be retracted at any time, including any collected data even after anonymization. \n" \
"If you have any more questions regarding the study, please consult the responsible investigator, Gabriel Kirkeby. When you have read and understood this introduction and your involvement as a participant, have no further questions and want to participate, please press [SPACE] to consent and begin the experiment. Would you like to decline, press [ESC] to exit this window."

Answering_Message = "Press Z if you think the speaker did not gesture when recording. \n" \
"Press M if you think the speaker did gesture when recording. "

Waiting_Message = "Get ready for the next recording."
Waiting_Message_First = "Get ready for the first recording."

Playing_Message = "Now Playing..."

One = 0
Two = 1
Three = 2
Four = 3

A=[NG1 := sound.Sound("CogCom_Exam_Project_Sound_Files\Sound_File_1_No_Gestures[1].wav"), NG2 := sound.Sound("CogCom_Exam_Project_Sound_Files\Sound_File_2_No_Gestures[1].wav"), NG3 := sound.Sound("CogCom_Exam_Project_Sound_Files\Sound_File_3_No_Gestures[1].wav"), NG4 := sound.Sound("CogCom_Exam_Project_Sound_Files\Sound_File_4_No_Gestures[1].wav")]
B=[G1 := sound.Sound("CogCom_Exam_Project_Sound_Files\Sound_File_1_Gestures[1].wav"), G2 := sound.Sound("CogCom_Exam_Project_Sound_Files\Sound_File_2_Gestures[1].wav"), G3 := sound.Sound("CogCom_Exam_Project_Sound_Files\Sound_File_3_Gestures[1].wav"), G4 := sound.Sound("CogCom_Exam_Project_Sound_Files\Sound_File_4_Gestures[1].wav")]

Stimulus=[One, Two, Three, Four]
Condition=[A, A, B, B]
f_num = 0

conds = [("Condition", Condition)]
random.shuffle(Stimulus)
random.shuffle(Condition)


#run

rows = []
for cname, tokens in conds:
    show(Consent_Form)
    rt = wait_space_rt()
    while f_num<=3:
        if f_num==0:
            show(Waiting_Message_First)
        else:
            show(Waiting_Message)
        core.wait(1.25)
        if Condition[f_num] == A:
            A[Stimulus[f_num]].play()
            show(Playing_Message)
            core.wait(A[Stimulus[f_num]].duration)
            Condition_Name = "No Gestures"
        elif Condition[f_num] == B:
            B[Stimulus[f_num]].play()
            show(Playing_Message)
            core.wait(B[Stimulus[f_num]].duration)
            Condition_Name = "Gestures"
        show(Answering_Message)
        kb.clearEvents()
        kb.clock.reset()
        ans="NA"
        while ans=="NA":
            for k in kb.getKeys(keyList=["z", "m", "escape"], waitRelease=False):
                if k.name == "z":
                    ans = "No"
                    round(k.rt * 1000, 3)
                if k.name == "m":
                    ans = "Yes"
                    round(k.rt * 1000, 3)
                if k.name == "escape":
                    win.close()
                    core.quit()
            core.wait(0.001)
        rows.append({
            "participant full name": pname,
            "participant ID": pid,
            "participant gender": pgender,
            "condition": Condition_Name,
            "file number": Stimulus[f_num]+1,
            "percieved gestures": ans
        })
        f_num = f_num+1


#save and exit
ts = datetime.now().strftime("%Y%m%d-%H%M%S")
os.makedirs("data_cogcom_exam", exist_ok=True)
out = f"data_cogcom_exam/CogCom_Exam_Data_Participant_{pid}_{ts}.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["participant full name", "participant ID", "participant gender","condition","file number","percieved gestures"])
    w.writeheader(); w.writerows(rows)

show(f"Done.\nSaved: {out}\nPress any key to exit.")
kb.waitKeys()
win.close()
core.quit()