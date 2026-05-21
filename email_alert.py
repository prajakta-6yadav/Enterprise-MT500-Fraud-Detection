import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart


class EnterpriseEmailAlert:

    def __init__(

        self,

        sender_email,

        sender_password,

        receiver_email

    ):

        self.sender_email = sender_email

        self.sender_password = sender_password

        self.receiver_email = receiver_email

        print(

            "Enterprise Email Alert Engine Initialized"

        )

    def send_fraud_alert(

        self,

        alert_data

    ):

        severity = alert_data.get(

            "severity",

            "LOW"

        )

        subject = (

            f"[{severity}] "

            "MT500 Fraud Alert"

        )

        body = f"""

Enterprise SWIFT Fraud Alert

Transaction Reference:
{alert_data.get('transaction_reference')}

Sender:
{alert_data.get('sender')}

Receiver:
{alert_data.get('receiver')}

Risk Score:
{alert_data.get('risk_score')}

Severity:
{alert_data.get('severity')}

Status:
{alert_data.get('status')}

Timestamp:
{alert_data.get('timestamp')}

"""

        message = MIMEMultipart()

        message["From"] = self.sender_email

        message["To"] = self.receiver_email

        message["Subject"] = subject

        message.attach(

            MIMEText(

                body,

                "plain"

            )

        )

        try:

            server = smtplib.SMTP(

                "smtp.gmail.com",

                587

            )

            server.starttls()

            server.login(

                self.sender_email,

                self.sender_password

            )

            server.sendmail(

                self.sender_email,

                self.receiver_email,

                message.as_string()

            )

            server.quit()

            print(

                "\nEnterprise Email Alert Sent"

            )

        except Exception as error:

            print(

                "\nEmail Alert Error:",

                error

            )