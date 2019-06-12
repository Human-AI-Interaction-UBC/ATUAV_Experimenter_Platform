library(magick)
library(stringr)


setwd("/Users/kristys/Documents/AOI_ATUAV_Experimenter_Platform")

# make sure this list has exactly the AOIs that you have, and that you have .png and .aoi files named with each of these numbers
mmd_list <- as.character(c(3,5,9,11,20,27,28,30,60,62,66,72,74,76,18))
#mmd_list <- as.character(c(27, 66))

for (msnv in mmd_list) {
  
  #read in image
  an_image <- image_read(paste("../msnv_screenshots_old/", msnv, "_old.png", sep=""))
  im <- image_draw(an_image)
  
  #read in AOI coordinates
  aois <- read.delim(paste("ref_aois_control/", msnv,".aoi",sep=""), header = FALSE, sep = "\t")
  aois <- data.frame(lapply(aois, as.character), stringsAsFactors=FALSE)
  

  for (i in 1:nrow(aois)) {
    x <- c()
    y <- c()
    
    if (grepl('overall', aois[i, 1]))
      break
    
    for (j in 2:9) {
      xy <- str_split(aois[i, j], ",")[[1]]
      x <- append(x, xy[1])
      y <- append(y, xy[2])
    }
    polygon(x,y, angle = 90, col= rgb(1,0.2,0.2,alpha=0.2))
  }
  
  image_write(im, path = paste('../', msnv,"_old_drawn.png"), format = "png")
}
