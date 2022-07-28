import requests, json
import movie


def main():
  movie.get_movies('Thor')
  c = movie.create_database()
  dicts = []
  keys = range(len(movie.create_database()))
  values = [1, 2, 3]
  for i in c:
    x = i[0]
    y = i[1]
    z = i[2]
    dicts.append({'1' : x, '2' : y, '3' : z})
  '''print(dicts)'''

  api_key = "701aMTQ3NjoxNDc0OmhCQTRnY3RMb29SdllBdTk"
  data = {
    "movie": dicts[0]
      }

  json_payload = {
    "data": json.dumps(data) ,
    "output_file": "output.pdf",
    "export_type": "json",
    "expiration": 1440,
    "template_id": "e2a77b2b1eb313c6"
    }

  response = requests.post(
    F"https://api.craftmypdf.com/v1/create",
    headers = {"X-API-KEY": F"{api_key}"},
    json = json_payload
    )

  print(response.content)

if __name__ == "__main__":
    main()