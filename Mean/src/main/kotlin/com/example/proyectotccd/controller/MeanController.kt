package com.example.proyectotccd.controller

import com.example.proyectotccd.domain.Metadata
import com.example.proyectotccd.domain.FileInfo
import com.example.proyectotccd.domain.PdfFiles
import com.example.proyectotccd.service.MeanService
import com.fasterxml.jackson.databind.ObjectMapper
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import java.nio.charset.StandardCharsets
@RestController
class MeanController(val meanService: MeanService, val mapper: ObjectMapper) {

    companion object {
        val logger: Logger = LoggerFactory.getLogger(MeanController::class.java)
    }

    @PostMapping(path = ["/calculate"], consumes = ["application/x-www-form-urlencoded;charset=UTF-8"])
    fun createMean(@RequestBody metadata: String): PdfFiles{
        logger.info("$metadata")
        val metadaInfo = metadata.split("=")[1]
        val metadataDecode = java.net.URLDecoder.decode(metadaInfo, StandardCharsets.UTF_8.displayName());
        logger.info("$metadataDecode")
        return meanService.createMean(Metadata(mapper.readValue(metadataDecode, FileInfo::class.java)))
    }

}