import tkinter as tk
from tkinter import messagebox
import datetime
import os

GOAL_TIME = "08:30"  # 목표 시간을 8:30으로 설정


class PunchBox:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Work Time Checker")
        self.window.geometry("300x200")
        
        # 메인 버튼들
        tk.Button(self.window, text="출근 체크", command=self.check_work_time).pack(pady=20)
        tk.Button(self.window, text="기록 보기", command=self.view_records).pack(pady=20)
        
    def check_work_time(self):
        try:
            now = datetime.datetime.now()
            current_date = now.strftime("%m/%d/%Y")
            current_time = now.strftime("%H:%M")
            
            # WorkTime.txt 파일이 없으면 생성
            if not os.path.exists("WorkTime.txt"):
                with open("WorkTime.txt", "w") as f:
                    pass
                    
            # 오늘 이미 체크인했는지 확인
            with open("WorkTime.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if current_date in line:
                        messagebox.showwarning("경고", "오늘은 이미 체크인하셨습니다!")
                        return

            # 현재 시간이 오전 5시 이전인지 확인
            if now.hour < 5:
                messagebox.showwarning("경고", "오전 5시 이후에만 체크인이 가능합니다!")
                return

            # 성공/실패 여부 확인
            goal_hour, goal_minute = map(int, GOAL_TIME.split(":"))
            goal_time = datetime.time(goal_hour, goal_minute)
            current = datetime.time(now.hour, now.minute)
            status = "Success" if current <= goal_time else "Fail"

            # 결과를 파일에 저장
            with open("WorkTime.txt", "a") as f:
                f.write(f"{current_date} {current_time} {status} {GOAL_TIME}\n")

            # 결과 메시지 표시
            icon = "✓" if status == "Success" else "✗"
            messagebox.showinfo("체크인 결과", f"{icon} {status}!\n출근시간: {current_time}")
            
        except Exception as e:
            messagebox.showerror("오류", f"처리 중 오류가 발생했습니다: {str(e)}")
            
    def view_records(self):
        try:
            if not os.path.exists("WorkTime.txt"):
                messagebox.showinfo("알림", "기록이 없습니다.")
                return
                
            with open("WorkTime.txt", "r") as f:
                records = f.readlines()
            
            record_window = tk.Toplevel(self.window)
            record_window.title("출근 기록")
            
            for record in records[-10:]:  # 최근 10개 기록만 표시
                tk.Label(record_window, text=record.strip()).pack(pady=5)
                
        except Exception as e:
            messagebox.showerror("오류", f"기록 조회 중 오류가 발생했습니다: {str(e)}")
                
    def run(self):
        self.check_work_time()
        self.window.mainloop()

if __name__ == "__main__":
    app = PunchBox()
    app.run()