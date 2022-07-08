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
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service
import java.awt.geom.Rectangle2D
import java.io.File
import java.io.FileOutputStream
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import com.example.proyectotccd.domain.PdfFiles

@Service
class MeanService(
    @Value("\${app.file-location.pdf}") val destinationPath: String,
    @Value("\${app.file-location.csv}") val csvPath: String,
    ) {

    companion object {
        val TYPES = setOf("double", "integer")
        val DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss")
        val logger: Logger = LoggerFactory.getLogger(MeanService::class.java)
    }

    fun createMean(metadata: Metadata): PdfFiles {
        val colNames = arrayListOf<String>()
        val columnsIds = metadata.metadata.colIds.mapNotNull {
            if (TYPES.contains(it.type.lowercase())) {
                colNames.add(it.colname)
                it.colid.toInt()
            } else {
                null
            }
        }
        logger.info("Calculating mean for file ${metadata.metadata.filename} and ${columnsIds.size} columns")

        val dirName = metadata.metadata.filename

        val doubleMatrix = readCsv(dirName, columnsIds)

        val meanResult = mean(doubleMatrix)

        val filePath = generatePDF(meanResult, dirName.split("/").last(), colNames).also {
            logger.info("File generated on path $it")
        }

        return PdfFiles(listOf(filePath))

    }

    private fun readCsv(path: String, index: List<Int>): List<List<Double>> {
        val file = File("$csvPath/$path")
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

    private fun generatePDF(means: List<Double>, baseName: String, cols: List<String>): String {

        val dataset = DefaultCategoryDataset().apply {
            means.forEachIndexed { i, m ->
                setValue(m, "mean", cols[i])
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

        val filePath = "${destinationPath}/${baseName}-mean-${now.format(DATE_FORMATTER)}.pdf"
        val fos = FileOutputStream(File(filePath))
        val document = Document()
        val writer = PdfWriter.getInstance(document, fos)

        document.open()
        val pdfContentByte = writer.directContent
        val width = 500 //width of BarChart
        val height = 300 //height of BarChart

        val pdfTemplate = pdfContentByte.createTemplate(width.toFloat(), height.toFloat())

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
        document.close()

        return filePath
    }

    private fun mean(values: List<List<Double>>): List<Double> {
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