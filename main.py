# -*- coding: utf-8 -*-
"""
Created on Wed May 20 12:39:45 2020

@author: Shanding Gershinen
"""

import os
import sys
import sqlite3 as sql


import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox as messagebox

LARGE_FONT = ("Matura MT Script Capitals", 18, 'bold')
small_font = ("Lucida Calligraphy", 14)

os.makedirs('./data', exist_ok=True)

def Quit():
    # print ('Hello, getting out of here')
    option = messagebox.askyesno('Quit', 'Are you sure you want to exit?')
    if option:
        sys.exit()


class Database:

    def __init__(self):
        self.connection = sql.connect('./data/records.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Records (firstName TEXT, lastName TEXT, age TEXT, gender TEXT, date TEXT, hospitalID TEXT, scanID TEXT, scanType TEXT, indication TEXT, findings TEXT, conclusion TEXT, doctors TEXT)")

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def insert(self, firstName, lastName, age, gender, date, hospitalID, scanID, scanType, indication, findings,
               conclusion, doctors):
        self.cursor.execute("INSERT INTO Records VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            firstName, lastName, age, gender, date, hospitalID, scanID, scanType, indication, findings, conclusion,
            doctors))
        self.connection.commit()

    def update(self, firstName, lastName, age, gender, date, hospitalID, scanID, scanType, indication, findings,
               conclusion, doctors):
        self.cursor.execute(
            "UPDATE Records SET firstName = ?, lastName = ?, age = ?, gender = ?, date = ?, scanID = ?, scanType = ?, "
            "indication = ?, findings = ?, conclusion = ?, doctors = ? WHERE hospitalID = ?",
            (firstName, lastName, age, gender, date, scanID, scanType, indication, findings, conclusion, doctors,
             hospitalID))
        self.connection.commit()

    def search(self, filter):
        self.cursor.execute("SELECT * FROM Records WHERE hospitalID = ?", (filter,))
        search_results = self.cursor.fetchall()
        return search_results
        # self.connection.commit()

    def delete(self, id):
        self.cursor.execute("DELETE FROM Records WHERE hospitalID = ?", (id,))
        self.connection.commit()

    def display(self):
        self.cursor.execute("SELECT * FROM Records")
        records = self.cursor.fetchall()
        return records


class Values:
    def validate(self, first_name_entry, last_name_entry, age_entry, gender_entry, date_entry, hospital_id_entry,
                 scan_id_entry, scan_type_entry, conclusion_entry, doctors_entry):

        if not (isinstance(first_name_entry, str) and first_name_entry != ''):
            return 'first name'
        elif not (isinstance(last_name_entry, str) and last_name_entry != ''):
            return 'last name'
        elif not (age_entry.isdigit() and age_entry != ''):
            return 'age'
        elif not (isinstance(gender_entry, str) and gender_entry != ''):
            return 'gender'
        elif not (isinstance(date_entry, str) and date_entry != ''):
            return 'date'
        elif not (hospital_id_entry.isdigit() and len(hospital_id_entry) == 6):
            return 'hospital id'
        elif not (scan_id_entry.isdigit() and len(scan_id_entry) == 4):
            return 'scan id'
        elif not (isinstance(scan_type_entry, str) and scan_type_entry != ''):
            return 'scan type'
        elif not (isinstance(conclusion_entry, str) and conclusion_entry != ''):
            return 'conclusion'
        elif not (isinstance(doctors_entry, str) and doctors_entry != ''):
            return 'doctors'
        else:
            return 'OK'


