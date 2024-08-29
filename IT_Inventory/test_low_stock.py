from server import check_low_stock, send_email, load_inventory

def test_check_low_stock():
    low_stock_items = check_low_stock()
    print("Low Stock Items:")
    for item in low_stock_items:
        print(item)

def test_send_email():
    subject = "Test Low Stock Alert"
    body = "This is a test email for low stock alert."
    send_email(subject, body)
    print("Test email sent.")

if __name__ == "__main__":
    # Test low stock check
    test_check_low_stock()

    # Test sending email (ensure your email credentials are correct)
    test_send_email()
