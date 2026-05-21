class MT500Parser:

    def __init__(self):
        print("MT500 Parser Initialized")

    def parse_message(self, message):

        parsed_data = {
            "message_type": message.get("message_type"),
            "sender": message.get("sender"),
            "receiver": message.get("receiver")
        }

        return parsed_data


sample_message = {
    "message_type": "MT500",
    "sender": "BANKAAAAXXX",
    "receiver": "BANKBBBBXXX"
}

parser = MT500Parser()

result = parser.parse_message(sample_message)

print(result)