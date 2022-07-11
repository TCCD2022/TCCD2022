package com.dataScienceAnalyst.method;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Service;

import javax.imageio.ImageIO;
import javax.servlet.http.HttpServletResponse;
import java.awt.image.BufferedImage;
import java.io.*;

import com.lowagie.text.*;
import com.lowagie.text.pdf.PdfWriter;

@Service
@SpringBootApplication
public class MethodApplication {
    public static void main(String[] args) {
        SpringApplication.run(MethodApplication.class, args);
    }

    public void export(HttpServletResponse response) throws IOException {

        DefaultCategoryDataset data = new DefaultCategoryDataset();

        data.setValue(4, "Prueba Termodinamica", "Andrés");
        data.setValue(4, "Prueba Termodinamica", "Camila");
        data.setValue(5, "Prueba Termodinamica", "Fernando");

        data.setValue(2, "Prueba Quimica I", "Andrés");
        data.setValue(3, "Prueba Quimica I", "Camila");
        data.setValue(3, "Prueba Quimica I", "Fernando");

        JFreeChart graphicBar = ChartFactory.createBarChart3D(
                "Resultados Prueba",
                "Estudiante",
                "Puntaje",
                data,
                PlotOrientation.VERTICAL,
                true,
                true,
                false
        );

        BufferedImage objBufferedImage= graphicBar.createBufferedImage(500,300);
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

        Document document = new Document(PageSize.A4);
        PdfWriter.getInstance(document, response.getOutputStream());

        document.open();
        Font fontTitle = FontFactory.getFont(FontFactory.HELVETICA_BOLD);
        fontTitle.setSize(18);

        Paragraph paragraph = new Paragraph("Graficos de los resultados obtenidos", fontTitle);
        paragraph.setAlignment(Paragraph.ALIGN_CENTER);

        Font fontParagraph = FontFactory.getFont(FontFactory.HELVETICA);
        fontParagraph.setSize(12);

        Paragraph paragraph2 = new Paragraph("A continuacion se presenta una grafica de barras con los resultados obtenidos en la prueba", fontParagraph);
        paragraph2.setAlignment(Paragraph.ALIGN_LEFT);

        Image png = Image.getInstance("image.png");

        document.add(paragraph);
        document.add(paragraph2);
        document.add(png);
        document.close();
    }

}
