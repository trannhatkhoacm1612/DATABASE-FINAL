import mysql.connector
import argparse
import subprocess
from bs4 import BeautifulSoup
import time



# Thiết lập mã dịch thành 65001
subprocess.call('chcp 65001', shell=True)
# biến parser
parser = argparse.Aparser = argparse.ArgumentParser(description='Chương trình của bạn')

parser.add_argument('--n1', type=str, help='Tên cơ sở dữ liệu') # name database
parser.add_argument('--n2', type=str, help='Tên cơ sở dữ liệu') # name database
parser.add_argument('--sn', type=str, help='Tên trường') # school name
parser.add_argument('--y', type=str, help='Năm học') # year
parser.add_argument('--t', type=str, help='Xếp loại') # type
parser.add_argument('--c', type=int, help='Chọn cách truy vấn') # choice

# option
# parser.add_argument('--u', type=str, help='Tên người dùng') # user
# parser.add_argument('--p', type=str, help='Mật khẩu') # password

args = parser.parse_args()
# user = args.u
# password = args.p
dbname1 = args.n1
dbname2 = args.n2
sn = args.sn
y = args.y
t = args.t
c = args.c


def querry(dbname_,sn_,y_,t_,choice_):
    mydb = mysql.connector.connect(host="localhost",user="root", password="khoa16122004", database=dbname_,charset='utf8mb4')
    cursor = mydb.cursor()
    sql_1 = """
            select hs.HO,hs.TEN,hs.NTNS,h.DIEMTB,h.XEPLOAI,h.KETQUA
            from HOC as h
            join TRUONG as t on h.MATR = t.MATR
            join HS as hs on h.MAHS = hs.MAHS
            where t.TENTR = %s
            AND h.NAMHOC = %s
            AND h.XEPLOAI = %s;
        """
    
    sql_2 = """
            Select hs.ho, hs.ten, hs.NTNS, h.DIEMTB, h.XEPLOAI, h.KETQUA
            from HS AS hs, HOC AS h, TRUONG AS t
            where hs.MAHS = h.MAHS
            AND h.MATR = t.MATR
            AND t.TENTR = %s
            AND h.NAMHOC = %s
            AND h.XEPLOAI = %s;
        """
    
    sql = sql_1
    if choice_ == 2:
        sql = sql_2

    val = (sn_,y_,t_) # giá trị input trong câu truy vấn

    start_time = time.time() # đo thời gian
    cursor.execute(sql,val) # thực hiện truy vấn
    end_time = time.time() # đo thời gian
    total_time = end_time - start_time # tổng thời gian
    print(f"Tổng thời gian truy vấn {dbname_}: {total_time}")

    result = cursor.fetchall() # list ghi kết quả
    re = ["Họ","Tên","NTNS","DIEMTB","XEPLOAI","KETQUA"]
    xml = BeautifulSoup('','xml') # Đối tượng BS
    root_main = xml.new_tag("data") # tạo tag root chính
    xml.append(root_main)
    for item in result: # duyệt các field để create root_child
        name_root = "row" # root_child từng mẫu truy vấn
        root = xml.new_tag(name_root) # tạo root_child 
        root_main.append(root) # thêm vào root chính

        i = 0 # biến index chạy song song với field
        for field in re:
            tag = xml.new_tag(field)
            tag.string = str(item[i])
            root.append(tag)
            i += 1
    with open(f"{dbname_}.xml","w",encoding="utf8") as file:
        file.write(xml.prettify()) # ghi file
        
    print(f"{dbname_}.xml đã được ghi")
        # i += 11
        # if i == 20:
        #     break



def main():

    querry(dbname1,sn,y,t,c)
    querry(dbname2,sn,y,t,c)



if __name__ == '__main__':
    main()
