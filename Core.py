from MainGUI import Ui_MainWindow
from AddBook import Add_Dialog
from AddMember import member_Dialog
from ViewBook import View_Books_Dialog
from ViewMember import View_Members_Dialog
import mysql.connector as mc

from PyQt6.QtWidgets import *

my_db = mc.connect(
    host='localhost',
    user='root',
    password='',
    database='library'
)
cursor = my_db.cursor()

class LibrarySyatem(QMainWindow, Ui_MainWindow):
  def __init__(self) -> None:
    super().__init__()
    self.setupUi(self)
    self.show()

    self.toolButton_addbook.clicked.connect(self.add_book)
    self.toolButton_addmember.clicked.connect(self.add_member)
    self.toolButton_viewbook.clicked.connect(self.view_books)
    self.toolButton_viewmember.clicked.connect(self.view_members)
    self.toolButton_issue.clicked.connect(self.issue_book)
    self.toolButton_submit.clicked.connect(self.submit_book)
    self.toolButton_renew.clicked.connect(self.renew_book)

    self.lineEdit_bookid.returnPressed.connect(self.search_book)
    self.lineEdit_memberid.returnPressed.connect(self.search_member)
    self.lineEdit_submission.returnPressed.connect(self.issued_book)

  def add_book(self):
    dialog = QDialog()
    ui = Add_Dialog()

    ui.setupUi(dialog)
    dialog.exec()

  def add_member(self):
    dialog = QDialog()
    ui = member_Dialog()

    ui.setupUi(dialog)
    dialog.exec()
  
  def view_books(self):
    dialog = QDialog()
    ui = View_Books_Dialog()

    ui.setupUi(dialog)
    dialog.exec()

  def view_members(self):
    dialog = QDialog()
    ui = View_Members_Dialog()

    ui.setupUi(dialog)
    dialog.exec()

  def search_book(self):
    try:
      if self.lineEdit_bookid.text() != '':
        id = int(self.lineEdit_bookid.text()) 
      else:return
    except:return
    try:
      cursor.execute(f'SELECT `title`, `author` FROM `addbook` WHERE id={id}')

      result = cursor.fetchall()
      
      for row in result:
        self.label_bookname.setText(row[0])
        self.label_bookauthor.setText(row[1])

        self.label_bookname.setStyleSheet('color:green')
        self.label_bookauthor.setStyleSheet('color:green')
      
      
    except mc.errors as e:
      pass
  
  def search_member(self):
    try:
      if self.lineEdit_memberid.text() != '':
        id = int(self.lineEdit_memberid.text()) 
      else:return
    except:return
    try:
      cursor.execute(f'SELECT `name`, `mobile` FROM `addmember` WHERE id={id}')

      result = cursor.fetchall()
      
      for row in result:
        self.label_membername.setText(row[0])
        self.label_contactinfo.setText(row[1])

        self.label_membername.setStyleSheet('color:green')
        self.label_contactinfo.setStyleSheet('color:green')
      
      
    except mc.errors as e:
      pass

  def issue_book(self):
    try:
      book_id = int(self.lineEdit_bookid.text())
      member_id = int(self.lineEdit_memberid.text())
    except:return
    try:
      cursor.execute(f"INSERT INTO `issue` (`bookID` , `memberID`) VALUES ({book_id} , {member_id})")
      result1 = cursor.fetchall()

      cursor.execute(f"UPDATE `addbook` SET `isAvilable` = FALSE WHERE id={book_id}")
      my_db.commit()

      self.lineEdit_bookid.setText('')
      self.lineEdit_memberid.setText('')

      self.label_bookname.setText("Book Name")
      self.label_bookauthor.setText("Book Author")

      self.label_membername.setText("Member Name")
      self.label_contactinfo.setText("Contact Info")

      QMessageBox.about(self , "Issue Book" , "Book Issued Successfully")

    except mc.errors as e:
      pass
  
  def issued_book(self):
    try:
      book_id = int(self.lineEdit_submission.text())
    except:return
    if not bool(book_id):
      return
    try:
      cursor.execute(f"SELECT * FROM `issue` WHERE bookID = {book_id}")
      result = cursor.fetchall()

      self.tableWidget_bookinfo.setRowCount(0)
      for row_num,row_data in enumerate(result):
        self.tableWidget_bookinfo.insertRow(row_num)
        for col_num , data in enumerate(row_data):
          self.tableWidget_bookinfo.setItem(row_num , col_num , QTableWidgetItem(str(data)))

    except mc.errors as e:
      pass

  def submit_book(self):
    try:
      book_id = int(self.lineEdit_submission.text())
      if not bool(book_id):return
    except:return
    try:
      q1 = f"DELETE FROM `issue` WHERE `bookID` = {book_id}"
      q2 = f"UPDATE `addbook` SET `isAvilable` = TRUE WHERE `id` = {book_id}"
      cursor.execute(q1)
      cursor.execute(q2)

      my_db.commit()
      QMessageBox.about(self , "Successe" , "Book Submited")
    except mc.errors as e:pass

  def renew_book(self):
    try:
      book_id = int(self.lineEdit_submission.text())
      if not bool(book_id):return    
    except :return
    try:
      q1 = f"UPDATE `issue` SET `issueTime`= DEFAULT,`renewCount`=`renewCount`+1 WHERE `bookID`={book_id}"
      cursor.execute(q1)
      my_db.commit()

      QMessageBox.about(self , "Renew Book" , "Done")
    except mc.errors as e: 
      print(e)