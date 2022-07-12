package com.dataScienceAnalyst.method.jsonEntity;

public class ObjectRequest {
    private Integer width;
    private Integer height;
    private Integer titleSize;
    private Integer paragraphSize;
    private String textTitle;
    private String textParagraph;
    private String titleGraphic;
    private String xLabel;
    private String yLabel;

    public String getxLabel() {
        return xLabel;
    }

    public void setxLabel(String xLabel) {
        this.xLabel = xLabel;
    }

    public String getyLabel() {
        return yLabel;
    }

    public void setyLabel(String yLabel) {
        this.yLabel = yLabel;
    }

    public String getTitleGraphic() {
        return titleGraphic;
    }

    public void setTitleGraphic(String titleGraphic) {
        this.titleGraphic = titleGraphic;
    }

    public Integer getWidth() {
        return width;
    }

    public void setWidth(Integer width) {
        this.width = width;
    }

    public Integer getHeight() {
        return height;
    }

    public void setHeight(Integer height) {
        this.height = height;
    }

    public Integer getTitleSize() {
        return titleSize;
    }

    public void setTitleSize(Integer titleSize) {
        this.titleSize = titleSize;
    }

    public Integer getParagraphSize() {
        return paragraphSize;
    }

    public void setParagraphSize(Integer paragraphSize) {
        this.paragraphSize = paragraphSize;
    }

    public String getTextTitle() {
        return textTitle;
    }

    public void setTextTitle(String textTitle) {
        this.textTitle = textTitle;
    }

    public String getTextParagraph() {
        return textParagraph;
    }

    public void setTextParagraph(String textParagraph) {
        this.textParagraph = textParagraph;
    }
}
