package com.example.proyectotccd.service

import com.example.proyectotccd.domain.Metadata
import com.github.doyaaaaaken.kotlincsv.dsl.csvReader
import com.itextpdf.awt.DefaultFontMapper
import com.itextpdf.awt.PdfGraphics2D
import com.itextpdf.text.Document
import com.itextpdf.text.pdf.PdfWriter
import org.jfree.chart.ChartFactory
import org.jfree.chart.labels.StandardCategoryItemLabelGenerator
import org.jfree.chart.plot.PlotOrientation
import org.jfree.chart.renderer.category.StackedBarRenderer
import org.jfree.data.category.DefaultCategoryDataset
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service
import java.awt.geom.Rectangle2D
import java.io.File
import java.io.FileOutputStream
import java.time.LocalDateTime

@Service
class MeanService(@Value("\${app.file-location.pdf}") val destinationPath: String) {

    fun createMean(metadata: Metadata): String {
        val columnsIds = metadata.metadata.let {
            it.colIds.filter {
                it.type == "Double"
            }.map {
                it.colid.toInt()
            }
        }

        val dirName = metadata.metadata.filename

        val doubleMatrix = readCsv(dirName, columnsIds)

        val meanResult = mean(doubleMatrix)

        return generate(meanResult, dirName.split("/").last())

    }

    fun readCsv(path: String, index: List<Int>): List<List<Double>> {
        val file = File(path)
        val result = csvReader().readAll(file)
        val doubleMatrix: MutableList<List<Double>> = arrayListOf()
        result.forEachIndexed { i, row ->
            if (i > 0) {
                val doubleList = arrayListOf<Double>()
                index.forEach { j ->
                    doubleList.add(row[j].toDouble())
                }
                doubleMatrix.add(doubleList)
            }
        }
        return doubleMatrix
    }

    fun generate(means: List<Double>, path: String): String {

        val dataset = DefaultCategoryDataset().apply {
            means.forEachIndexed { i, m ->
                setValue(m, "test 1", "columna ${i + 1}")
            }
        }

        val jFreeChart = ChartFactory.createBarChart(
            "Mean Calculator",
            "Column",
            "Mean value",
            dataset,
            PlotOrientation.HORIZONTAL,
            false, false, false
        )
        val renderer = StackedBarRenderer(false)
        renderer.defaultItemLabelGenerator = StandardCategoryItemLabelGenerator()
        renderer.setDefaultItemLabelsVisible(true, true)
        jFreeChart.categoryPlot.renderer = renderer

        val now = LocalDateTime.now()

        val filePath = "${destinationPath}/${path}-mean-${now}.pdf"
        val fos = FileOutputStream(File(filePath))
        val document = Document()
        val writer = PdfWriter.getInstance(document, fos)

        document.open()
        val pdfContentByte = writer.directContent
        val width = 500 //width of BarChart

        val height = 300 //height of BarChart

        val pdfTemplate = pdfContentByte.createTemplate(width.toFloat(), height.toFloat())

        //create graphics

        //create graphics
        PdfGraphics2D(pdfTemplate, width.toFloat(), height.toFloat(), DefaultFontMapper())
        val graphics2d = PdfGraphics2D(pdfTemplate, width.toFloat(), height.toFloat(), DefaultFontMapper())

        //create rectangle

        //create rectangle
        val rectangle2d: Rectangle2D = Rectangle2D.Double(
            0.0, 0.0, width.toDouble(), height.toDouble()
        )

        jFreeChart.draw(graphics2d, rectangle2d)

        pdfContentByte.addTemplate(pdfTemplate, 40f, 500f) //0, 0 will draw BAR chart on bottom left of page
        graphics2d.dispose()
        pdfTemplate.restoreState()
        pdfTemplate.restoreState()
        document.close()

        return filePath
    }

    fun mean(values: List<List<Double>>): List<Double> {
        val result = arrayListOf<Double>().apply {
            repeat(values.first().size) {
                add(0.0)
            }
        }
        values.forEach { row ->
            row.forEachIndexed { i, col ->
                result[i] += (col / values.size)
            }
        }
        return result
    }

}