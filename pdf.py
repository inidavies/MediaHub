import requests, json

def main():
  database = [{'name': 'Teaching Developmentally Disabled Children', 'author': 'Ole Ivar Lovaas', 'link': 'http://books.google.com/books?id=qcW_QgAACAAJ&dq=me&hl=&cd=1&source=gbs_api', 'thumbnail': 'http://books.google.com/books/content?id=qcW_QgAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'}]
  dicts = []
  for i in database:
    Title = i["name"]
    Release = i["author"]
    Trailer = i["link"]
    dicts.append({'type' : Title, 'name' : Release, 'link' : Trailer})
  '''print(dicts)'''
  api_key = "22c0MTQ5MDoxNDg4OjVWMkxOV0tXY256VU54Q1Q"

  data = {
    "dicts": dicts
  }

  json_payload = {
    "data": json.dumps(data) ,
    "output_file": "output.pdf",
    "export_type": "json",
    "expiration": 1440,
    "template_id": "b4a77b2b1e383910"
    }

  response = requests.post(
    F"https://api.craftmypdf.com/v1/create",
    headers = {"X-API-KEY": F"{api_key}"},
    json = json_payload
    )

  print(response.content)

if __name__ == "__main__":
    main()