

String paintings_url = "http://localhost:8888/data/paintings";

JSONArray paintings_list = new JSONArray();

void update_paintings_data() {
  PaintingDataUpdateThread p = new PaintingDataUpdateThread();
  p.start();
  
  for (int i = 0; i < paintings_list.size(); ++i) {
    JSONObject painting_data = paintings_list.getJSONObject(i);
    if (!paintings.containsKey(painting_data.getInt("id"))) {
      new Painting(painting_data);
    }
  }
}


class PaintingDataUpdateThread extends Thread {
  PaintingDataUpdateThread() {}

  public void run() {
    paintings_list = loadJSONObject(paintings_url).getJSONArray("paintings");
  }
}
