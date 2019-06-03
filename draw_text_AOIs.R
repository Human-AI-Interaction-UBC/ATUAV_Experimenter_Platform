library(magick)
library(stringr)

# change this path to the directory where your screenshots and .aoi files are
setwd("/Users/tiffany/Desktop/AOI_verification/aois_chrome")

# make sure this list has exactly the AOIs that you have, and that you have .png and .aoi files named with each of these numbers
mmd_list <- as.character(c(3,5,9,11,18,20,27,28,30,60,62,66,72,74,76))
# mmd_list <- as.character(c(62))

for (msnv in mmd_list){
  
  #read in image
  an_image <- image_read(paste(msnv,".png",sep=""))
  im <- image_draw(an_image)
  
  #read in AOI coordinates
  my_aois <- read.delim(paste(msnv,".aoi",sep=""), header = FALSE, sep = "\t")
  refs <-   my_aois[1,1:ncol(my_aois)]
  refs <- data.frame(lapply(refs, as.character), stringsAsFactors=FALSE)
  refs <- paste(refs[1,], collapse = "\t")
  
  refs <- str_split(refs, "\t")[[1]]
  refs <- refs[!sapply(refs, function(x) x =="")]
  
  size <- length(refs)/8
  
  for (i in 0:(size-1)){
    x <- c()
    y <- c()
    
    for (j in (8*i + 1): (8*i + 8)) {
      xy <- str_split(refs, ",")[[j]]
      x <- append(x, xy[1], length(x))
      y <- append(y, xy[2], length(y))
    }
    polygon(x,y, angle = 90, col= rgb(1,0.2,0.2,alpha=0.2))
  }
  
  image_write(im, path = paste(msnv,"_drawn.png"), format = "png")
  
}
