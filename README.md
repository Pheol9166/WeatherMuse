# WeatherMuse
Music Recommend Discord Bot based on Today's Weather

⁕ You need your discord bot token and server id!

<img src=https://user-images.githubusercontent.com/112241898/235357087-d8b2ea72-942d-4891-8338-5dfcec86ca1a.png height=400 weight=200>

## Playlist
It consists of four weather categories
- Clear: Clear weather
- Rain: Rain, Drizzle, Squall, Tornado, Thunderstorm
- Clouds: Clouds, Haze, Fog, Mist, Ash, Dust, Smoke, Sand
- Snow: Snow

Each song is JSON type, and it consists of title, artist, and URL. 

ex)
{
  "title": "title of song"
  "artist": "artist of song"
  "URL": "URL of song"
}
## Slash Commands
### Recommend
- /추천: WeatherMuse recommends you a song that suits today's weather when it gets city!
<img src=https://user-images.githubusercontent.com/112241898/235358376-0115d620-a1fd-4ba4-bd24-1d65890c4663.png height=300 weight=100>

### Edit
- /노래_추가: add a new song to playlist in WeatherMuse
<img src=https://user-images.githubusercontent.com/112241898/235358985-a7458867-a388-4f57-aa77-b9279201cf45.png height=300 weight=100>

- /노래_제거: delete the song in playlist when WeatherMuse gets weather and song title
<img src=https://user-images.githubusercontent.com/112241898/235359736-894adc96-5fa8-41c1-b24a-38ceb24a832c.png height=200 weight=100>

- /제목_변경: Edit song's title when WeatherMuse gets weather and song title
<img src=https://user-images.githubusercontent.com/112241898/235360494-f835733d-fef1-4f1f-a600-253ca2e921bb.png height=200 weight=100>

- /가수_변경: Edit song's artist when WeatherMuse gets weather and song title
<img src=https://user-images.githubusercontent.com/112241898/235360434-d9e820da-400f-49e8-9904-ed02317c1f3d.png height=200 weight=100>

- /url_변경: Edit song's URL when WeatherMuse gets weather and song title
<img src=https://user-images.githubusercontent.com/112241898/235360259-95d055bd-ec4c-4bd8-bfc5-f24cde29c7a8.png height=200 weight=200>

### Search
- /종합_검색: Search Song in playlist based on song title and artist
<img src=https://user-images.githubusercontent.com/112241898/235360547-4d5232d7-f009-4a42-99d9-8039099c7f41.png height=300 weight=100>

- /제목으로_검색: Search Song in playlist based on song title
<img src=https://user-images.githubusercontent.com/112241898/235360617-e1b60df8-6049-4dbe-aa71-66fd443b664e.png height=300 weight=100>

- /가수로_검색: Search Song in playlist based on artist
<img src=https://user-images.githubusercontent.com/112241898/235360335-d4b6cb25-b41d-49a3-9ea8-ff9d12be4ada.png height=400 height=300>
