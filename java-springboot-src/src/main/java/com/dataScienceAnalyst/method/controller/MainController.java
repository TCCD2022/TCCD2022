package com.dataScienceAnalyst.method.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import com.dataScienceAnalyst.method.MethodApplication;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/demo")
public class MainController {
    private final MethodApplication methodService;

    public MainController(MethodApplication methodService) {
        this.methodService = methodService;
    }

    @RequestMapping(value="/test", method = RequestMethod.GET)
    public void getGraphic(HttpServletResponse response) throws IOException {
        response.setContentType("application/pdf");
        DateFormat dateFormatter = new SimpleDateFormat("yyyy-MM-dd:hh:mm:ss");
        String currentDateTime = dateFormatter.format(new Date());

        String headerKey = "Content-Disposition";
        String headerValue = "attachment; filename=pdf_" + currentDateTime + ".pdf";
        response.setHeader(headerKey, headerValue);

        //this.methodService.export(response);
    }

    @RequestMapping(value="/method", method = RequestMethod.POST)
    public void methodTeam2(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String bodyUrlEncoded = request.getReader().lines().collect(Collectors.joining(System.lineSeparator()));
        System.out.println(bodyUrlEncoded);
        String data = bodyUrlEncoded.split("=")[1];
        String bodyText = java.net.URLDecoder.decode(data, StandardCharsets.UTF_8.displayName());
        System.out.println(bodyText);
        this.methodService.export(bodyText,response);
    }
}
