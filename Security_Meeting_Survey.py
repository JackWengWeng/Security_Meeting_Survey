from datetime import datetime, timedelta
import streamlit as st
import sqlite3
import requests
import datetime

conn = sqlite3.connect("./Security Meeting Survey.db")

def writetoSQLite(fill_date, department, filler_name, meeting_status, additional_info):
   try:
       cursor = conn.cursor()
       sqlstr = 'INSERT INTO 保安防護聯繫會議辦理情形 (填報日期,填報單位,填報人,會議辦理情形,召開日期或未規劃原因) VALUES (?,?,?,?,?);'
       cursor.execute(sqlstr, (fill_date, department, filler_name, meeting_status, additional_info))
       conn.commit()
   except Exception as e:
      print("Error: %s" % e) 
   cursor.close()
   del cursor 
   return

def send_line_notify(token, message):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': message}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

st.set_page_config(page_title="保安防護聯繫會議辦理情形填報表單")
st.title('保安防護聯繫會議辦理情形填報表單')

fill_date = datetime.date.today()

departments = ["協和發電廠", "龍崎E/S", "通霄發電廠","台中發電廠","林口發電廠","大潭發電廠","頂湖E/S","霧社水庫(萬大發電廠)","明潭發電廠","大觀發電廠","日月潭水庫","中寮開閉所","高雄中央調度中心(高屏供電區處)","大林發電廠","竹園E/S","峨眉E/S","龍潭E/S","南科E/S"]
department = st.selectbox("填表單位", departments)

filler_name = st.text_input("填表人")

meeting_status = st.selectbox("會議辦理情形", ["已召開完畢", "已規劃召開", "尚無規劃召開"])

if meeting_status == "已召開完畢":
    meeting_date = st.date_input("召開日期", datetime.date.today())
elif meeting_status == "已規劃召開":
    planned_meeting_date = st.date_input("規劃召開日期", datetime.date.today())
elif meeting_status == "尚無規劃召開":
    no_plan_reason = st.text_input("尚無規劃原因")

if meeting_status == "已召開完畢":
    additional_info = str(meeting_date)
elif meeting_status == "已規劃召開":
    additional_info = str(planned_meeting_date)
elif meeting_status == "尚無規劃召開":
    additional_info = no_plan_reason

submitted = st.button("提交")

if submitted:
    if not filler_name or not department or (meeting_status == "已召開完畢" and not meeting_date) or (meeting_status == "已規劃召開" and not planned_meeting_date) or (meeting_status == "尚無規劃召開" and not no_plan_reason):
        st.warning("請確保所有欄位都已填寫！")
    else:
        st.write("填表日期:", fill_date)
        st.write("填表單位:", department)    
        st.write("填表人:", filler_name)
        if meeting_status == "已召開完畢":
            st.write("會議辦理情形:", meeting_status, "，召開日期為", meeting_date)
            st.header("資料提交成功，感謝您的協助")
            writetoSQLite(fill_date, department, filler_name, meeting_status, additional_info)
            send_line_notify("dnHh8DVnX0JiLoushbQJ0b5NJXze8Ew95xGztHYjyKN", f"\n填表日期: {fill_date}\n填表單位: {department}\n填表人: {filler_name}\n會議辦理情形: {meeting_status}\n召開日期: {meeting_date}")
        elif meeting_status == "已規劃召開":
            st.write("會議辦理情形:", meeting_status, "，規劃召開日期為", planned_meeting_date)
            st.header("資料提交成功，感謝您的協助")
            writetoSQLite(fill_date, department, filler_name, meeting_status, additional_info)
            send_line_notify("dnHh8DVnX0JiLoushbQJ0b5NJXze8Ew95xGztHYjyKN", f"\n填表日期: {fill_date}\n填表單位: {department}\n填表人: {filler_name}\n會議辦理情形: {meeting_status}\n規劃召開日期: {planned_meeting_date}")
        elif meeting_status == "尚無規劃召開":
            st.write("會議辦理情形:", meeting_status, "，尚無規劃原因:", no_plan_reason)
            st.header("資料提交成功，感謝您的協助")
            writetoSQLite(fill_date, department, filler_name, meeting_status, additional_info)
            send_line_notify("dnHh8DVnX0JiLoushbQJ0b5NJXze8Ew95xGztHYjyKN", f"\n填表日期: {fill_date}\n填表單位: {department}\n填表人: {filler_name}\n會議辦理情形: {meeting_status}\n尚無規劃原因: {no_plan_reason}")
