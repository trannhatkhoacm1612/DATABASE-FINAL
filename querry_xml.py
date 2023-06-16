import argparse
import xml.etree.ElementTree as ET



# Biến parser
parser = argparse.ArgumentParser(description="Querry xml")
parser.add_argument('--f', type=str, help='Tên file xml') # file xml input
parser.add_argument('--s', type=float, help='Ngưỡng điểm bắt đầu') # Ngưỡng start
parser.add_argument('--e', type=float,help='Ngưỡng điểm sau cùng') # Ngưỡng end

args = parser.parse_args()

file = args.f
threshold = (args.s,args.e)



# Hàm truy suất và so sánh dữ kiện
def querry(file_,threshold):
    tree = ET.parse(file_) # lấy tree grafh của file
    root = tree.getroot() # lấy tag root cao nhất
    for row_tag in root: # duyệt từng phần tử của tag root
        DTB = float(row_tag.find("DIEMTB").text.strip()) # lấy tag <DIEMTB>
        if threshold[0] <= DTB <= threshold[1]: # Kiểm điều kiện
            print(row_tag.find("Họ").text.strip(),row_tag.find("Tên").text.strip()) # print ra kết quả


def main():
    querry(file,threshold) 


if __name__ == '__main__':
    main()