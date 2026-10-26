package com.fal.fal4mir.data;

import android.util.Log;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class FalApi {
    private static final String TAG = "FalApi";
    private static final int TIMEOUT = 12000;
    private static final String API_URL = "https://4mir.ir/fall/api.php";

    public static class FalData {
        public String number;
        public String ghazal;
        public String tabir;
        public String imageUrl;
        public String voiceUrl;
        public String link;
    }

    public static FalData fetch() {
        try {
            String json = httpGet(API_URL);
            if (json == null) return null;

            JSONObject root = new JSONObject(json);
            if (root.optInt("status") != 200) {
                Log.w(TAG, "API status not 200");
                return null;
            }

            JSONObject result = root.optJSONObject("result");
            if (result == null) return null;

            FalData data = new FalData();
            data.number = result.optString("number", "—");
            data.ghazal = result.optString("ghazal", "");
            data.tabir = result.optString("tabir", "");
            data.imageUrl = result.optString("image", "");
            data.voiceUrl = result.optString("voice", "");
            data.link = result.optString("link", "");

            return data;
        } catch (Exception e) {
            Log.e(TAG, "fetch error", e);
            return null;
        }
    }

    private static String httpGet(String urlStr) {
        try {
            URL url = new URL(urlStr);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setConnectTimeout(TIMEOUT);
            conn.setReadTimeout(TIMEOUT);
            conn.setRequestProperty("User-Agent", "Fal4mir/1.0");

            if (conn.getResponseCode() != 200) return null;

            BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) sb.append(line);
            br.close();
            return sb.toString();
        } catch (Exception e) {
            Log.e(TAG, "httpGet error", e);
            return null;
        }
    }
}
