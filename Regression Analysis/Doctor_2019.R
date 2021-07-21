## Read Data
  library(Ecdat)
  data(Doctor)

  str(Doctor)
  head(Doctor)
  head(Doctor[,2:4])


attach(Doctor)

  doctor.dep <- as.matrix(Doctor[,1])
  doctor.var <- as.matrix(Doctor[,2:4])

  solve(crossprod(doctor.var),t(doctor.var)%*%doctor.dep)

  lm(doctor~children+access+health)

detach(Doctor)