library(magick)
library(stringr)


setwd("/Users/kristys/Documents/AOI_ATUAV_Experimenter_Platform")

# make sure this list has exactly the AOIs that you have, and that you have .png and .aoi files named with each of these numbers
#mmd_list <- as.character(c(3,5,9,11,18,20,27,28,30,60,62,66,72,74,76))
mmd_list <- as.character(c(62))

for (msnv in mmd_list){
  
  #read in image
  an_image <- image_read(paste("../msnv_screenshots/", msnv, ".png", sep=""))
  im <- image_draw(an_image)
  
  #read in AOI coordinates
  aois <- read.delim(paste(msnv,".aoi",sep=""), header = FALSE, sep = "\t")
  aois <- data.frame(lapply(aois, as.character), stringsAsFactors=FALSE)
  

  for (i in 1:nrow(aois)) {
    x <- c()
    y <- c()
    
    for (j in 2:9) {
      xy <- str_split(aois[i, j], ",")[[1]]
      x <- append(x, xy[1])
      y <- append(y, xy[2])
    }
    polygon(x,y, angle = 90, col= rgb(1,0.2,0.2,alpha=0.2))
  }
  
  image_write(im, path = paste(msnv,"_drawn.png"), format = "png")
  
}
