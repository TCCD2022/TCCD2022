package com.example.proyectotccd.domain

data class PdfFiles(val pdffile: List<String>,
                    val format: List<String> = listOf("pdf"))