library(plumber)
pr <- plumb("read_file.R")
pr$run(host = "0.0.0.0", port = 8181)