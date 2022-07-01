library(plumber)
library(jsonlite)
library(data.table)
library(ggplot2)
library(tikzDevice)
library(xfun)
library(ggfortify)


FOLDER_RESULTS <- 'dvg--results-'
MEDIA_FOLDER <- "/code/media/"
cd <- getwd()

# Sys.setenv(R_TEXI2DVICMD='emulation')


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

#* Projection based on principal component analysis
#* @post /pca
function(metadata){

  # TODO: use column types
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
  
  p <- autoplot(tpca, data = cols, colour = colorear,loadings = pbiplot, loadings.colour = 'black',
                  loadings.label = pbiplot, loadings.label.colour = 'black', loadings.label.size = 4) +
    theme_bw()
  
  p <- p + labs(title = mdat$title,
                caption = mdat$caption)
  
  p <- p + theme(plot.title = element_text(hjust = 0.5))
  
  now <- Sys.time()
#  filenametex <- file.path(respath,paste0(tmpfilename,"-pca",format(now, "%Y%m%d_%H%M%S"),".tex"))
  filenamepdf <- file.path(respath,paste0(tmpfilename,"-pca",format(now, "%Y%m%d_%H%M%S"),".pdf"))
  print(filenamepdf)
  cmwidth <- mdat$width
  cmheight <- mdat$height
  ggsave(filenamepdf, width = cmwidth, height = cmheight, units = "cm")
  # tikz(filenametex,standAlone = TRUE, sanitize=TRUE, width = cmwidth, height = cmheight)
  # print(p)
  # dev.off()
  # setwd(respath)
  # # print(getwd())
  # tools::texi2dvi(filenametex,pdf=T)
  # setwd(cd)
  # TODO: remove tex auxiliary files
  list(
    pdffile = filenamepdf,
    format = 'pdf'
  )
}
