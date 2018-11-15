import re

read = re.compile(r"([a-zA-Z]+) = input\(\)")
write = re.compile(r"print\((.+)\)")
loop = re.compile(r"while(.+)")
branch = re.compile(r"if(.+)")
