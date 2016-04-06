from requests import post

def ixio(text):
	data = {"f:1": text}
	url = post("http://ix.io", data=data)
	return url.text
