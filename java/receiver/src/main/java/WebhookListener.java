  /* Copyright 2019 Esri
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
   http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.*/

import org.json.JSONObject;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import static java.nio.file.StandardOpenOption.APPEND;
import static java.nio.file.StandardOpenOption.CREATE;

@WebServlet("/WebhookListener")
public class WebhookListener extends HttpServlet {
  private static final String filePath = "c:\\temp\\webhookPayloads.txt";

  @Override
  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    response.setContentType("text/html");
    PrintWriter out = response.getWriter();
    out.println("<h3>Hello from Webhook Listener!</h3>");
    out.println("<h5>Simple Java HttpServlet that can receive in coming Webhook pay loads, convert to JSON format and write to a file in disk!</h5>");
  }

  @Override
  protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    resp.setContentType("text/html");
    PrintWriter out = resp.getWriter();

    StringBuilder builder = new StringBuilder();
    String aux = "";

    while ((aux = req.getReader().readLine()) != null) {
      builder.append(aux);
    }
    String payLoad = builder.toString();
    try {
        //Convert to Json
      JSONObject jsonPayLoad = new JSONObject(payLoad);
      String s = jsonPayLoad.toString() + System.lineSeparator();
        //write to stdout
        System.out.println("Received Payload:: " + jsonPayLoad.toString());
        //write to a file
        Path path = Paths.get(filePath);
        byte[] strToByte = s.getBytes();
        Files.write(path,strToByte,APPEND,CREATE);
        out.println("{\"success\":\"true\"}");
    } catch (Exception e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
  }
}
