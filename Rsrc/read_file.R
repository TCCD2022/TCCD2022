library(plumber)
library(jsonlite)
library(data.table)
library(ggplot2)
library(xfun)
library(ggfortify)


FOLDER_RESULTS <- 'dvg--results-'

# Shared volume
MEDIA_FOLDER <- "/code/media/"

# current working directory
cd <- getwd()


# filename: csv file variable common to all data analysis methods

#* Extracts file metadata such as number of rows, columns and file size
#* @param filename full file path
#* @post /coltypes
function(filename){

  DATA <- fread(filename)
  
  list(
    numrows = nrow(DATA),
    numcols = ncol(DATA),
    filesize = file.info(filename)$size,
    coltypes = DATA[, lapply(.SD, typeof)]
  )
}


# medatadata: json structure that includes:
# filename: csv file path
# col_ids: is a structure containing information about the variables to be used
# 	   'colid' column ids,
#          'colname' column/variable names
#	   'type' variable types and
#	   'scale' scale of the variables columns 

# autor: Venustiano Soancatl Aguilar

#* Projection based on principal component analysis
#* @post /pca
function(metadata){

  # INPUT 
  # colour: categorical variable to color data points
  # scale: boolean variable
  # biplot: boolean variable to include a biplot or not
  # height: height of the plot in cm
  # width: width of the plot in cm
  # title: title of the plot
  # caption: caption of the plot

  # OUTPUT
  # file plot saved in the shared filesystem
  # list including filepath and fileformat

  # TODO: handle exceptions

  mdat <- fromJSON(metadata)
  
  mcols <- as.data.table(mdat$col_ids)
  colorear <- mdat$colour
  
  if (colorear == "--No variable--"){
    colorear = NULL
  }
  pscale <- mdat$scale
  pbiplot <- mdat$biplot
  
  print(as.data.table(mdat$col_ids))
  print(mdat$height)
  print(mdat$width)

  # full path of the filename
  filename <- paste0(MEDIA_FOLDER,mdat$filename)
  
  dpath <- dirname(filename)
  respath = file.path(dpath, FOLDER_RESULTS)
  tmpfilename <- basename(filename)                   # Apply basename function
  
  print(dpath)
  print(tmpfilename)
  print(respath)
  
  # check if sub directory exists 
  if (!dir.exists(respath)){
    # create a new sub directory inside
    dir.create(respath)
  }

  pcacols <- mcols[,colname]
  
  print(pcacols)
  
  cols <- fread(filename,select = pcacols)
  
  # print(cols)
  
  pcacols <- pcacols[! pcacols %in% append(c(),colorear)]

  # print(pcacols)
  # print(cols[,..pcacols])
  
  # PCA
  tpca <- prcomp(Filter(is.numeric,cols[,..pcacols]),scale=pscale)
  summary(tpca)

  # projection plot
  
  p <- autoplot(tpca, data = cols, colour = colorear,loadings = pbiplot, loadings.colour = 'black',
                  loadings.label = pbiplot, loadings.label.colour = 'black', loadings.label.size = 4) +
    theme_bw()
  
  p <- p + labs(title = mdat$title,
                caption = mdat$caption)
  
  p <- p + theme(plot.title = element_text(hjust = 0.5))
  
  now <- Sys.time()
  filenamepdf <- file.path(respath,paste0(tmpfilename,"-pca",format(now, "%Y%m%d_%H%M%S"),".pdf"))
  print(filenamepdf)
  cmwidth <- mdat$width
  cmheight <- mdat$height
  
  ggsave(filenamepdf, width = cmwidth, height = cmheight, units = "cm")

  list(
    pdffile = filenamepdf,
    format = 'pdf'
  )
}
