package com.example.proyectotccd.service

import com.example.proyectotccd.domain.FileInfo
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
import com.itextpdf.text.exceptions.IllegalPdfSyntaxException
import org.jfree.chart.renderer.category.StandardBarPainter
import java.awt.Color
import java.time.temporal.ChronoUnit

@Service
class MeanService(
    @Value("\${app.file-location.pdf}") val destinationPath: String,
    @Value("\${app.file-location.csv}") val csvPath: String,
    ) {

    companion object {
        val TYPES = setOf("double", "integer")
        val DATE_FORMATTER: DateTimeFormatter = DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss")
        val logger: Logger = LoggerFactory.getLogger(MeanService::class.java)
    }

    fun createMean(metadata: FileInfo): PdfFiles {
        val colNames = metadata.colIds.mapNotNull { column ->
            if (TYPES.any { column.type.lowercase().split(",\u00a0").contains(it) }) {
                column.colname
            } else {
                null
            }
        }
        logger.info("Calculating mean for file ${metadata.filename} and ${colNames.size} columns")

        val dirName = metadata.filename

        val doubleMatrix = logDuration("read_csv") {
            readCsv(dirName, colNames)
        }

        val meanResult = logDuration("mean") {
            mean(doubleMatrix)
        }

        val filePath = logDuration("pdf") {
            generatePDF(meanResult, dirName.split("/").last(), colNames, metadata.title, metadata.colour).also {
                logger.info("File generated on path $it")
            }
        }

        return PdfFiles(listOf(filePath))

    }

    private inline fun <T> logDuration(id: String, crossinline callback: () -> T): T {
        val start = LocalDateTime.now()
        val result = callback()
        val end = LocalDateTime.now()
        logger.info("$id duration ${ChronoUnit.MILLIS.between(start, end)}ms")

        return result
    }

    private fun readCsv(path: String, names: List<String>): List<List<Double>> {
        val file = File("$csvPath/$path")
        val result = csvReader().readAll(file)
        val doubleMatrix: MutableList<List<Double>> = arrayListOf()
        val index = arrayListOf<Int>()
        result.forEachIndexed { i, row ->
            if (i == 0) {
                row.forEachIndexed { j, colName ->
                    if (names.contains(colName)) {
                        index.add(j)
                    }
                }
                logger.info("processing columns $index corresponding to cols $names")
            } else {
                val doubleList = arrayListOf<Double>()
                index.forEach { j ->
                    var cell = row.getOrNull(j)?.toDoubleOrNull()
                    if (cell == null) {
                        logger.warn("Cell $i , $j does not have a valid numeric value")
                        cell = 0.0
                    }
                    doubleList.add(cell)
                }
                doubleMatrix.add(doubleList)
            }
        }
        return doubleMatrix
    }

    private fun generatePDF(means: List<Double>, baseName: String, cols: List<String>, title: String, colour: String): String {

        val dataset = DefaultCategoryDataset().apply {
            means.forEachIndexed { i, m ->
                setValue(m, "mean", cols[i])
            }
        }

        val jFreeChart = ChartFactory.createBarChart(
            title,
            "Column",
            "Mean value",
            dataset,
            PlotOrientation.HORIZONTAL,
            false, false, false
        )
        val renderer = StackedBarRenderer(false)
        renderer.defaultItemLabelGenerator = StandardCategoryItemLabelGenerator()
        renderer.setDefaultItemLabelsVisible(true, true)
        renderer.barPainter = StandardBarPainter()
        renderer.setSeriesPaint(0, getColour(colour))
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
        try {
            pdfTemplate.sanityCheck()
            logger.info("sanity check success")
        } catch (ex: IllegalPdfSyntaxException) {
            logger.info("sanity check failure")
            pdfTemplate.restoreState()
            pdfTemplate.restoreState()
        }
        document.close()

        return filePath
    }

    private fun getColour(colour: String) = when(colour) {
            "orange" -> Color.ORANGE
            "yellow" -> Color.YELLOW
            "blue" -> Color.BLUE
            "magenta" -> Color.MAGENTA
            "pink" -> Color.PINK
            "red" -> Color.RED
            else -> Color.RED
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