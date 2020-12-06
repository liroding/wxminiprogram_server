import xlwt
import pymysql
import sys

class MYSQL:

    def connectDB(self):
        try:
            self._connect = pymysql.Connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='dingyinglai',
                db='mysite_mysqldb',
                charset='utf8'
            )
            print('success')
            return 0
        except:
            return -1

    def export(self, table_name, output_path):
        self._cursor = self._connect.cursor()
        count = self._cursor.execute('select * from '+table_name)
        # print(self._cursor.lastrowid)
        #print(count)
        
        self._cursor.scroll(0, mode='absolute')
        
        results = self._cursor.fetchall()

        fields = self._cursor.description
        workbook = xlwt.Workbook()

        #sheet = workbook.add_sheet('table_'+table_name, cell_overwrite_ok=True)
        sheet = workbook.add_sheet(table_name, cell_overwrite_ok=True)

        for field in range(0, len(fields)):
            sheet.write(0, field, fields[field][0])

        row = 1
        col = 0
        for row in range(1,len(results)+1):
            for col in range(0, len(fields)):
                sheet.write(row, col, u'%s' % results[row-1][col])

        workbook.save(output_path)


     
    def convert(self, table_name, output_path):

        mysql = MYSQL()
        flag = mysql.connectDB()
        if flag == -1:
           print('db connect failed')
        else:
           print('db connect success')
           mysql.export(table_name, output_path)
    
'''
mysql = MYSQL()
print(sys.argv[1])
print(sys.argv[2])

flag = mysql.connectDB()
if flag == -1:
      print('db connect failed')
else:
      print('db connect success')
      mysql.export(sys.argv[1], sys.argv[2])
'''    
