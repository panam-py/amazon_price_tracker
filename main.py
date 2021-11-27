from bs4 import BeautifulSoup
import requests
import smtplib

AMAZON_LINK = input("Enter the link of the product you want to track: ")
user_price = float(input("Enter your desired price: "))
email_address = input("Enter your email address: ")

headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

response = requests.get(AMAZON_LINK, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

product_price = soup.select_one(selector="#price_inside_buybox").getText().strip()
product_price = product_price.split("$")[1].replace(",", "")
product_price = float(product_price)

product_name = soup.select_one(selector="#productTitle").getText().strip()

print(product_name)
print(product_price)

if product_price > user_price:
    print(f"The current price of the {product_name} is {product_price} which is ${product_price-user_price} above your budget. A mail will be sent to you once it is within your budget")
else:
    print(f"The product, {product_name} has a price of {product_price}, which is within your budget of {user_price}")
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(sender_email, sender_password)
    connection.sendmail(from_addr="panampraisehebron@gmail.com", to_addrs=email_address, msg=f"Subject:Amazon Automated Price Checker\n\n The product which you asked me to check: {product_name} is now {product_price} which is within your set budget of {user_price}.\n Hurry and buy now.")
    connection.close()
    print(f"Mail has been sucessfully sent to your email address: {email_address}")
