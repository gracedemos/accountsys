from hashlib import sha256
import os
import json

f = open("data.json", 'r')
file_data = json.load(f)
f.close()

class masspass():
	def __init__(self):
		self.data = file_data

	def add(self, pass_data):
		n = 0
		for i in self.data["passwords"]:
			if i["user"] == pass_data["user"]:
				n = 1
				return "Username Taken"
		if n == 0:
			self.data["passwords"].append(pass_data)
			return "Addition Successful"


	def prep(self, user, passw):
		passw = sha256(passw.encode()).hexdigest()
		nid = os.urandom(16).hex()
		ret = {
			"user": user,
			"pass": passw,
			"id": nid
		}
		return ret

	def finalize(self):
		f = open("data.json", 'w')
		json.dump(self.data, f, indent = 4)
		f.close()

	def verify_prep(self, user, passw):
		ret = {
			"user": user,
			"pass": passw
		}
		return ret

	def verify(self, pass_data):
		passw = sha256(pass_data["pass"].encode()).hexdigest()
		for i in self.data["passwords"]:
			if(i["user"] == pass_data["user"]):
				if(i["pass"] == passw):
					return "Password Verified"
				else:
					return "Password Could Not Be Verified"
		return "Password Could Not Be Verified"

	def get_id(self, user):
		ID = ""
		for i in self.data["passwords"]:
			if(i["user"] == user):
				ID = i["id"]
		return ID