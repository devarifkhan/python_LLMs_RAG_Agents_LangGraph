import tiktoken


enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey there! My name is Md Ariful Islam"
tokens = enc.encode(text)


print("Tokens", tokens)

decoded = enc.decode(tokens)
print("Decoded:", decoded)

