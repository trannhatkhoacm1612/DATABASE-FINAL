import json
import random
import mysql.connector
import subprocess
import argparse
import tqdm

# Thiết lập mã dịch thành 65001
subprocess.call('chcp 65001', shell=True)


# Biến parser
parser = argparse.ArgumentParser(description='Chương trình của bạn')

parser.add_argument('--u', type=str, help='Tên người dùng') # user
parser.add_argument('--n', type=str, help='Tên cơ sở dữ liệu') # database_name
parser.add_argument('--p', type=str, help='Mật khẩu') # password

args = parser.parse_args()
user = args.u
dbname = args.n
password = args.p




# hàm random years
def gender_date(years):
    return r"/".join([str(random.randint(1,29)),str(random.randint(1,13)),str(years)])


# hàm gender bảng HS
def gender_HS(json_file,number):
    # json_file là file danh sách họ ,tên đệm
    # number là số mẫu cần tạo    

    with open(json_file, "r",encoding="utf8") as file:
        count = 1
        di = json.load(file) # đọc file json
        ten = di['ten']
        ten_dem = di['ten_dem'] # list chứa tên
        ho = di['ho'] # list chứa họ
        diachi = di['diachi'] # list chứa địa chỉ
        Name = [] # list chính
        for count in tqdm.tqdm(range(number),"HS generating proccess"):
            name = [str(count + 1),random.choice(ho),' '.join([random.choice(ten_dem),random.choice(ten)]),str(random.randint(100000000000,999999999999)),gender_date(2004),random.choice(diachi)]
            random.seed(count + 1) # seed phân biệt random
            Name.append(name) # thêm vào Name

        return Name


# Hàm gender bảng TRUONG
def gender_Truong(json_file,number):
    # input tương tự trên

    with open(json_file,"r",encoding="utf8") as file:
        di = json.load(file) # đọc file json
        Truong = [] # list chính
        for count in tqdm.tqdm(range(number),"Truong generating proccess"):
            truong = [count + 1,list(di[count].values())[0],list(di[count].values())[1]]
            Truong.append(truong) 
            # count += 1
    return Truong


# Hàm set xếp loại
def xep_loai(score):
    if score >= 9:
        return "Xuất sắc"
    elif score >= 8:
        return "Giỏi"
    elif score >= 6:
        return "Khá"
    elif score >= 5:
        return "Trung bình"
    else:
        return "Yếu"
    
# Hàm Gender bảng HOC
def gender_Hoc(students,schools):
    # students là list ứng với tabel HS
    # schools là list ứng với tabel TRUONG

    seed = 0 # seed random
    Hoc = [] # List chính
    i = 0 # Biến chạy học sinh song song for item
    ketquas = ["Hoàn thành", "Chưa hoàn thành"]
    random.seed(seed)
    for hocsinh in tqdm.tqdm(students,"Hoc generating process"):
        random.seed(seed) # seed random
        matruong = schools[seed % 99 ][0] # lấy modulo vì school có len là 100
        mahs =students[i][0]
        for years in range(2020, 2023): # tương ứng 3 năm học : 2020, 2021,2022
            score = round(random.uniform(1,10),2) # random score và làm tròn hai chữ số thập phân
            ketqua = random.choice(ketquas) # chọn random ketqua
            Hoc.append([matruong,mahs,years,score,xep_loai(score),ketqua])
        seed += 1
        i += 1

    return Hoc




# hàm insert vào database
def insert_DB(dbname_,user_,password_,schools,students,studies):
    # dbname_ là tên database muốn insert
    # user_ là người host
    # password_ là mk của user
    # schools, students, studies tương ứng là ba list tương ứng với 3 bảng


    mydb = mysql.connector.connect(host="localhost",user=user_,password=password_,database=dbname_,charset='utf8mb4') # connect database_
    cursor = mydb.cursor()
    for item in tqdm.tqdm(schools,"Inserting truong process"):
        sql = "INSERT INTO truong(matr,tentr,diachitr) values (%s,%s,%s)"
        val = tuple(item)
        cursor.execute(sql,val) # thực hiện insert
    for item in tqdm.tqdm(students,"Inserting students process"):
        sql = "INSERT INTO hs(MAHS,HO,TEN,CCCD,NTNS,DCHI_HS) values(%s,%s,%s,%s,%s,%s)"
        val = tuple(item)
        cursor.execute(sql,val) # thực hiện insert
    for item in tqdm.tqdm(studies,"Inserting studies process"):
        sql = "INSERT INTO hoc(MATR,MAHS,NAMHOC,DIEMTB,XEPLOAI,KETQUA) values(%s,%s,%s,%s,%s,%s)"
        val = tuple(item)
        cursor.execute(sql,val) # thực hiện insert
    mydb.commit() # lưu






def main():
    schools = gender_Truong(r"./data/TRUONG.json",100)
    students = gender_HS(r"./data/HS.json",1000000)
    studies = gender_Hoc(students,schools)
    insert_DB(dbname,user,password,schools,students,studies)

if __name__ == '__main__':
    main()



