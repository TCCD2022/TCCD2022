package com.example.proyectotccd.controller

import com.example.proyectotccd.domain.Metadata
import com.example.proyectotccd.service.MeanService
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

@RestController("/mean")
class MeanController(val meanService: MeanService) {

    @PostMapping("/createMean")
    fun createMean(@RequestBody metadata: Metadata): String{
        return meanService.createMean(metadata)
    }

}