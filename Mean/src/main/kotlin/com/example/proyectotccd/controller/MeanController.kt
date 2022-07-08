package com.example.proyectotccd.controller

import com.example.proyectotccd.domain.Metadata
import com.example.proyectotccd.service.MeanService
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

@RestController
class MeanController(val meanService: MeanService) {

    @PostMapping("/calculate")
    fun createMean(@RequestBody metadata: Metadata): String{
        return meanService.createMean(metadata)
    }

}