import uuid
import json
import os
import mysql.connector

# Kết nối MySQL
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}
conn = mysql.connector.connect(**db_config)

cursor = conn.cursor()

insert_product_query = """
    INSERT INTO products (id, name, sku, description, brand, price, quantity, thumbnail, category_id, is_featured)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

insert_image_query = """
    INSERT INTO product_images (product_id, image_url)
    VALUES (%s, %s)
"""

try:
    data_folder = "datafiles"
    inserted_count = 0
    skipped_count = 0

    for filename in os.listdir(data_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(data_folder, filename)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    if not content.strip():
                        print(f"⚠️ File rỗng, bỏ qua: {filename}")
                        continue
                    data = json.loads(content)
            except json.JSONDecodeError as e:
                print(f"❌ File JSON lỗi định dạng ({filename}): {e}")
                continue

            for item in data:
                cursor.execute("SELECT id FROM products WHERE sku = %s", (item["sku"],))
                result = cursor.fetchone()

                if result:
                    print(f"⛔ SKU '{item['sku']}' đã tồn tại. Bỏ qua.")
                    skipped_count += 1
                    continue

                product_id = str(uuid.uuid4())
                product_values = (
                    product_id,
                    item["name"],
                    item["sku"],
                    item["description"],
                    item["brand"],
                    item["price"],
                    item["quantity"],
                    item["thumbnail"],
                    item["categoryId"],
                    item["featured"]
                )

                cursor.execute(insert_product_query, product_values)

                for image_url in item["images"]:
                    cursor.execute(insert_image_query, (product_id, image_url))

                print(f"✅ Đã thêm sản phẩm: {item['name']}")
                inserted_count += 1

    conn.commit()
    print("\n🎉 Thêm dữ liệu hoàn tất!")
    print(f"✅ Tổng sản phẩm thêm mới: {inserted_count}")
    print(f"⛔ Tổng sản phẩm bỏ qua do trùng SKU: {skipped_count}")

except mysql.connector.Error as err:
    print(f"Lỗi MySQL: {err}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
