package com.dataScienceAnalyst.method.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;

@RestController
@RequestMapping("/demo")
public class MainController {
    @RequestMapping(value="/test", method = RequestMethod.GET)
    public String getGraphic(HttpServletRequest request){
        String graphic = "{name: grafica, descriptio: simulando un JSON}";
        return  graphic;
    }
}
