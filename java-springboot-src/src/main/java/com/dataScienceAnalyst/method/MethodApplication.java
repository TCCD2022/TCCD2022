package com.dataScienceAnalyst.method;

import com.itextpdf.text.*;
import com.itextpdf.text.pdf.PdfWriter;
import com.dataScienceAnalyst.method.jsonEntity.ObjectRequest;
import com.opencsv.CSVReader;
import com.opencsv.exceptions.CsvException;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Service;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;

import javax.imageio.ImageIO;
import javax.servlet.http.HttpServletResponse;

import com.google.gson.Gson;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.List;


@Service
@SpringBootApplication
public class MethodApplication {
    public static void main(String[] args) {
        SpringApplication.run(MethodApplication.class, args);
    }

    public String export(String request, HttpServletResponse response) throws IOException, DocumentException {


        ObjectRequest obj = new Gson().fromJson(request, ObjectRequest.class);
        System.out.println(obj.getFilename());

        DefaultCategoryDataset data = new DefaultCategoryDataset();
        data = readCastCSV(data, obj.getFilename());

    /*
        data.setValue(4, "Prueba Termodinamica", "Andrés");
        data.setValue(4, "Prueba Termodinamica", "Camila");
        data.setValue(5, "Prueba Termodinamica", "Fernando");

        data.setValue(2, "Prueba Quimica I", "Andrés");
        data.setValue(3, "Prueba Quimica I", "Camila");
        data.setValue(3, "Prueba Quimica I", "Fernando");
    */
        JFreeChart graphicBar = ChartFactory.createBarChart3D(
                obj.getTitleGraphic(),
                obj.getxLabel(),
                obj.getyLabel(),
                data,
                PlotOrientation.VERTICAL,
                true,
                true,
                false
        );

        BufferedImage objBufferedImage= graphicBar.createBufferedImage(obj.getWidth(),obj.getHeight());
        ByteArrayOutputStream bas = new ByteArrayOutputStream();
        try {
            ImageIO.write(objBufferedImage, "png", bas);
        } catch (IOException e) {
            e.printStackTrace();
        }

        byte[] byteArray=bas.toByteArray();

        InputStream in = new ByteArrayInputStream(byteArray);
        BufferedImage image = ImageIO.read(in);
        File outputfile = new File("image.png");
        ImageIO.write(image, "png", outputfile);

        Document document = new Document();
        //PdfWriter.getInstance(document, response.getOutputStream());

        DateFormat dateFormatter = new SimpleDateFormat("yyyy-MM-dd:hh:mm:ss");
        String currentDateTime = dateFormatter.format(new Date());

        String route = "/code/media/documents/mbg_" + currentDateTime + ".pdf";
        PdfWriter.getInstance(document, new FileOutputStream(route));

        document.open();
        Font fontTitle = FontFactory.getFont(FontFactory.HELVETICA_BOLD);
        fontTitle.setSize(obj.getTitleSize());

        Paragraph paragraph = new Paragraph(obj.getTextTitle(), fontTitle);
        paragraph.setAlignment(Paragraph.ALIGN_CENTER);

        Font fontParagraph = FontFactory.getFont(FontFactory.HELVETICA);
        fontParagraph.setSize(obj.getParagraphSize());

        Paragraph paragraph2 = new Paragraph(obj.getTextParagraph(), fontParagraph);
        paragraph2.setAlignment(Paragraph.ALIGN_LEFT);

        Image png = Image.getInstance("image.png");

        document.add(paragraph);
        document.add(paragraph2);
        document.add(png);
        document.close();
        return route;

    }

    public DefaultCategoryDataset readCastCSV(DefaultCategoryDataset data, String csvRoute) throws FileNotFoundException {
        try(CSVReader reader = new CSVReader(new FileReader("/code/media/"+ csvRoute))){
            List<String[]> r = reader.readAll();
            for (int i = 1; i < r.size(); i++) {
                for (int j = 0; j < r.get(0).length-1; j++) {
                    data.setValue(Double.parseDouble(r.get(i)[j]), r.get(0)[j], r.get(0)[j+1]);
                }
            }

        } catch (IOException | CsvException ioException) {
            ioException.printStackTrace();
        }
        return data;
    }

}
