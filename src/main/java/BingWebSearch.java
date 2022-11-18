//Quicktart -> Rest APIs -> Java

import java.net.*;
import java.util.*;
import java.io.*;
import javax.net.ssl.HttpsURLConnection;

import com.google.gson.*;

public class BingWebSearch {

    // Add your Bing Search V7 subscription key to your environment variables.
    static String subscriptionKey = System.getenv("BING_SEARCH_V7_SUBSCRIPTION_KEY");
    static String endpoint = System.getenv("BING_SEARCH_V7_ENDPOINT") + "v7.0/search";

    // Add your own search terms, if desired.
   // static String searchTerm = "Samsung 635L";

    public static String OutputResults(String searchTerm){
        //System.out.println(subscriptionKey);
        String outputResult = "";
        System.out.println(endpoint);
        System.out.println(searchTerm);
        String json_text = "";
        try {
            System.out.println("Searching the Web for: " + searchTerm);
            outputResult += "Searching the Web for: " + searchTerm;
            SearchResults result = SearchWeb(searchTerm);

//            System.out.println("\nRelevant HTTP Headers:\n");
//            for (String header : result.relevantHeaders.keySet())
//                System.out.println(header + ": " + result.relevantHeaders.get(header));

            System.out.println("\nJSON Response:\n");
            outputResult += "\n\nJSON Response:\n";

            //System.out.println(result.jsonResponse);
            json_text = result.jsonResponse;
           // System.out.println(prettify(result.jsonResponse));
        } catch (Exception e) {
            e.printStackTrace(System.out);
            System.exit(1);
        }

        JsonParser parser = new JsonParser();
        JsonObject json = (JsonObject) parser.parse(json_text);
        Gson gson = new GsonBuilder().setPrettyPrinting().create();


        JsonObject webpages = (JsonObject) json.get("webPages");
        JsonArray values = webpages.getAsJsonArray("value");
        JsonObject obj1 = values.get(0).getAsJsonObject();
        JsonObject obj2 = values.get(1).getAsJsonObject();
        JsonObject obj3 = values.get(2).getAsJsonObject();
        JsonObject obj4 = values.get(3).getAsJsonObject();
        JsonObject obj5 = values.get(4).getAsJsonObject();
        JsonObject [] objects = {obj1, obj2, obj3, obj4, obj5};
        System.out.println(gson.toJson(obj1));
        System.out.println(gson.toJson(obj2));
        System.out.println(gson.toJson(obj3));
        System.out.println(gson.toJson(obj4));
        System.out.println(gson.toJson(obj5));

        outputResult = relevantCriterion(objects);

        System.out.println(outputResult);
        return outputResult;
    }

    public static SearchResults SearchWeb (String searchQuery) throws Exception {
        // Construct URL of search request (endpoint + query string)
        URL url = new URL(endpoint + "?q=" +  URLEncoder.encode(searchQuery, "UTF-8"));
        HttpsURLConnection connection = (HttpsURLConnection)url.openConnection();
        connection.setRequestProperty("Ocp-Apim-Subscription-Key", subscriptionKey);

        // Receive JSON body
        InputStream stream = connection.getInputStream();
        Scanner scanner = new Scanner(stream);
        String response = scanner.useDelimiter("\\A").next();

        // Construct result object for return
        SearchResults results = new SearchResults(new HashMap<String, String>(), response);

        // Extract Bing-related HTTP headers
        Map<String, List<String>> headers = connection.getHeaderFields();
        for (String header : headers.keySet()) {
            if (header == null) continue;      // may have null key
            if (header.startsWith("BingAPIs-") || header.startsWith("X-MSEdge-")) {
                results.relevantHeaders.put(header, headers.get(header).get(0));
            }
        }
        stream.close();
        scanner.close();

        return results;
    }

    // pretty-printer for JSON; uses GSON parser to parse and re-serialize
    public static String prettify (String json_text) {
        JsonParser parser = new JsonParser();
        JsonObject json = (JsonObject) parser.parse(json_text);
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        return gson.toJson(json);
    }

    public static String relevantCriterion(JsonObject [] objects){
        String result = null;

        List<String> descriptions = new ArrayList();
        for( int i = 0; i < objects.length; i++){
            String text = String.valueOf(objects[i].get("snippet"));
            if(!((text).toLowerCase()).contains("offer") ||
                    (text.toLowerCase()).contains("sale") ||
                    !((String.valueOf(objects[i].get("language")).toLowerCase()).contains("en"))) {
                if(text.toLowerCase().contains("actual product")){
                    int startIndex = text.indexOf("Actual product");
                    int endIndex = text.indexOf(".", startIndex);
                    StringBuilder sb = new StringBuilder(text);
                    sb.delete(startIndex-1, endIndex+1);
                    text = sb.toString();
                }
                descriptions.add(text);
            }
        }
        String temp = descriptions.get(0);
        for (int i = 0; i < descriptions.size(); i++){
            if(temp.length() < descriptions.get(i).length()){
                temp = descriptions.get(i);
            }
        }
        result = temp.replace("\"", "");
        return result;
    }
}












