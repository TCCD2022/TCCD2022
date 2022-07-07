package com.example.proyectotccd.domain

import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.annotation.JsonNaming
import java.util.Collections.emptyList



data class Metadata(val metadata: FileInfo)

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy::class)
data class FileInfo(val filename: String = "",
                    val colIds: List<ColumnsInfo> = emptyList())

data class ColumnsInfo(val colid: String = "",
                       val colname: String = "",
                       val type: String = "",
                       val scale: String = "")