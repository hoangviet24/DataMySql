# Hướng dẫn sử dụng
## Đầu tiên là cấu hình
```
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}
conn = mysql.connector.connect(**db_config)
Cấu hình tương ứng với csdl
```
```
Chúng ta có các file json tương ứng với từng sản phẩm, nếu muốn thêm sản phẩm tạo file json tương ứng là được ví dụ, Card RTX 3050 sẽ là RTX3050.json
```
# Cuối cùng
tạo Category
```
Ở đây đã có các mẫu id sẵn tương ứng nên là hãy vô mysql để tạo tương ứng bằng câu lệnh sau
```
```
insert into categories('uuid tương ứng trong từng sản phẩm','name','type')
cách chèn cate như sau:
- uuid thì sẽ lấy từ categoryID trong file json, name sẽ là tên của sản phẩm đó, ví dụ chèn vào sản phẩm Intel Core I3 thì sẽ là Intel Core I3,type sẽ là CPU Intel tương ứng với lại CPU
```
$\rightarrow$ name sẽ là branch + thế hệ
$\rightarrow$ type sẽ là Model + branch 

