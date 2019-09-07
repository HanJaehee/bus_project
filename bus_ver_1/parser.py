from xml.etree.ElementTree import parse

tree = parse('data.xml')
root = tree.getroot()

student = root.findall("student")

#name = student.findtext("name")
#print(name)
name = []
for x in student:
    name.append(x.findtext("name"))
#name = [x.findtext("name") for x in student]
print(name)
"""
age = [x.findtext("age") for x in student]
score = [x.find("score").attrib for x in student]

print(name)
print(age)
print(score)
"""