class HospitalRecordManagement(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Hospital Record Management")
        # self.w = tk.Tk.winfo_screenwidth(self)
        # self.h = tk.Tk.winfo_screenheight(self)
        # tk.Tk.geometry(self, "{}x{}".format(self.w, self.h))

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Main, Add, Delete, Search, Display):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Main)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Main(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.header = tk.Frame(self, bd=4)
        # self.header.pack(side='top', fill='x', expand=True, anchor='n')
        self.header.pack(side='top', expand=True, anchor='n')
        # footer = tk.Frame(self).pack(side='bottom')

        self.add_button = tk.Button(self.header, text='New Record', cursor='hand2',
                                    command=lambda: controller.show_frame(Add))
        self.add_button.pack(side='left', padx=10, pady=5)

        self.delete_button = tk.Button(self.header, text='Delete Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Delete))
        self.delete_button.pack(side='left', padx=10, pady=5)
        self.search_button = tk.Button(self.header, text='Search', cursor='hand2',
                                       command=lambda: controller.show_frame(Search))
        self.search_button.pack(side='left', padx=10, pady=5)
        self.display_button = tk.Button(self.header, text='Display Record', cursor='hand2',
                                        command=lambda: controller.show_frame(Display))
        self.display_button.pack(side='left', padx=10, pady=5)
        self.exit_button = tk.Button(self.header, text='Exit', cursor='hand2',
                                     command=Quit)
        self.exit_button.pack(side='left', padx=10, pady=5)

        self.body = tk.Frame(self)
        self.body.pack(fill='both', expand=True, anchor='n')
        self.label = tk.Label(self.body, text='Home')
        self.label.pack()


class Add(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.database = Database()
        self.scan_list = ['Abdominal', 'Abdomino-pelvic', 'Doppler', 'Occular', 'Obstretrics', 'Thyroid', 'TVS']
        self.doctorsList = ['Alabi', 'Atim', 'Anako', 'Momodu', 'Simon', 'Shalangwa']
        self.genderList = ['Male', 'Female']

        self.first = tk.StringVar()
        self.last = tk.StringVar()
        self.v_age = tk.StringVar()
        self.v_gender = tk.StringVar()
        self.v_date = tk.StringVar()
        self.v_hos_id = tk.StringVar()
        self.v_scan_id = tk.StringVar()
        self.v_scan_type = tk.StringVar()
        self.v_indication = tk.StringVar()
        self.v_findings = tk.StringVar()
        self.v_conclusion = tk.StringVar()
        self.v_docs = tk.StringVar()

        self.header = tk.Frame(self, bd=5)
        self.header.pack(side='top', expand=True, anchor='n')
        # footer = tk.Frame(self).pack(side='bottom')

        self.add_button = tk.Button(self.header, text='New Record', cursor='hand2',
                                    command=lambda: controller.show_frame(Add))
        self.add_button.pack(side='left', padx=10, pady=5)

        self.delete_button = tk.Button(self.header, text='Delete Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Delete))
        self.delete_button.pack(side='left', padx=10, pady=5)
        self.search_button = tk.Button(self.header, text='Search', cursor='hand2',
                                       command=lambda: controller.show_frame(Search))
        self.search_button.pack(side='left', padx=10, pady=5)
        self.display_button = tk.Button(self.header, text='Display Record', cursor='hand2',
                                        command=lambda: controller.show_frame(Display))
        self.display_button.pack(side='left', padx=10, pady=5)
        self.exit_button = tk.Button(self.header, text='Exit', cursor='hand2',
                                     command=Quit)
        self.exit_button.pack(side='left', padx=10, pady=5)

        self.body = tk.Frame(self)
        self.body.pack(fill='both', expand=True, anchor='n')

        self.name_frame = tk.Frame(self.body)
        self.name_frame.pack(side='top', fill='x')
        self.indication_frame = tk.Frame(self.body)
        self.indication_frame.pack(side='top', fill='x')
        self.findings_frame = tk.Frame(self.body)
        self.findings_frame.pack(side='top', fill='both')
        self.conclusion_frame = tk.Frame(self.body)
        self.conclusion_frame.pack(side='top', fill='x')
        self.doctors_frame = tk.Frame(self.body)
        self.doctors_frame.pack(side='top', fill='x')
        self.submit_frame = tk.Frame(self.body)
        self.submit_frame.pack(side='top')

        self.first_name = tk.Label(self.name_frame, text='First Name')
        self.first_name.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.first_name_entry = tk.Entry(self.name_frame, textvariable=self.first)
        self.first_name_entry.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.last_name = tk.Label(self.name_frame, text='Last Name')
        self.last_name.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.last_name_entry = tk.Entry(self.name_frame, textvariable=self.last)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        self.age = tk.Label(self.name_frame, text='Age')
        self.age.grid(row=0, column=2, padx=10, pady=5, sticky='w')

        self.age_entry = tk.Entry(self.name_frame, textvariable=self.v_age)
        self.age_entry.grid(row=1, column=2, padx=10, pady=5, sticky='w')

        self.gender = ttk.Label(self.name_frame, text='Gender')
        self.gender.grid(row=0, column=3, padx=10, pady=5, sticky='w')

        self.gender_entry = ttk.Combobox(self.name_frame, values=self.genderList, textvariable=self.v_gender)
        self.gender_entry.grid(row=1, column=3, padx=10, pady=5, sticky='w')

        self.date = tk.Label(self.name_frame, text='Date')
        self.date.grid(row=0, column=4, padx=10, pady=5, sticky='w')

        self.date_entry = tk.Entry(self.name_frame, textvariable=self.v_date)
        self.date_entry.grid(row=1, column=4, padx=10, pady=5, sticky='w')

        self.hospital_id = tk.Label(self.name_frame, text='Hospital ID')
        self.hospital_id.grid(row=0, column=5, padx=10, pady=5, sticky='w')

        self.hospital_id_entry = tk.Entry(self.name_frame, textvariable=self.v_hos_id)
        self.hospital_id_entry.grid(row=1, column=5, padx=10, pady=5, sticky='w')

        self.scan_id = tk.Label(self.name_frame, text='Scan ID')
        self.scan_id.grid(row=0, column=6, padx=10, pady=5, sticky='w')

        self.scan_id_entry = tk.Entry(self.name_frame, textvariable=self.v_scan_id)
        self.scan_id_entry.grid(row=1, column=6, padx=10, pady=5, sticky='w')

        self.scan_type = tk.Label(self.indication_frame, text='Scan Type')
        self.scan_type.grid(row=0, column=0, padx=10, pady=5, sticky='e')

        self.scan_type_entry = ttk.Combobox(self.indication_frame, values=self.scan_list, textvariable=self.v_scan_type)
        self.scan_type_entry.grid(row=0, column=1, padx=10, pady=5, sticky='e')

        self.indication = tk.Label(self.indication_frame, text='Indication')
        self.indication.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.indication_entry = tk.Entry(self.indication_frame, textvariable=self.v_indication)
        self.indication_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        self.findings = tk.Label(self.findings_frame, text='Findings')
        self.findings.pack(anchor='w', padx=10)
        self.findings_entry = ScrolledText(self.findings_frame, wrap='word')
        self.findings_entry.pack(fill='x', padx=10, pady=5)

        self.conclusion = tk.Label(self.conclusion_frame, text='Conclusion')
        self.conclusion.grid(row=9, column=0, padx=10, pady=5, sticky='w')

        self.conclusion_entry = tk.Entry(self.conclusion_frame, textvariable=self.v_conclusion)
        self.conclusion_entry.grid(row=9, column=1, padx=10, pady=5, sticky='w')

        self.doctors = tk.Label(self.doctors_frame, text='Doctors')
        self.doctors.grid(row=10, column=0, padx=10, pady=5, sticky='w')

        self.doctors_entry = ttk.Combobox(self.doctors_frame, values=self.doctorsList, textvariable=self.v_docs)
        self.doctors_entry.grid(row=10, column=1, padx=10, pady=5, sticky='e')

        self.submit = tk.Button(self.submit_frame, text='Submit', font=small_font, command=self.Submit)
        self.submit.pack(side='bottom', fill='x')

    def Submit(self):

        self.values = Values()
        self.test = self.values.validate(self.first_name_entry.get(), self.last_name_entry.get(), self.age_entry.get(),
                                         self.gender_entry.get(), self.date_entry.get(), self.hospital_id_entry.get(),
                                         self.scan_id_entry.get(), self.scan_type_entry.get(),
                                         self.conclusion_entry.get(), self.doctors_entry.get())

        if self.test == 'OK':

            try:
                self.database.insert(self.first_name_entry.get(), self.last_name_entry.get(), self.age_entry.get(),
                                     self.gender_entry.get(), self.date_entry.get(), self.hospital_id_entry.get(),
                                     self.scan_id_entry.get(), self.scan_type_entry.get(), self.indication_entry.get(),
                                     self.findings_entry.get("1.0", tk.END), self.conclusion_entry.get(),
                                     self.doctors_entry.get())




            except Exception as err:
                messagebox.showerror("Error", "Record not successfully entered. \n" + str(err))


            else:
                messagebox.showinfo('Success', 'Records successfully entered.')
                self.clear()

        else:
            self.message = 'Invalid input in field {}'.format(self.test)
            messagebox.showerror("Error", self.message)

    def clear(self):
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_entry.set('')
        self.date_entry.delete(0, tk.END)
        self.hospital_id_entry.delete(0, tk.END)
        self.scan_id_entry.delete(0, tk.END)
        self.scan_type_entry.set('')
        self.indication_entry.delete(0, tk.END)
        self.findings_entry.delete('1.0', tk.END)
        self.conclusion_entry.delete(0, tk.END)
        self.doctors_entry.set('')


class Delete(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.elements = ['First Name', 'Last Name', 'Hospital ID', 'Scan ID']
        self.v = tk.StringVar()
        self.name = tk.StringVar()
        self.vv = 'hospital id'

        self.header = tk.Frame(self, bd=4)
        self.header.pack(side='top', expand=True, anchor='n')
        # footer = tk.Frame(self).pack(side='bottom')

        self.add_button = tk.Button(self.header, text='New Record', cursor='hand2',
                                    command=lambda: controller.show_frame(Add))
        self.add_button.pack(side='left', padx=10, pady=5)

        self.delete_button = tk.Button(self.header, text='Delete Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Delete))
        self.delete_button.pack(side='left', padx=10, pady=5)
        self.search_button = tk.Button(self.header, text='Search', cursor='hand2',
                                       command=lambda: controller.show_frame(Search))
        self.search_button.pack(side='left', padx=10, pady=5)
        self.display_button = tk.Button(self.header, text='Display Record', cursor='hand2',
                                        command=lambda: controller.show_frame(Display))
        self.display_button.pack(side='left', padx=10, pady=5)
        self.exit_button = tk.Button(self.header, text='Exit', cursor='hand2',
                                     command=Quit)
        self.exit_button.pack(side='left', padx=10, pady=5)

        self.body = tk.Frame(self)
        self.body.pack(fill='both', expand=True, anchor='n')

        self.label = tk.Label(self.body, text='Delete Record', font=small_font)
        self.label.grid(row=0, columnspan=4)

        self.search_text = tk.Label(self.body, text='Enter hospital ID to delete', font=small_font)
        self.search_text.grid(row=1, column=0, padx=100, pady=100, ipady=10)

        self.search_entry = tk.Entry(self.body, textvariable=self.name)
        self.search_entry.grid(row=1, column=1, padx=100, pady=100, sticky='w', ipady=10)

        self.search = tk.Button(self.body, text='Delete', font=small_font, command=self.delete_file)
        self.search.grid(row=2, columnspan=4, ipady=10)

        self.database = Database()

    def delete_file(self):
        self.val = self.search_entry.get()
        option = messagebox.askyesno('Delete', 'Are you sure you want to delete thus record?')
        if option:
            try:
                self.database.delete(self.val)
                messagebox.showinfo('Success', 'Record deleted')
                self.search_entry.delete(0, tk.END)
            except Exception as err:
                messagebox.showerror('Error', err)
        else:
            pass

    def Search(self):
        self.database = Database()
        self.data = self.database.search(self.search_entry.get())


class Search(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.database = Database()
        self.elements = ['First Name', 'Last Name', 'Hospital ID', 'Scan ID']
        self.v = tk.StringVar()
        self.vv = 'First Name'

        self.header = tk.Frame(self, bd=4)
        self.header.pack(side='top', expand=True, anchor='n')
        # footer = tk.Frame(self).pack(side='bottom')

        self.add_button = tk.Button(self.header, text='New Record', cursor='hand2',
                                    command=lambda: controller.show_frame(Add))
        self.add_button.pack(side='left', padx=10, pady=5)

        self.delete_button = tk.Button(self.header, text='Delete Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Delete))
        self.delete_button.pack(side='left', padx=10, pady=5)
        self.search_button = tk.Button(self.header, text='Search', cursor='hand2',
                                       command=lambda: controller.show_frame(Search))
        self.search_button.pack(side='left', padx=10, pady=5)
        self.display_button = tk.Button(self.header, text='Display Record', cursor='hand2',
                                        command=lambda: controller.show_frame(Display))
        self.display_button.pack(side='left', padx=10, pady=5)
        self.exit_button = tk.Button(self.header, text='Exit', cursor='hand2',
                                     command=Quit)
        self.exit_button.pack(side='left', padx=10, pady=5)

        self.body = tk.Frame(self)
        self.body.pack(fill='both', expand=True, anchor='n')

        self.label = tk.Label(self.body, text='Search Record', font=small_font)
        self.label.grid(row=0, columnspan=4)

        self.search_text = tk.Label(self.body, text='Enter hospital ID to search', font=small_font)
        self.search_text.grid(row=1, column=0, padx=100, pady=100, ipady=10)

        self.search_entry = tk.Entry(self.body)
        self.search_entry.grid(row=1, column=1, padx=100, pady=100, sticky='w', ipady=10)

        # self.or_search_by = tk.Label(self.body, text=' or search by', font=small_font)
        # self.or_search_by.grid(row=1, column=2, padx=10, pady=100, ipady=10)
        #
        #
        # self.search_filter = ttk.Combobox(self.body, values=self.elements, textvariable=self.v, font=small_font)
        # self.search_filter.current(0)
        # self.vv = self.search_filter.current(0)
        # self.search_filter.grid(row=1, column=3, padx=10, pady=100, ipady=10)

        self.search = tk.Button(self.body, text='Search', font=small_font, command=self.Search)
        self.search.grid(row=2, columnspan=4, ipady=10)

    def Search(self):

        self.data = self.database.search(self.search_entry.get())
        if not self.data:
            messagebox.showerror('Not Found', 'This record is not found!')
        else:
            ask = messagebox.askokcancel(self.data[0][:2], 'View record')
            if ask:
                self.popup(self.data)
            else:
                pass

    def popup(self, vals):
        win = tk.Toplevel()
        win.wm_title('Search Result')

        scan_list = ['Abdominal', 'Abdomino-pelvic', 'Doppler', 'Ocular', 'Obstretrics', 'Thyroid', 'TVS']
        doctorsList = ['one', 'two']
        genderList = ['Male', 'Female']

        self.first = tk.StringVar()
        self.last = tk.StringVar()
        self.v_age = tk.StringVar()
        self.v_gender = tk.StringVar()
        self.v_date = tk.StringVar()
        self.v_hos_id = tk.StringVar()
        self.v_scan_id = tk.StringVar()
        self.v_scan_type = tk.StringVar()
        self.v_indication = tk.StringVar()
        self.v_findings = tk.StringVar()
        self.v_conclusion = tk.StringVar()
        self.v_docs = tk.StringVar()

        body = tk.Frame(win)
        body.pack(fill='both', expand=True, anchor='n')

        name_frame = tk.Frame(body)
        name_frame.pack(side='top', fill='x')
        indication_frame = tk.Frame(body)
        indication_frame.pack(side='top', fill='x')
        findings_frame = tk.Frame(body)
        findings_frame.pack(side='top', fill='both')
        conclusion_frame = tk.Frame(body)
        conclusion_frame.pack(side='top', fill='x')
        doctors_frame = tk.Frame(body)
        doctors_frame.pack(side='top', fill='x')
        submit_frame = tk.Frame(body)
        submit_frame.pack(side='top')

        first_name = tk.Label(name_frame, text='First Name')
        first_name.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        first_name_entry = tk.Entry(name_frame, textvariable=self.first)
        first_name_entry.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        last_name = tk.Label(name_frame, text='Last Name')
        last_name.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        last_name_entry = tk.Entry(name_frame, textvariable=self.last)
        last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        age = tk.Label(name_frame, text='Age')
        age.grid(row=0, column=2, padx=10, pady=5, sticky='w')

        age_entry = tk.Entry(name_frame, textvariable=self.v_age)
        age_entry.grid(row=1, column=2, padx=10, pady=5, sticky='w')

        gender = ttk.Label(name_frame, text='Gender')
        gender.grid(row=0, column=3, padx=10, pady=5, sticky='w')

        gender_entry = ttk.Combobox(name_frame, values=genderList, textvariable=self.v_gender)
        gender_entry.grid(row=1, column=3, padx=10, pady=5, sticky='w')

        date = tk.Label(name_frame, text='Date')
        date.grid(row=0, column=4, padx=10, pady=5, sticky='w')

        date_entry = tk.Entry(name_frame, textvariable=self.v_date)
        date_entry.grid(row=1, column=4, padx=10, pady=5, sticky='w')

        hospital_id = tk.Label(name_frame, text='Hospital ID')
        hospital_id.grid(row=0, column=5, padx=10, pady=5, sticky='w')

        hospital_id_entry = tk.Entry(name_frame, textvariable=self.v_hos_id)
        hospital_id_entry.grid(row=1, column=5, padx=10, pady=5, sticky='w')

        scan_id = tk.Label(name_frame, text='Scan ID')
        scan_id.grid(row=0, column=6, padx=10, pady=5, sticky='w')

        scan_id_entry = tk.Entry(name_frame, textvariable=self.v_scan_id)
        scan_id_entry.grid(row=1, column=6, padx=10, pady=5, sticky='w')

        scan_type = tk.Label(indication_frame, text='Scan Type')
        scan_type.grid(row=0, column=0, padx=10, pady=5, sticky='e')

        scan_type_entry = ttk.Combobox(indication_frame, values=scan_list, textvariable=self.v_scan_type)
        scan_type_entry.grid(row=0, column=1, padx=10, pady=5, sticky='e')

        indication = tk.Label(indication_frame, text='Indication')
        indication.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        indication_entry = tk.Entry(indication_frame, textvariable=self.v_indication)
        indication_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        findings = tk.Label(findings_frame, text='Findings')
        findings.pack(anchor='w', padx=10)
        self.findings_entry = ScrolledText(findings_frame, wrap='word')
        self.findings_entry.pack(fill='x', padx=10, pady=5)

        conclusion = tk.Label(conclusion_frame, text='Conclusion')
        conclusion.grid(row=9, column=0, padx=10, pady=5, sticky='w')

        conclusion_entry = tk.Entry(conclusion_frame, textvariable=self.v_conclusion)
        conclusion_entry.grid(row=9, column=1, padx=10, pady=5, sticky='w')

        doctors = tk.Label(doctors_frame, text='Doctors')
        doctors.grid(row=10, column=0, padx=10, pady=5, sticky='w')

        doctors_entry = ttk.Combobox(doctors_frame, values=doctorsList, textvariable=self.v_docs)
        doctors_entry.grid(row=10, column=1, padx=10, pady=5, sticky='e')

        submit = tk.Button(submit_frame, text='Submit', font=small_font, command=self.Update)
        submit.pack(side='bottom', fill='x')

        self.first.set(vals[0][0])
        self.last.set(vals[0][1])
        self.v_age.set(vals[0][2])
        self.v_gender.set(vals[0][3])
        self.v_date.set(vals[0][4])
        self.v_hos_id.set(vals[0][5])
        self.v_scan_id.set(vals[0][6])
        self.v_scan_type.set(vals[0][7])
        self.v_indication.set(vals[0][8])
        self.findings_entry.insert(1.0, vals[0][9])
        self.v_conclusion.set(vals[0][10])
        self.v_docs.set(vals[0][11])

    def Update(self):

        self.values = Values()
        self.test = self.values.validate(self.first.get(), self.last.get(), self.v_age.get(), self.v_gender.get(),
                                         self.v_date.get(), self.v_hos_id.get(), self.v_scan_id.get(),
                                         self.v_scan_type.get(), self.v_conclusion.get(), self.v_docs.get())

        if (self.test == 'OK'):

            try:
                # print(self.first.get(), self.last.get(), self.v_age.get(), self.v_gender.get(), self.v_date.get(),
                # self.v_hos_id.get(), self.v_scan_id.get(), self.v_scan_type.get(), self.v_indication.get(),
                # self.findings_entry.get('1.0', tk.END), self.v_conclusion.get(), self.v_docs.get())
                self.database.update(self.first.get(), self.last.get(), self.v_age.get(), self.v_gender.get(),
                                     self.v_date.get(), self.v_hos_id.get(), self.v_scan_id.get(),
                                     self.v_scan_type.get(), self.v_indication.get(),
                                     self.findings_entry.get('1.0', tk.END), self.v_conclusion.get(), self.v_docs.get())





            except Exception as err:
                messagebox.showerror("Error", "Record not successfully updated. \n" + str(err))


            else:
                messagebox.showinfo('Success', 'Records successfully updated.')
                # self.clear()

        else:
            self.message = 'Invalid input in field {}'.format(self.test)
            messagebox.showerror("Error", self.message)


class Display(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.database = Database()
        self.data = self.database.display()

        self.header = tk.Frame(self, bd=4)
        self.header.pack(side='top', expand=True, anchor='n')
        # footer = tk.Frame(self).pack(side='bottom')

        self.add_button = tk.Button(self.header, text='New Record', cursor='hand2',
                                    command=lambda: controller.show_frame(Add))
        self.add_button.pack(side='left', padx=10, pady=5)

        self.delete_button = tk.Button(self.header, text='Delete Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Delete))
        self.delete_button.pack(side='left', padx=10, pady=5)
        self.search_button = tk.Button(self.header, text='Search', cursor='hand2',
                                       command=lambda: controller.show_frame(Search))
        self.search_button.pack(side='left', padx=10, pady=5)
        self.display_button = tk.Button(self.header, text='Display Record', cursor='hand2',
                                        command=lambda: controller.show_frame(Display))
        self.display_button.pack(side='left', padx=10, pady=5)
        self.exit_button = tk.Button(self.header, text='Exit', cursor='hand2',
                                     command=Quit)
        self.exit_button.pack(side='left', padx=10, pady=5)

        self.body = tk.Frame(self)
        self.body.pack(side='top', fill='both', expand=True, anchor='n')

        tk.Label(self.body, text="Record List").pack(side='top')

        self.display = ttk.Treeview(self.body)
        self.display.pack(fill='both')

        self.display['show'] = 'headings'
        self.display['columns'] = (
            'first_name', 'last_name', 'age', 'gender', 'date', 'hospital_id', 'scan_id', 'doctors')

        self.display.heading('first_name', text='First Name')
        self.display.heading('last_name', text='Last Name')
        self.display.heading('age', text='Age')
        self.display.heading('gender', text='Gender')
        self.display.heading('date', text='Date')
        self.display.heading('hospital_id', text='Hospital ID')
        self.display.heading('scan_id', text='Scan ID')
        self.display.heading('doctors', text='Doctors')

        self.display.column('age', width=100, stretch=tk.NO)
        self.display.column('gender', width=100, stretch=tk.NO)
        self.display.column('date', width=100, stretch=tk.NO)
        self.display.column('scan_id', width=100, stretch=tk.NO)
        self.display.column('hospital_id', width=100, stretch=tk.NO)

        for d in self.data:
            display_data = d[:7] + tuple([d[-1]])
            self.display.insert('', 'end', values=display_data)


app = HospitalRecordManagement()
app.mainloop()
