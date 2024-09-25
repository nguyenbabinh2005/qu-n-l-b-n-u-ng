import json

class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.name} - Giá: {self.price} - Tồn kho: {self.stock}"

class Store:
    def __init__(self):
        self.products = []
        self.load_products()

    def load_products(self):
        try:
            with open('products.json', 'r') as file:
                products_data = json.load(file)
                for data in product_data:
                    product = Product(data['name'], data['price'], data['stock'])
                    self.products.append(product)
        except FileNotFoundError:
            print("Không tìm thấy file sản phẩm. Bắt đầu với danh sách trống.")

    def save_products(self):
        with open('products.json', 'w') as file:
            products_data = [{'name': p.name, 'price': p.price, 'stock': p.stock} for p in self.products]
            json.dump(products_data, file)

    def add_product(self, product):
        self.products.append(product)
        print(f"Đã thêm {product.name} vào cửa hàng.")

    def remove_product(self, product_name):
        self.products = [p for p in self.products if p.name != product_name]
        print(f"Đã xóa {product_name} khỏi cửa hàng.")
    def list_products(self):
        if not self.products:
            print("Không có sản phẩm nào.")
        else:
            for product in self.products:
                print(product)

    def find_product(self, product_name):
        for product in self.products:
            if product.name == product_name:
                return product
        return None

    def update_product(self, product_name, price=None, stock=None):
        product = self.find_product(product_name)
        if product:
            if price is not None:
                product.price = price
            if stock is not None:
                product.stock = stock
            print(f"Cập nhật thành công {product.name}.")
        else:
            print(f"Không tìm thấy sản phẩm: {product_name}")

class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.order_history = []

    def add_order(self, order):
        self.order_history.append(order)

    def list_orders(self):
        if not self.order_history:
            print("Không có đơn hàng nào.")
        else:
            for i, order in enumerate(self.order_history, start=1):
                print(f"Đơn hàng {i}:")
                print(order)
                print(f"Tổng giá: {order.total_price()}")

    def __str__(self):
        return f"{self.name} - Số điện thoại: {self.phone}"

class CustomerManager:
    def __init__(self):
        self.customers = []

    def add_customer(self, customer):
        self.customers.append(customer)
        print(f"Đã thêm khách hàng: {customer.name}")

    def remove_customer(self, phone):
        self.customers = [c for c in self.customers if c.phone != phone]
        print(f"Đã xóa khách hàng có số điện thoại: {phone}")

    def list_customers(self):
        if not self.customers:
            print("Không có khách hàng nào.")
        else:
            for customer in self.customers:
                print(customer)

class Order:
    def __init__(self):
        self.items = []
        self.discount = 0

    def add_item(self, product, quantity):
        if product.stock >= quantity:
            self.items.append((product, quantity))
            product.stock -= quantity
            print(f"Đã thêm {quantity} của {product.name} vào đơn hàng.")
        else:
            print(f"Không đủ hàng cho {product.name}.")

    def apply_discount(self, discount):
        self.discount = discount
        print(f"Đã áp dụng giảm giá: {discount}%")

    def total_price(self):
        total = sum(item.price * quantity for item, quantity in self.items)
        if self.discount:
            total *= (1 - self.discount / 100)
        return total

    def __str__(self):
        order_details = []
        for product, quantity in self.items:
            order_details.append(f"- {product.name}: {quantity} cái")
        return "\n".join(order_details)

class OrderManager:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)
        print("Đơn hàng đã được lưu.")

    def list_orders(self):
        if not self.orders:
            print("Không có đơn hàng nào.")
        else:
            for i, order in enumerate(self.orders, start=1):
                print(f"Đơn hàng {i}:")
                print(order)
                print(f"Tổng giá: {order.total_price()}")

class Report:
    @staticmethod
    def calculate_revenue(orders):
        total_revenue = sum(order.total_price() for order in orders)
        return total_revenue

def main():
    store = Store()
    order_manager = OrderManager()
    customer_manager = CustomerManager()

    while True:
        print("\n--- MENU ---")
        print("1. Thêm sản phẩm")
        print("2. Xóa sản phẩm")
        print("3. Liệt kê sản phẩm")
        print("4. Cập nhật sản phẩm")
        print("5. Thêm khách hàng")
        print("6. Xóa khách hàng")
        print("7. Liệt kê khách hàng")
        print("8. Tạo đơn hàng")
        print("9. Liệt kê đơn hàng")
        print("10. Báo cáo doanh thu")
        print("11. Lưu dữ liệu")
        print("0. Thoát")
        choice = input("Chọn một tùy chọn: ")

        if choice == '1':
            name = input("Nhập tên sản phẩm: ")
            price = float(input("Nhập giá sản phẩm: "))
            stock = int(input("Nhập số lượng tồn kho: "))
            product = Product(name, price, stock)
            store.add_product(product)

        elif choice == '2':
            name = input("Nhập tên sản phẩm cần xóa: ")
            store.remove_product(name)

        elif choice == '3':
            print("Danh sách sản phẩm:")
            store.list_products()

        elif choice == '4':
            name = input("Nhập tên sản phẩm cần cập nhật: ")
            price = float(input("Nhập giá mới (hoặc để trống để không cập nhật): ") or 0)
            stock = int(input("Nhập số lượng mới (hoặc để trống để không cập nhật): ") or 0)
            store.update_product(name, price if price else None, stock if stock else None)

        elif choice == '5':
            name = input("Nhập tên khách hàng: ")
            phone = input("Nhập số điện thoại: ")
            customer = Customer(name, phone)
            customer_manager.add_customer(customer)

        elif choice == '6':
            phone = input("Nhập số điện thoại khách hàng cần xóa: ")
            customer_manager.remove_customer(phone)

        elif choice == '7':
            print("Danh sách khách hàng:")
            customer_manager.list_customers()

        elif choice == '8':
            order = Order()
            customer_phone = input("Nhập số điện thoại khách hàng (hoặc để trống nếu không có): ")
            if customer_phone:
                customer = next((c for c in customer_manager.customers if c.phone == customer_phone), None)
                if customer:
                    print(f"Đang tạo đơn hàng cho khách hàng: {customer.name}")
                else:
                    print("Khách hàng không tồn tại.")

            while True:
                product_name = input("Nhập tên sản phẩm để thêm vào đơn hàng (hoặc nhập 'done' để hoàn tất): ")
                if product_name.lower() == 'done':
                    break
                product = store.find_product(product_name)
                if product:
                    quantity = int(input("Nhập số lượng: "))
                    order.add_item(product, quantity)
                else:
                    print("Sản phẩm không tồn tại.")

            discount = float(input("Nhập phần trăm giảm giá (hoặc 0 nếu không có): "))
            if discount > 0:
                order.apply_discount(discount)

            if customer:
                customer.add_order(order)

            order_manager.add_order(order)

        elif choice == '9':
            order_manager.list_orders()

        elif choice == '10':
            total_revenue = Report.calculate_revenue(order_manager.orders)
            print(f"Tổng doanh thu: {total_revenue}")

        elif choice == '11':
            store.save_products()

        elif choice == '0':
            print("Cảm ơn bạn đã sử dụng ứng dụng!")
            break

        else:
            print("Tùy chọn không hợp lệ. Vui lòng chọn lại.")

if __name__ == "__main__":
    main()
