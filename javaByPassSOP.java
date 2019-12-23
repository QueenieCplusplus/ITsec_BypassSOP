import java.applet.*;

import java.net.*;
import java.util.*;
import java.io.*;

import java.awt.*;

public class javaByPassSOP extends Applet{

    public javaByPassSOP(){
        super();
        return;
    }

    public static String getInfo(){

        String result = "";

        try {
            
            URL url = new URL("");// 建立java.net.URL 物件實例, 引數輸入網頁網址字串。
            
            BufferReader inStream = new BufferReader(new InputStreamReader(url.open()));
            
            String inLine;
            while((inLine = inStream.readLine()) != null)
                result += inLine;
                inLine.close();

        } catch(Exception e) {

            result = "e:" + e.toString();

        }

        return result;

    }
}

