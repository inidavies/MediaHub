import requests, json
import movie


def main():
  movie.get_movies('Thor')
  database = movie.create_database()
  dicts = []
  for i in database:
    Title = i[0]
    Release = i[1]
    Trailer = i[2]
    dicts.append({'Movie' : Title, 'Release_Date' : Release, 'Trailer_Link' : Trailer})
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